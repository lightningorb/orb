import base64
import codecs
import os
from functools import lru_cache
from traceback import print_exc
from orb.lnd.lnd_base import LndBase
from orb.store.db_cache import aliases_cache

try:
    import grpc

    from orb.lnd.grpc_generated import router_pb2 as lnrouter
    from orb.lnd.grpc_generated import router_pb2_grpc as lnrouterrpc
    from orb.lnd.grpc_generated import lightning_pb2 as ln
    from orb.lnd.grpc_generated import lightning_pb2_grpc as lnrpc
    from orb.lnd.grpc_generated import invoices_pb2 as invoices
    from orb.lnd.grpc_generated import invoices_pb2_grpc as invoicesrpc
except:
    print_exc()

MESSAGE_SIZE_MB = 50 * 1024 * 1024


class Lnd(LndBase):
    def __init__(self, tls_certificate, server, network, macaroon):
        os.environ["GRPC_SSL_CIPHER_SUITES"] = "HIGH+ECDSA"
        combined_credentials = self.get_credentials(
            tls_certificate.encode(), network, macaroon.encode()
        )
        channel_options = [
            ("grpc.max_message_length", MESSAGE_SIZE_MB),
            ("grpc.max_receive_message_length", MESSAGE_SIZE_MB),
        ]
        grpc_channel = grpc.secure_channel(
            server + ":10009", combined_credentials, channel_options
        )
        self.stub = lnrpc.LightningStub(grpc_channel)
        self.router_stub = lnrouterrpc.RouterStub(grpc_channel)
        self.invoices_stub = invoicesrpc.InvoicesStub(grpc_channel)

    @staticmethod
    def get_credentials(tls_certificate, network, macaroon):
        ssl_credentials = grpc.ssl_channel_credentials(tls_certificate)
        auth_credentials = grpc.metadata_call_credentials(
            lambda _, callback: callback([("macaroon", macaroon)], None)
        )
        combined_credentials = grpc.composite_channel_credentials(
            ssl_credentials, auth_credentials
        )
        return combined_credentials

    @lru_cache(maxsize=None)
    def get_info(self):
        return self.stub.GetInfo(ln.GetInfoRequest())

    def get_balance(self):
        return self.stub.WalletBalance(ln.WalletBalanceRequest())

    def channel_balance(self):
        request = ln.ChannelBalanceRequest()
        response = self.stub.ChannelBalance(request)
        return response

    def sign_message(self, message):
        request = ln.SignMessageRequest(msg=message.encode())
        return self.stub.SignMessage(request)

    @aliases_cache
    def get_node_alias(self, pub_key):
        return self.stub.GetNodeInfo(
            ln.NodeInfoRequest(pub_key=pub_key, include_channels=False)
        ).node.alias

    @lru_cache(maxsize=None)
    def get_node_info(self, pub_key):
        return self.stub.GetNodeInfo(
            ln.NodeInfoRequest(pub_key=pub_key, include_channels=True)
        )

    @lru_cache(maxsize=None)
    def get_node_channels_pubkeys(self, pub_key):
        node_info = self.get_node_info(pub_key)
        return [
            (c.node1_pub, c.node2_pub)[pub_key == c.node1_pub]
            for c in node_info.channels
        ]

    def get_own_pubkey(self):
        return self.get_info().identity_pubkey

    def generate_invoice(self, memo, amount):
        invoice_request = ln.Invoice(memo=memo, value=amount, expiry=60)
        add_invoice_response = self.stub.AddInvoice(invoice_request)
        return add_invoice_response.payment_request, self.decode_payment_request(
            add_invoice_response.payment_request
        )

    def cancel_invoice(self, payment_hash):
        payment_hash_bytes = self.hex_string_to_bytes(payment_hash)
        return self.invoices_stub.CancelInvoice(
            invoices.CancelInvoiceMsg(payment_hash=payment_hash_bytes)
        )

    def list_invoices(self):
        request = ln.ListInvoiceRequest(
            pending_only=False, index_offset=0, num_max_invoices=100, reversed=False
        )
        return self.stub.ListInvoices(request)

    def decode_payment_request(self, payment_request):
        request = ln.PayReqString(pay_req=payment_request)
        return self.stub.DecodePayReq(request)

    def get_channels(self, active_only=False, use_cache=True):
        return self.stub.ListChannels(
            ln.ListChannelsRequest(active_only=active_only)
        ).channels

    @lru_cache(maxsize=None)
    def get_max_channel_capacity(self):
        max_channel_capacity = 0
        for channel in self.get_channels(active_only=False):
            if channel.capacity > max_channel_capacity:
                max_channel_capacity = channel.capacity
        return max_channel_capacity

    def get_route(
        self,
        pub_key,
        amount,
        ignored_pairs,
        ignored_nodes,
        last_hop_pubkey,
        outgoing_chan_id,
        fee_limit_msat,
    ):
        if fee_limit_msat:
            fee_limit = {"fixed_msat": int(fee_limit_msat)}
        else:
            fee_limit = None
        if last_hop_pubkey:
            last_hop_pubkey = base64.b16decode(last_hop_pubkey, True)
        request = ln.QueryRoutesRequest(
            pub_key=pub_key,
            last_hop_pubkey=last_hop_pubkey,
            outgoing_chan_id=outgoing_chan_id,
            amt=amount,
            ignored_pairs=ignored_pairs,
            fee_limit=fee_limit,
            ignored_nodes=ignored_nodes,
            use_mission_control=True,
        )
        try:
            response = self.stub.QueryRoutes(request)
            return response.routes
        except:
            return None

    # @lru_cache(maxsize=None)
    def get_edge(self, channel_id):
        return self.stub.GetChanInfo(ln.ChanInfoRequest(chan_id=channel_id))

    def get_policy_to(self, channel_id):
        edge = self.get_edge(channel_id)
        # node1_policy contains the fee base and rate for payments from node1 to node2
        if edge.node1_pub == self.get_own_pubkey():
            return edge.node1_policy
        return edge.node2_policy

    def get_policy_from(self, channel_id):
        edge = self.get_edge(channel_id)
        # node1_policy contains the fee base and rate for payments from node1 to node2
        if edge.node1_pub == self.get_own_pubkey():
            return edge.node2_policy
        return edge.node1_policy

    def get_ppm_to(self, channel_id):
        return self.get_policy_to(channel_id).fee_rate_milli_msat

    def get_ppm_from(self, channel_id):
        return self.get_policy_from(channel_id).fee_rate_milli_msat

    def send_payment(self, payment_request, route):
        last_hop = route.hops[-1]
        last_hop.mpp_record.payment_addr = payment_request.payment_addr
        last_hop.mpp_record.total_amt_msat = payment_request.num_msat
        request = lnrouter.SendToRouteRequest(route=route)
        request.payment_hash = self.hex_string_to_bytes(payment_request.payment_hash)
        result = []
        res = self.router_stub.SendToRouteV2(request)
        return res

    @lru_cache(maxsize=None)
    def decode_request(self, req: str):
        request = ln.PayReqString(pay_req=req)
        response = self.stub.DecodePayReq(request)
        return response

    def open_channel(self, node_pubkey_string, sat_per_vbyte, amount_sat):
        request = ln.OpenChannelRequest(
            sat_per_vbyte=sat_per_vbyte,
            node_pubkey_string=node_pubkey_string,
            local_funding_amount=amount_sat,
            push_sat=0,
            private=False,
            spend_unconfirmed=False,
        )
        response = self.stub.OpenChannelSync(request)
        return response

    def close_channel(self, channel_point, force, sat_per_vbyte):
        request = ln.CloseChannelRequest(
            channel_point=channel_point, force=force, sat_per_vbyte=sat_per_vbyte
        )
        return self.stub.CloseChannel(request)

    def new_address(self):
        request = ln.NewAddressRequest(type=0, account=None)
        response = self.stub.NewAddress(request)
        return response

    def connect(self, addr):
        pk, h = addr.split("@")
        ln_addr = ln.LightningAddress(pubkey=pk, host=h)
        request = ln.ConnectPeerRequest(addr=ln_addr, perm=False, timeout=10)
        return self.stub.ConnectPeer(request)

    def send_coins(self, addr, amount, sat_per_vbyte):
        return self.stub.SendCoins(
            ln.SendCoinsRequest(addr=addr, amount=amount, sat_per_vbyte=sat_per_vbyte)
        )
        return response

    def update_channel_policy(self, channel, *args, **kwargs):
        tx, output = channel.channel_point.split(":")
        cp = ln.ChannelPoint(funding_txid_str=tx, output_index=int(output))
        request = ln.PolicyUpdateRequest(*args, **kwargs, chan_point=cp)
        return self.stub.UpdateChannelPolicy(request)

    def get_htlc_events(self):
        request = lnrouter.SubscribeHtlcEventsRequest()
        return self.router_stub.SubscribeHtlcEvents(request)

    def get_channel_events(self):
        request = ln.ChannelEventSubscription()
        return self.stub.SubscribeChannelEvents(request)

    def get_forwarding_history(
        self, start_time=None, end_time=None, index_offset=0, num_max_events=100
    ):
        request = ln.ForwardingHistoryRequest(
            start_time=start_time,
            end_time=end_time,
            index_offset=index_offset,
            num_max_events=num_max_events,
        )
        return self.stub.ForwardingHistory(request)

    # def keysend(self, target_pubkey, msg, amount, fee_limit, timeout):
    #     secret = secrets.token_bytes(32)
    #     hashed_secret = sha256(secret).hexdigest()
    #     custom_records = [
    #         (5482373484, secret),
    #     ]
    #     msg = str(msg)
    #     if len(msg) > 0:
    #         custom_records.append((34349334, bytes.fromhex(msg.encode("utf-8").hex())))
    #     for response in self.router_stub.SendPaymentV2(
    #         lnr.SendPaymentRequest(
    #             dest=bytes.fromhex(target_pubkey),
    #             dest_custom_records=custom_records,
    #             fee_limit_sat=fee_limit,
    #             timeout_seconds=timeout,
    #             amt=amount,
    #             payment_hash=bytes.fromhex(hashed_secret),
    #         )
    #     ):
    #         if response.status == 1:
    #             print("In-flight")
    #         if response.status == 2:
    #             print("Succeeded")
    #         if response.status == 3:
    #             if response.failure_reason == 1:
    #                 print("Failure - Timeout")
    #             elif response.failure_reason == 2:
    #                 print("Failure - No Route")
    #             elif response.failure_reason == 3:
    #                 print("Failure - Error")
    #             elif response.failure_reason == 4:
    #                 print("Failure - Incorrect Payment Details")
    #             elif response.failure_reason == 5:
    #                 print("Failure Insufficient Balance")
    #         if response.status == 0:
    #             print("Unknown Error")

    def get_channel(self, chan_id):
        for channel in self.get_channels():
            if chan_id == channel.chan_id:
                return channel

    def get_channel_remote_balance(self, chan_id):
        for channel in self.get_channels():
            if chan_id == channel.chan_id:
                return channel.remote_balance

    def get_channel_local_balance(self, chan_id):
        for channel in self.get_channels():
            if chan_id == channel.chan_id:
                return channel.local_balance

    def get_own_alias(self):
        return self.get_info().alias

    def fee_report(self):
        request = ln.FeeReportRequest()
        return self.stub.FeeReport(request)

    def cancel_invoice(self, payment_hash):
        payment_hash_bytes = self.hex_string_to_bytes(payment_hash)
        return self.invoices_stub.CancelInvoice(
            invoices.CancelInvoiceMsg(payment_hash=payment_hash_bytes)
        )

    def get_pending_channels(self):
        request = ln.PendingChannelsRequest()
        response = self.stub.PendingChannels(request)
        return response

    def subscribe_channel_graph(self):
        request = ln.GraphTopologySubscription()
        return self.stub.SubscribeChannelGraph(request)
