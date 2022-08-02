# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-15 07:15:28
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-08-01 17:08:30

from functools import lru_cache
import base64, json, requests, codecs

from orb.store.db_cache import aliases_cache
from orb.lnd.lnd_base import LndBase
from orb.misc.auto_obj import dict2obj, todict
from orb.misc.channel import Channel

from memoization import cached

decode_hex = codecs.getdecoder("hex_codec")
encode_pk = lambda PK: base64.urlsafe_b64encode(
    b"".join(decode_hex(PK[x : x + 2])[0] for x in range(0, len(PK), 2))
).decode()


class LndREST(LndBase):
    def __init__(self, tls_certificate, server, macaroon, port):
        self.cert_path = tls_certificate
        self.hostname = server
        self.rest_port = port
        self.headers = {
            "Grpc-Metadata-macaroon": macaroon.encode()
            if type(macaroon) is str
            else macaroon
        }
        self.version = None

    @property
    def fqdn(self):
        return f"https://{self.hostname}:{self.rest_port}"

    def get_balance(self):
        url = f"{self.fqdn}/v1/balance/blockchain"
        r = requests.get(url, headers=self.headers, verify=self.cert_path)
        return dict2obj(r.json())

    def channel_balance(self):
        url = f"{self.fqdn}/v1/balance/channels"
        r = requests.get(url, headers=self.headers, verify=self.cert_path)
        return dict2obj(r.json())

    def get_channels(self, active_only=False):
        url = f"{self.fqdn}/v1/channels"
        r = requests.get(
            url,
            headers=self.headers,
            verify=self.cert_path,
            data={"active_only": active_only},
        )
        return [Channel(dict2obj(c)) for c in r.json()["channels"]]

    def get_info(self):
        url = f"{self.fqdn}/v1/getinfo"
        r = requests.get(url, headers=self.headers, verify=self.cert_path)
        return dict2obj(r.json())

    @cached(ttl=5)
    def get_edge(self, channel_id):
        url = f"{self.fqdn}/v1/graph/edge/{channel_id}"
        r = requests.get(url, headers=self.headers, verify=self.cert_path)
        return dict2obj(r.json())

    @cached(ttl=5)
    def get_policy_to(self, channel_id):

        edge = self.get_edge(channel_id)
        if edge.get("code", 0) == 3:
            print(edge.message)
            return None
        if edge.get("error"):
            print(edge.error)
            return None
        # node1_policy contains the fee base and rate for payments from node1 to node2
        if edge.node1_pub == self.get_own_pubkey():
            return edge.node1_policy
        return edge.node2_policy

    @cached(ttl=5)
    def get_policy_from(self, channel_id):
        edge = self.get_edge(channel_id)
        if edge.get("code", 0) == 3:
            print(edge.message)
            return None
        if edge.get("error"):
            print(edge.error)
            return None
        # node1_policy contains the fee base and rate for payments from node1 to node2
        if edge.node1_pub == self.get_own_pubkey():
            return edge.node2_policy
        return edge.node1_policy

    def get_own_pubkey(self):
        return self.get_info().identity_pubkey

    @aliases_cache
    def get_node_alias(self, pub_key):
        url = f"{self.fqdn}/v1/graph/node/{pub_key}"
        r = requests.get(url, headers=self.headers, verify=self.cert_path)
        res = r.json()
        if res.get("code") == 5:
            print(res["message"])
        return dict2obj(r.json()).node.alias

    @lru_cache(maxsize=None)
    def get_node_info(self, pub_key):
        return self.__get(f"/v1/graph/node/{pub_key}")

    def fee_report(self):
        url = f"{self.fqdn}/v1/fees"
        r = requests.get(url, headers=self.headers, verify=self.cert_path)
        return dict2obj(r.json())

    def decode_payment_request(self, payment_request):
        url = f"{self.fqdn}/v1/payreq/{payment_request}"
        r = requests.get(url, headers=self.headers, verify=self.cert_path)
        return dict2obj(r.json())

    def decode_request(self, payment_request):
        url = f"{self.fqdn}/v1/payreq/{payment_request}"
        r = requests.get(url, headers=self.headers, verify=self.cert_path)
        return dict2obj(r.json())

    def get_route(
        self,
        pub_key,
        amount,
        ignored_pairs,
        ignored_nodes,
        last_hop_pubkey,
        outgoing_chan_id,
        fee_limit_msat,
        time_pref=0.5,
    ):
        """
        https://github.com/lightningnetwork/lnd/issues/6133
        """
        url = f"{self.fqdn}/v1/graph/routes/{pub_key}/{amount}?use_mission_control=true&fee_limit.fixed_msat={int(fee_limit_msat)}&outgoing_chan_id={outgoing_chan_id}"
        if self.get_version() >= "0.15.0":
            url += f"&time_pref={time_pref}"
        if last_hop_pubkey:
            print(last_hop_pubkey)
            last_hop_pubkey = encode_pk(last_hop_pubkey)
            url += f"&last_hop_pubkey={last_hop_pubkey}"
        if ignored_pairs:
            # todo: encoding isn't correct, but mission control knows
            # what to do even without the ignored nodes
            pass
            # print([x["from"] for x in ignored_pairs])
            # ignored = ",".join([x["from"].decode() for x in ignored_pairs])
            #     url += f"&ignored_nodes={ignored}"
        r = requests.get(url, headers=self.headers, verify=self.cert_path)
        return dict2obj(r.json()).get("routes")

    def send_payment(self, payment_request, route):
        """
        SendToRouteV2 attempts to make a payment via the specified route.
        This method differs from SendPayment in that it allows users to
        specify a full route manually. This can be used for things like
        rebalancing, and atomic swaps.
        """
        last_hop = route.hops[-1]
        last_hop.mpp_record = dict2obj(
            dict(
                payment_addr=payment_request.payment_addr,
                total_amt_msat=payment_request.num_msat,
            )
        )
        url = f"{self.fqdn}/v2/router/route/send"
        pbytes = self.hex_string_to_bytes(payment_request.payment_hash)
        data = {"payment_hash": base64.b64encode(pbytes).decode(), "route": route}
        jdata = json.dumps(todict(data))
        r = requests.post(url, data=jdata, headers=self.headers, verify=self.cert_path)
        return dict2obj(r.json())

    def router_send(
        self,
        pub_key,
        amount,
        payment_request,
        last_hop_pubkey,
        outgoing_chan_id,
        fee_limit_msat,
        payment_request_raw,
    ):
        """
        SendPaymentV2 attempts to route a payment described
        by the passed PaymentRequest to the final destination.
        The call returns a stream of payment updates.

        Does not allow for self-payment.
        """
        url = f"{self.fqdn}/v2/router/send"
        data = {
            "payment_request": payment_request_raw,
            "timeout_seconds": 120,
            "fee_limit_msat": int(fee_limit_msat),
            "outgoing_chan_id": outgoing_chan_id,
        }
        r = requests.post(
            url,
            headers=self.headers,
            verify=self.cert_path,
            stream=True,
            data=json.dumps(data),
        )
        return r

    def get_htlc_events(self):
        url = f"{self.fqdn}/v2/router/htlcevents"
        for event in requests.get(
            url, headers=self.headers, verify=self.cert_path, stream=True
        ).iter_lines():
            j = json.loads(event)
            if "result" in j:
                yield dict2obj(j["result"])

    def get_invoice_events(self):
        url = f"{self.fqdn}/v1/invoices/subscribe"
        for event in requests.get(
            url, headers=self.headers, verify=self.cert_path, stream=True
        ).iter_lines():
            j = json.loads(event)
            if "result" in j:
                yield dict2obj(j["result"])

    def get_channel_events(self):
        url = f"{self.fqdn}/v1/channels/subscribe"
        r = requests.get(url, headers=self.headers, verify=self.cert_path, stream=True)
        for l in r.iter_lines():
            j = json.loads(l.decode())
            j = dict2obj(j)
            if hasattr(j, "result"):
                yield j.result

    def get_forwarding_history(
        self, start_time=None, end_time=None, index_offset=0, num_max_events=100
    ):
        data = dict(
            start_time=start_time,
            end_time=end_time,
            index_offset=index_offset,
            num_max_events=num_max_events,
        )
        url = f"{self.fqdn}/v1/switch"
        r = requests.post(
            url, headers=self.headers, verify=self.cert_path, data=json.dumps(data)
        )
        return dict2obj(r.json())

    def get_pending_channels(self):
        url = f"{self.fqdn}/v1/channels/pending"
        r = requests.get(url, headers=self.headers, verify=self.cert_path)
        return dict2obj(r.json())

    def update_channel_policy(self, channel, *args, **kwargs):
        tx, output = channel.channel_point.split(":")
        kwargs.update(dict(chan_point=dict(funding_txid_str=tx, output_index=output)))
        if kwargs.get("base_fee_msat") is not None:
            kwargs["base_fee_msat"] = str(kwargs["base_fee_msat"])
        return self.__post(url=f"/v1/chanpolicy", data=kwargs)

    def list_invoices(self):
        url = f"{self.fqdn}/v1/invoices"
        r = requests.get(
            url,
            headers=self.headers,
            verify=self.cert_path,
            data=json.dumps(dict(reversed=True, num_max_invoices="100")),
        )
        return dict2obj(r.json())

    def generate_invoice(self, memo, amount):
        url = f"{self.fqdn}/v1/invoices"
        data = dict(memo=memo, value=amount, expiry=3600)
        r = requests.post(
            url, headers=self.headers, verify=self.cert_path, data=json.dumps(data)
        )
        add_invoice_response = dict2obj(r.json())
        return add_invoice_response.payment_request, self.decode_payment_request(
            add_invoice_response.payment_request
        )

    def new_address(self):
        """
        lncli: newaddress NewAddress creates a new address
        under control of the local wallet.
        """
        return self.__get("/v1/newaddress")

    def open_channel(self, node_pubkey_string, sat_per_vbyte, amount_sat):
        """
        OpenChannelSync is a synchronous version of the OpenChannel
        RPC call. This call is meant to be consumed by clients to
        the REST proxy. As with all other sync calls, all byte
        slices are intended to be populated as hex encoded strings.
        """
        url = f"/v1/channels"
        data = dict(
            sat_per_vbyte=int(sat_per_vbyte),
            node_pubkey_string=node_pubkey_string,
            local_funding_amount=int(amount_sat),
            push_sat=0,
            private=False,
            spend_unconfirmed=False,
        )
        return self.__post(url=url, data=data)

    def send_coins(self, addr, amount, sat_per_vbyte):
        """
        lncli: sendcoins SendCoins executes a request to send coins
        to a particular address. Unlike SendMany, this RPC call
        only allows creating a single output at a time. If
        neither target_conf, or sat_per_vbyte are set, then
        the internal wallet will consult its fee model to
        determine a fee for the default confirmation target.
        """
        url = f"/v1/transactions"
        data = {
            "addr": addr,  # The address to send coins to
            "amount": amount,  # The amount in satoshis to send
            "sat_per_vbyte": sat_per_vbyte,  # A manual fee rate set in sat/vbyte that should be used when crafting the transaction.
        }
        return self.__post(url, data=data)

    def sign_message(self, msg):
        """
        SignMessage signs a message with the key specified in
        the key locator. The returned signature is fixed-size
        LN wire format encoded.

        The main difference to SignMessage in the main RPC is
        that a specific key is used to sign the message instead
        of the node identity private key.
        """
        return self.__post(
            f"/v1/signmessage", data=dict(msg=base64.b64encode(msg.encode()).decode())
        ).signature

    def keysend(self, target_pubkey, msg, amount, fee_limit, timeout):
        import secrets
        from hashlib import sha256

        secret = secrets.token_bytes(32)
        hashed_secret = sha256(secret).digest()
        custom_records = {5482373484: base64.b64encode(secret).decode()}
        msg = str(msg)
        if len(msg) > 0:
            custom_records[34349334] = base64.b64encode(msg.encode("utf-8")).decode()

        data = {
            "amt": amount,
            "dest": encode_pk(target_pubkey),
            "timeout_seconds": timeout,
            "dest_custom_records": custom_records,
            "fee_limit_sat": fee_limit,
            "payment_hash": base64.b64encode(hashed_secret).decode(),
        }

        jdata = json.dumps(data)

        r = requests.post(
            f"{self.fqdn}/v2/router/send",
            headers=self.headers,
            verify=self.cert_path,
            stream=True,
            data=jdata,
        )

        for raw_response in r.iter_lines():
            json_data = json.loads(raw_response)
            if json_data.get("error"):
                print(json_data["error"])
                break
            response = dict2obj(json_data)
            print(response.status)
            if response.status == "FAILED":
                print(response.failure_reason)

    def list_peers(self):
        """
        Return list of peers
        """
        return self.__get("/v1/peers")

    def connect(self, addr):
        """
        lncli: connect ConnectPeer attempts to establish a connection
        to a remote peer. This is at the networking level, and is
        used for communication between nodes. This is distinct from
        establishing a channel with a peer.

        Lnd().connect(address) gives an error in REST.. strangely
        it connects successfully, and the error can be ignored.
        """
        pk, host = addr.split("@")
        return self.__post(
            "/v1/peers",
            data={"addr": dict(pubkey=pk, host=host), "perm": True, "timeout": "30"},
        )

    def close_channel(self, channel_point: str, force: bool, sat_per_vbyte: int):
        tx, output = channel_point.split(":")
        url = f"{self.fqdn}/v1/channels/{tx}/{output}"
        query = ""
        if force:
            query = f"force={int(force)}"
        else:
            query = f"sat_per_vbyte={int(force)}"
        url += f"?{query}"
        print(url)
        r = requests.delete(
            url, headers=self.headers, verify=self.cert_path, stream=True
        )
        return r.iter_lines()

    def list_payments(
        self, include_incomplete=True, index_offset=0, max_payments=100, reversed=False
    ):
        url = f"/v1/payments?include_incomplete={'true' if include_incomplete else 'false'}&index_offset={index_offset}&max_payments={max_payments}"
        return self.__get(url)

    def batch_open(self, pubkeys, amounts, sat_per_vbyte):
        """
        lncli: batchopenchannel BatchOpenChannel attempts to open multiple
        single-funded channels in a single transaction in an atomic way.
        This means either all channel open requests succeed at once or all
        attempts are aborted if any of them fail. This is the safer
        variant of using PSBTs to manually fund a batch of channels through
        the OpenChannel RPC.
        """
        chans = [
            dict(
                node_pubkey=encode_pk(pk),
                local_funding_amount=str(int(amount)),
                push_sat=0,
                private=False,
                min_htlc_msat=1000,
            )
            for pk, amount in zip(pubkeys, amounts)
        ]
        data = {
            "channels": chans,
            "sat_per_vbyte": str(sat_per_vbyte),
            "spend_unconfirmed": False,
        }
        return self.__post(url="/v1/channels/batch", data=data)

    def __get(self, url):
        """
        Simplify get requests.

        url should NOT including the FQDN.
        data should NOT be json encoded.

        returns an autoobj
        """
        full_url = f"{self.fqdn}{url}"
        r = requests.get(full_url, headers=self.headers, verify=self.cert_path)
        j = r.json()
        o = dict2obj(j)
        return o

    def __post(self, url, data):
        """
        Simplify posts requests.

        url should NOT including the FQDN.
        data should NOT be json encoded.

        returns an autoobj
        """
        full_url = f"{self.fqdn}{url}"
        jdata = json.dumps(todict(data))
        r = requests.post(
            full_url, headers=self.headers, verify=self.cert_path, data=jdata
        )
        j = r.json()
        return dict2obj(j)
