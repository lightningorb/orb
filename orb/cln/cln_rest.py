# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-15 07:15:28
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-09-19 08:32:32

from typing import Union

import base64, json, requests, codecs
from urllib.parse import urlencode

from orb.cln.cln_base import ClnBase
from orb.misc.auto_obj import dict2obj
from orb.store.db_cache import aliases_cache

from memoization import cached

decode_hex = codecs.getdecoder("hex_codec")
encode_pk = lambda PK: base64.urlsafe_b64encode(
    b"".join(decode_hex(PK[x : x + 2])[0] for x in range(0, len(PK), 2))
).decode()


class ClnREST(ClnBase):
    def __init__(self, tls_certificate, server, macaroon, port):
        super(ClnREST, self).__init__(protocol="rest")
        self.cert_path = tls_certificate
        self.hostname = server
        self.rest_port = port
        self.headers = {
            "macaroon": macaroon.encode() if type(macaroon) is str else macaroon,
            "encodingtype": "hex",
            "Content-Type": "application/json",
        }
        self.version = None

    @property
    def fqdn(self):
        return (
            f"http{['', 's'][bool(self.cert_path)]}://{self.hostname}:{self.rest_port}"
        )

    def get_balance(self):
        """
        Conversion done.
        """
        return self._get("/v1/getBalance")

    def local_remote_bal(self):
        """
        Conversion done.
        """
        return self._get("/v1/channel/localRemoteBal")

    def get_node_info(self, pubkey: str):
        """
        Conversion done.
        """
        url = f"{self.fqdn}/v1/network/listNode/{pubkey}"
        r = requests.get(url, headers=self.headers, verify=self.cert_path)
        return dict2obj(r.json()[0])

    @cached(ttl=5)
    def list_channel(self, shortchannelid: str):
        """
        Conversion done.
        """
        url = f"{self.fqdn}/v1/network/listChannel/{shortchannelid}"
        r = requests.get(url, headers=self.headers, verify=self.cert_path)
        return dict2obj(r.json())

    def channel_balance(self):
        url = f"{self.fqdn}/v1/balance/channels"
        r = requests.get(url, headers=self.headers, verify=self.cert_path)
        return dict2obj(r.json())

    def get_channels(self):
        """
        Conversion Done
        """
        peers = self.listpeers()

        ret = []
        for p in peers.peers:
            for c in p.channels:
                if c.state != "CHANNELD_NORMAL":
                    continue
                c.remote_pubkey = p.id
                ret.append(c)
        return ret

    def get_info(self):
        """
        Conversion done
        """
        return self._get(f"/v1/getinfo")

    def rpc(self, method: str, **kwargs):
        for k, v in list(kwargs.items()):
            if v is None:
                del kwargs[k]
        return self._post("/v1/rpc", {"method": method, "params": kwargs})

    @cached(ttl=5)
    def get_policy_to(self, channel_id):
        """
        Conversion done
        """
        edge = self.list_channel(channel_id)
        # node1_policy contains the fee base and rate for payments from node1 to node2
        if edge["0"].source == self.get_own_pubkey():
            return edge["0"]
        return edge["1"]

    @cached(ttl=5)
    def get_policy_from(self, channel_id):
        """
        Conversion done
        """
        edge = self.list_channel(channel_id)
        # node1_policy contains the fee base and rate for payments from node1 to node2
        if edge["0"].source == self.get_own_pubkey():
            return edge["1"]
        return edge["0"]

    def get_own_pubkey(self):
        return self.get_info().id

    @aliases_cache
    def get_node_alias(self, pub_key):
        res = self.get_node_info(pub_key)
        if not hasattr(res, "alias"):
            return res.nodeid[:10]
        else:
            return res.alias

    def fee_report(self):
        url = f"{self.fqdn}/v1/fees"
        r = requests.get(url, headers=self.headers, verify=self.cert_path)
        return dict2obj(r.json())

    def decode_payment_request(self, payment_request):
        """
        Conversion Done.
        """
        return self._get(f"/v1/pay/decodePay/{payment_request}")

    def send_payment(self, payment_request, route):
        sp = self.sendpay(
            route=route["route"],
            payment_hash=payment_request.payment_hash,
            payment_secret=payment_request.payment_secret,
        )
        wsp = self.waitsendpay(payment_hash=payment_request.payment_hash)
        return wsp

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
        from threading import Thread, Condition
        from orb.misc.utils_no_kivy import pref

        protocol = pref("c-lightning-events.protocol")
        hostname = pref("c-lightning-events.hostname")
        port = int(pref("c-lightning-events.port"))
        fqdn = f"{protocol}://{hostname}:{port}"

        self.cv = Condition()
        self.message = None

        def run(*_):
            import websocket

            def on_message(_, message):
                with self.cv:
                    message = dict2obj(json.loads(message))
                    key = next(iter(message.todict().keys()))
                    if key in ["warning"]:
                        return
                    self.message = message
                    self.cv.notifyAll()

            def on_close(*_):
                with self.cv:
                    self.message = None
                    self.cv.notifyAll()

            ws = websocket.WebSocketApp(
                fqdn,
                on_message=on_message,
                on_close=on_close,
            )

            ws.run_forever()

        Thread(target=run).start()

        while True:
            with self.cv:
                self.cv.wait()
                if self.message:
                    yield self.message
                else:
                    raise Exception("Websocket closed")

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

    def get_forwarding_history(self, index_offset=0, num_max_events=100):
        r = self._get(
            f"/v1/channel/listForwardsPaginated?status=settled&offset={index_offset}&maxLen={num_max_events}&sort_by=resolved_time"
        )
        if index_offset >= r.totalForwards:
            return dict2obj(
                dict(listForwards=[], maxLen=0, offset=0, status=0, totalForwards=0)
            )
        for i in range(1, len(r.listForwards)):
            if (
                not r.listForwards[i - 1].resolved_time
                <= r.listForwards[i].resolved_time
            ):
                raise Exception(
                    "Events need to be sorted - please use the latest version of c-lightning-REST"
                )
        return r

    def get_pending_channels(self):
        url = f"{self.fqdn}/v1/channels/pending"
        r = requests.get(url, headers=self.headers, verify=self.cert_path)
        return dict2obj(r.json())

    def set_channel_fee(self, channel, *args, **kwargs):
        """
        Conversion done.
        """
        return self._post(
            url=f"/v1/channel/setChannelFee",
            data=dict(
                id=channel.chan_id,
                base=kwargs["base_fee_msat"],
                ppm=int(kwargs["fee_rate"] * 1e6),
            ),
        )

    def list_invoices(self):
        url = f"{self.fqdn}/v1/invoices"
        r = requests.get(
            url,
            headers=self.headers,
            verify=self.cert_path,
            data=json.dumps(dict(reversed=True, num_max_invoices="100")),
        )
        return dict2obj(r.json())

    def generate_invoice(self, amount: int, memo: str = "Orb invoice"):
        label = None
        if not label:
            from uuid import uuid4

            label = str(uuid4())
        data = dict(label=label, description=memo, amount=amount * 1000, expiry=3600)
        r = self._post("/v1/invoice/genInvoice", data=data)
        if hasattr(r, "warning_deadends"):
            print(r.warning_deadends)

        return r.bolt11, self.decode_payment_request(r.bolt11)

    def new_address(self):
        """
        Conversion done.
        """
        return self._get("/v1/newaddr")

    def open_channel(
        self, node_pubkey_string: str, amount_sat: int, sat_per_vbyte: float
    ):
        """
        Conversion done.
        """
        # rates = self.feerates(style="perkb")
        # min_acc = rates.perkb.min_acceptable
        # if sat_per_vbyte * 1000 < min_acc:
        # raise Exception(f"Min acceptable fee-rate: {min_acc}perkb")
        return self.fundchannel(
            id=node_pubkey_string,
            amount=int(amount_sat),
            feerate="urgent",  # , feerate=sat_per_vbyte * 1000
        )

    def send_coins(
        self, addr: str, satoshi: int, sat_per_vbyte: int, send_all: bool = False
    ):
        assert type(addr) is str
        assert type(satoshi) is int
        assert type(sat_per_vbyte) is int
        assert type(send_all) is bool
        if type(sat_per_vbyte) is int:
            feerate = f"{sat_per_vbyte*1000}perkb"
        if send_all:
            kwargs = dict(destination=addr, satoshi="all")
            kwargs["feerate"] = "normal"
            # kwargs["feerate"] = feerate
            return self.withdraw(**kwargs)
        else:
            # if this throws an exception, then good
            outputs, change = self.select_outputs_for_amount(satoshi)
            if not outputs:
                raise Exception("insufficient funds available to construct transaction")
            utxos = [f"{o.tx_hash}:{o.tx_index}" for o in outputs]
            kwargs = dict(destination=addr, satoshi=satoshi, utxos=utxos)
            # kwargs["feerate"] = feerate
            kwargs["feerate"] = "normal"
            return self.withdraw(**kwargs)

    def sign_message(self, msg):
        """
        SignMessage signs a message with the key specified in
        the key locator. The returned signature is fixed-size
        LN wire format encoded.

        The main difference to SignMessage in the main RPC is
        that a specific key is used to sign the message instead
        of the node identity private key.
        """
        return self._post(
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
        return self.listpeers()

    def connect(self, id):
        """
        lncli: connect ConnectPeer attempts to establish a connection
        to a remote peer. This is at the networking level, and is
        used for communication between nodes. This is distinct from
        establishing a channel with a peer.
        """
        return self._post("/v1/peer/connect", data=dict(id=id))

    def close_channel(
        self,
        id: str,
        unilateral_timeout: int = 172800,
        dest: str = "",
        fee_negotiation_step: str = "50%",
    ):
        params = dict(
            unilateralTimeout=unilateral_timeout,
            feeNegotiationStep=fee_negotiation_step,
        )
        if dest:
            params["dest"] = dest
        params_encoded = urlencode(params)
        url = f"{self.fqdn}/v1/channel/closeChannel/{id}?{params_encoded}"
        print(url)
        r = requests.delete(url, headers=self.headers, verify=self.cert_path)
        print(r)
        return dict2obj(r.json())

    @cached(ttl=60)
    def listsendpays_cached(self):
        return self.listsendpays(status="complete")

    def list_payments(self, index_offset=0, max_payments=100):
        pay = self.listsendpays_cached()
        return pay.payments[index_offset : index_offset + max_payments]

    def batch_open(self, pubkeys, amounts, sat_per_vbyte):
        """
        https://lightning.readthedocs.io/lightning-multifundchannel.7.html
        The multifundchannel RPC command opens multiple payment
        channels with nodes by committing a single funding transaction
        to the blockchain that is shared by all channels.
        """
        chans = [
            dict(
                id=pk,
                amount=str(int(amount)),
            )
            for pk, amount in zip(pubkeys, amounts)
        ]
        return self.multifundchannel(
            destinations=chans, feerate="urgent", minchannels=10
        )

    def _get(self, url):
        """
        Simplify get requests.

        url should NOT including the FQDN.
        data should NOT be json encoded.

        returns an autoobj
        """
        full_url = f"{self.fqdn}{url}"
        r = requests.get(full_url, headers=self.headers, verify=self.cert_path)
        if r.status_code != 200:
            print(f"Status Code: {r.status_code}")
        j = r.json()
        o = dict2obj(j)
        return o

    def _post(self, url, data):
        """
        Simplify posts requests.

        url should NOT including the FQDN.
        data should NOT be json encoded.

        returns an autoobj
        """
        full_url = f"{self.fqdn}{url}"
        r = requests.post(
            full_url, headers=self.headers, verify=self.cert_path, data=json.dumps(data)
        )
        j = r.json()
        return dict2obj(j)

    def __getattr__(self, name):
        return lambda **kwargs: self.rpc(name, **kwargs)
