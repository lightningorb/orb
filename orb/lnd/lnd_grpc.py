# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-15 07:15:28
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-08-23 05:07:25
import sys
import os
import json
import base64

from typing import Union
from functools import lru_cache
from traceback import print_exc

from memoization import cached

from orb.misc.auto_obj import dict2obj
from orb.lnd.lnd_base import LndBase
from orb.store.db_cache import aliases_cache
from google.protobuf.json_format import MessageToJson


sys.path.append("orb/lnd/grpc_generate")
sys.path.append("orb/lnd")

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


class LndGRPC(LndBase):
    def __init__(self, tls_certificate, server, port, macaroon):
        super(LndGRPC, self).__init__("grpc")
        os.environ["GRPC_SSL_CIPHER_SUITES"] = "HIGH+ECDSA"
        combined_credentials = self.get_credentials(
            tls_certificate.encode()
            if type(tls_certificate) is str
            else tls_certificate,
            macaroon.encode() if type(macaroon) is str else macaroon,
        )
        channel_options = [
            ("grpc.max_message_length", MESSAGE_SIZE_MB),
            ("grpc.max_receive_message_length", MESSAGE_SIZE_MB),
        ]
        grpc_channel = grpc.secure_channel(
            f"{server}:{port}", combined_credentials, channel_options
        )
        self.stub = lnrpc.LightningStub(grpc_channel)
        self.router_stub = lnrouterrpc.RouterStub(grpc_channel)
        self.invoices_stub = invoicesrpc.InvoicesStub(grpc_channel)
        self.version = None

    @staticmethod
    def get_credentials(tls_certificate, macaroon):
        ssl_credentials = grpc.ssl_channel_credentials(tls_certificate)
        auth_credentials = grpc.metadata_call_credentials(
            lambda _, callback: callback([("macaroon", macaroon)], None)
        )
        combined_credentials = grpc.composite_channel_credentials(
            ssl_credentials, auth_credentials
        )
        return combined_credentials

    def get_info(self):
        json_obj = json.loads(
            MessageToJson(
                self.stub.GetInfo(ln.GetInfoRequest()),
                including_default_value_fields=True,
                preserving_proto_field_name=True,
                sort_keys=True,
            )
        )
        return dict2obj(json_obj)

    def get_balance(self):
        json_obj = json.loads(
            MessageToJson(
                self.stub.WalletBalance(ln.WalletBalanceRequest()),
                including_default_value_fields=True,
                preserving_proto_field_name=True,
                sort_keys=True,
            )
        )
        return dict2obj(json_obj)

    def channel_balance(self):
        request = ln.ChannelBalanceRequest()
        response = self.stub.ChannelBalance(request)
        return response

    def sign_message(self, message):
        request = ln.SignMessageRequest(msg=message.encode())
        return self.stub.SignMessage(request).signature

    @aliases_cache
    def get_node_alias(self, pub_key):
        return self.stub.GetNodeInfo(
            ln.NodeInfoRequest(pub_key=pub_key, include_channels=False)
        ).node.alias

    @lru_cache(maxsize=None)
    def get_node_info(self, pub_key):
        response = self.stub.GetNodeInfo(
            ln.NodeInfoRequest(pub_key=pub_key, include_channels=True)
        )
        json_obj = json.loads(
            MessageToJson(
                response,
                including_default_value_fields=True,
                preserving_proto_field_name=True,
                sort_keys=True,
            )
        )
        return dict2obj(json_obj)

    @lru_cache(maxsize=None)
    def get_node_channels_pubkeys(self, pub_key):
        node_info = self.get_node_info(pub_key)
        return [
            (c.node1_pub, c.node2_pub)[pub_key == c.node1_pub]
            for c in node_info.channels
        ]

    def get_own_pubkey(self):
        return self.get_info().identity_pubkey

    def generate_invoice(self, amount: int, memo: str = "Orb invoice"):
        invoice_request = ln.Invoice(memo=memo, value=amount, expiry=3600)
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

    @lru_cache(None)
    def decode_payment_request(self, payment_request):
        request = ln.PayReqString(pay_req=payment_request)
        j = json.loads(
            MessageToJson(
                self.stub.DecodePayReq(request),
                including_default_value_fields=True,
                preserving_proto_field_name=True,
                sort_keys=True,
            )
        )
        return dict2obj(j)

    def get_invoice_events(self):
        return self.stub.SubscribeInvoices(
            request=ln.InvoiceSubscription(add_index=None, settle_index=None)
        )

    def get_channels(self, active_only=False):
        from orb.misc.channel import Channel

        return [
            Channel(c)
            for c in self.stub.ListChannels(
                ln.ListChannelsRequest(active_only=active_only)
            ).channels
        ]

    def get_route(
        self,
        pub_key: str,
        amount_sat: int,
        ignored_pairs: list,
        ignored_nodes: list,
        last_hop_pubkey: Union[str, None],
        outgoing_chan_id: Union[str, None],
        fee_limit_msat: int,
        time_pref: float = 0.5,
        source_pub_key: Union[str, None] = None,
    ):
        if fee_limit_msat:
            fee_limit = {"fixed_msat": int(fee_limit_msat)}
        else:
            fee_limit = None
        if last_hop_pubkey:
            last_hop_pubkey = base64.b16decode(last_hop_pubkey, True)
        kwargs = dict(
            pub_key=pub_key,
            amt=amount_sat,
            ignored_pairs=ignored_pairs,
            fee_limit=fee_limit,
            ignored_nodes=ignored_nodes,
            use_mission_control=True,
        )
        if last_hop_pubkey:
            kwargs["last_hop_pubkey"] = last_hop_pubkey
        if outgoing_chan_id:
            kwargs["outgoing_chan_id"] = int(outgoing_chan_id)
        if self.get_version() >= "0.15.0":
            kwargs["time_pref"] = time_pref
        request = ln.QueryRoutesRequest(**kwargs)
        try:
            response = self.stub.QueryRoutes(request)
            return response.routes
        except:
            return []

    @cached(ttl=5)
    def get_edge(self, channel_id: str):
        json_obj = json.loads(
            MessageToJson(
                self.stub.GetChanInfo(ln.ChanInfoRequest(chan_id=int(channel_id))),
                including_default_value_fields=True,
                preserving_proto_field_name=True,
                sort_keys=True,
            )
        )
        obj = dict2obj(json_obj)
        return obj

    @cached(ttl=5)
    def get_policy_to(self, channel_id):
        edge = self.get_edge(channel_id)
        # node1_policy contains the fee base and rate for payments from node1 to node2
        if edge.node1_pub == self.get_own_pubkey():
            return edge.node1_policy
        return edge.node2_policy

    @cached(ttl=5)
    def get_policy_from(self, channel_id):
        edge = self.get_edge(channel_id)
        # node1_policy contains the fee base and rate for payments from node1 to node2
        if edge.node1_pub == self.get_own_pubkey():
            return edge.node2_policy
        return edge.node1_policy

    @cached(ttl=5)
    def get_ppm_to(self, channel_id):
        return self.get_policy_to(channel_id).fee_rate_milli_msat

    @cached(ttl=5)
    def get_ppm_from(self, channel_id):
        return self.get_policy_from(channel_id).fee_rate_milli_msat

    def send_payment(self, payment_request, route):
        last_hop = route.hops[-1]
        import base64 as b64

        last_hop.mpp_record.payment_addr = b64.b64decode(payment_request.payment_addr)
        last_hop.mpp_record.total_amt_msat = payment_request.num_msat
        request = lnrouter.SendToRouteRequest(route=route)
        request.payment_hash = self.hex_string_to_bytes(payment_request.payment_hash)
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
        tx, output = channel_point.split(":")
        cp = ln.ChannelPoint(funding_txid_str=tx, output_index=int(output))
        kwargs = dict(channel_point=cp, force=force)
        if not force:
            kwargs["sat_per_vbyte"] = sat_per_vbyte
        request = ln.CloseChannelRequest(**kwargs)
        return self.stub.CloseChannel(request)

    def new_address(self):
        request = ln.NewAddressRequest(type=0, account=None)
        response = self.stub.NewAddress(request)
        return response

    def connect(self, addr):
        pk, h = addr.split("@")
        ln_addr = ln.LightningAddress(pubkey=pk, host=h)
        request = ln.ConnectPeerRequest(addr=ln_addr, perm=False, timeout=10)
        response = self.stub.ConnectPeer(request)
        json_obj = json.loads(
            MessageToJson(
                response,
                including_default_value_fields=True,
                preserving_proto_field_name=True,
                sort_keys=True,
            )
        )
        return dict2obj(json_obj)

    def send_coins(self, addr: str, amount: int, sat_per_vbyte: int):
        return self.stub.SendCoins(
            ln.SendCoinsRequest(
                addr=addr, amount=int(amount), sat_per_vbyte=int(sat_per_vbyte)
            )
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
        for e in self.stub.SubscribeChannelEvents(request):
            json_obj = json.loads(
                MessageToJson(
                    e,
                    including_default_value_fields=True,
                    preserving_proto_field_name=True,
                    sort_keys=True,
                )
            )
            obj = dict2obj(json_obj)
            yield obj

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

    def list_payments(
        self, include_incomplete=True, index_offset=0, max_payments=100, reversed=False
    ):
        request = ln.ListPaymentsRequest(
            include_incomplete=include_incomplete,
            index_offset=index_offset,
            max_payments=max_payments,
            reversed=reversed,
        )
        response = self.stub.ListPayments(request)
        json_obj = json.loads(
            MessageToJson(
                response,
                including_default_value_fields=True,
                preserving_proto_field_name=True,
                sort_keys=True,
            )
        )
        return dict2obj(json_obj)

    def list_peers(self):
        response = self.stub.ListPeers(ln.ListPeersRequest())
        json_obj = json.loads(
            MessageToJson(
                response,
                including_default_value_fields=True,
                preserving_proto_field_name=True,
                sort_keys=True,
            )
        )
        return dict2obj(json_obj)

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

    def batch_open(self, pubkeys, amounts, sat_per_vbyte):
        chans = [
            dict(
                node_pubkey=base64.b16decode(pk, True),
                local_funding_amount=int(amount),
                push_sat=0,
                private=False,
                min_htlc_msat=1000,
            )
            for pk, amount in zip(pubkeys, amounts)
        ]
        return self.stub.BatchOpenChannel(
            ln.BatchOpenChannelRequest(
                sat_per_vbyte=sat_per_vbyte, spend_unconfirmed=False, channels=chans
            )
        )

    def htlc_interceptor(self, chan_id, htlc_id, action=1):
        key = lnrouterrpc.CircuitKey(chan_id=chan_id, htlc_id=htlc_id)

        def request_generator():
            while True:
                yield lnrouterrpc.ForwardHtlcInterceptResponse(
                    incoming_circuit_key=key, action=action
                )

        return self.router_stub.HtlcInterceptor(request_generator())

    def keysend(self, target_pubkey, msg, amount, fee_limit, timeout):
        import secrets
        from hashlib import sha256

        secret = secrets.token_bytes(32)
        hashed_secret = sha256(secret).hexdigest()
        custom_records = [
            (5482373484, secret),
        ]
        msg = str(msg)
        if len(msg) > 0:
            custom_records.append((34349334, bytes.fromhex(msg.encode("utf-8").hex())))
        for response in self.router_stub.SendPaymentV2(
            lnrouter.SendPaymentRequest(
                dest=bytes.fromhex(target_pubkey),
                dest_custom_records=custom_records,
                fee_limit_sat=fee_limit,
                timeout_seconds=timeout,
                amt=amount,
                payment_hash=bytes.fromhex(hashed_secret),
            )
        ):
            if response.status == 1:
                print("In-flight")
            if response.status == 2:
                print("Succeeded")
            if response.status == 3:
                if response.failure_reason == 1:
                    print("Failure - Timeout")
                elif response.failure_reason == 2:
                    print("Failure - No Route")
                elif response.failure_reason == 3:
                    print("Failure - Error")
                elif response.failure_reason == 4:
                    print("Failure - Incorrect Payment Details")
                elif response.failure_reason == 5:
                    print("Failure Insufficient Balance")
            if response.status == 0:
                print("Unknown Error")

    def describe_graph(self, include_unannounced=False):
        response = self.stub.DescribeGraph(
            ln.ChannelGraphRequest(
                include_unannounced=include_unannounced,
            )
        )
        json_obj = json.loads(
            MessageToJson(
                response,
                including_default_value_fields=True,
                preserving_proto_field_name=True,
                sort_keys=True,
            )
        )
        return json_obj
