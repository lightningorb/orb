# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-15 07:15:28
# @Last Modified by:   lnorb.com
# @Last Modified time: 2021-12-31 05:17:33
from orb.store.db_cache import aliases_cache
from orb.lnd.lnd_base import LndBase
from functools import lru_cache
import base64, json, requests
from munch import Munch


class LndREST(LndBase):
    def __init__(self, tls_certificate, server, network, macaroon, port):
        self.cert_path = tls_certificate
        self.hostname = server
        self.rest_port = port
        self.headers = {"Grpc-Metadata-macaroon": macaroon.encode()}

    @property
    def fqdn(self):
        return f"https://{self.hostname}:{self.rest_port}"

    def get_balance(self):
        url = f"{self.fqdn}/v1/balance/blockchain"
        r = requests.get(url, headers=self.headers, verify=self.cert_path)
        return Munch.fromDict(r.json())

    def channel_balance(self):
        url = f"{self.fqdn}/v1/balance/channels"
        r = requests.get(url, headers=self.headers, verify=self.cert_path)
        return Munch.fromDict(r.json())

    def get_channels(self, active_only=False):
        url = f"{self.fqdn}/v1/channels"
        r = requests.get(
            url,
            headers=self.headers,
            verify=self.cert_path,
            data={"active_only": active_only},
        )
        return Munch.fromDict(r.json()).channels

    @lru_cache(maxsize=None)
    def get_info(self):
        url = f"{self.fqdn}/v1/getinfo"
        r = requests.get(url, headers=self.headers, verify=self.cert_path)
        return Munch.fromDict(r.json())

    def get_edge(self, channel_id):
        url = f"{self.fqdn}/v1/graph/edge/{channel_id}"
        r = requests.get(url, headers=self.headers, verify=self.cert_path)
        return Munch.fromDict(r.json())

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
            return Munch.fromDict(edge.node1_policy)
        return Munch.fromDict(edge.node2_policy)

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
            return Munch.fromDict(edge.node2_policy)
        return Munch.fromDict(edge.node1_policy)

    def get_own_pubkey(self):
        return self.get_info().identity_pubkey

    @aliases_cache
    def get_node_alias(self, pub_key):
        url = f"{self.fqdn}/v1/graph/node/{pub_key}"
        r = requests.get(url, headers=self.headers, verify=self.cert_path)
        return Munch.fromDict(r.json()).node.alias

    def fee_report(self):
        url = f"{self.fqdn}/v1/fees"
        r = requests.get(url, headers=self.headers, verify=self.cert_path)
        return Munch.fromDict(r.json())

    def decode_payment_request(self, payment_request):
        url = f"{self.fqdn}/v1/payreq/{payment_request}"
        r = requests.get(url, headers=self.headers, verify=self.cert_path)
        return Munch.fromDict(r.json())

    def decode_request(self, payment_request):
        url = f"{self.fqdn}/v1/payreq/{payment_request}"
        r = requests.get(url, headers=self.headers, verify=self.cert_path)
        return Munch.fromDict(r.json())

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
        if last_hop_pubkey:
            last_hop_pubkey = base64.b16decode(last_hop_pubkey, True)
        url = f"{self.fqdn}/v1/graph/routes/{pub_key}/{amount}"
        exit()
        r = requests.get(
            url,
            headers=self.headers,
            verify=self.cert_path,
            data=json.dumps(
                {
                    "use_mission_control": True,
                    "last_hop_pubkey": last_hop_pubkey,
                    "fee_limit.fixed_msat": fee_limit_msat,
                    "ignored_nodes": [x["from"] for x in ignored_pairs],
                    "outgoing_chan_id": int(outgoing_chan_id),
                }
            ),
        )
        obj = r.json()
        return Munch.fromDict(obj).routes

    def send_payment(self, payment_request, route):
        last_hop = route.hops[-1]
        last_hop.mpp_record = Munch.fromDict(
            dict(
                payment_addr=payment_request.payment_addr,
                total_amt_msat=payment_request.num_msat,
            )
        )
        url = f"{self.fqdn}/v2/router/route/send"
        pbytes = self.hex_string_to_bytes(payment_request.payment_hash)
        data = {"payment_hash": base64.b64encode(pbytes).decode(), "route": route}
        r = requests.post(
            url, data=json.dumps(data), headers=self.headers, verify=self.cert_path
        )
        return Munch.fromDict(r.json())

    def get_htlc_events(self):
        url = f"{self.fqdn}/v2/router/htlcevents"
        return requests.get(
            url, headers=self.headers, verify=self.cert_path, stream=True
        ).iter_lines()

    def get_channel_events(self):
        pass

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
        return Munch.fromDict(r.json())

    def get_pending_channels(self):
        url = f"{self.fqdn}/v1/channels/pending"
        r = requests.get(url, headers=self.headers, verify=self.cert_path)
        return Munch.fromDict(r.json())

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

    def update_channel_policy(self, channel, *args, **kwargs):
        tx, output = channel.channel_point.split(":")
        url = f"{self.fqdn}/v1/chanpolicy"
        kwargs.update(dict(chan_point=dict(funding_txid_str=tx, output_index=output)))
        kwargs["global"] = False
        kwargs["base_fee_msat"] = str(kwargs["base_fee_msat"])
        r = requests.post(
            url, headers=self.headers, verify=self.cert_path, data=json.dumps(kwargs)
        )
        return Munch.fromDict(r.json())
