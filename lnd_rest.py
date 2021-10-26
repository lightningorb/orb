from lnd_base import LndBase
from functools import lru_cache
import base64, json, requests
from kivy.app import App
import os
from munch import Munch
from ui_actions import console_output


class Lnd(LndBase):
    def __init__(self):
        app = App.get_running_app()
        data_dir = app.user_data_dir
        self.cert_path = os.path.join(data_dir, "tls.cert")
        self.hostname = app.config["lnd"]["hostname"]
        self.rest_port = app.config["lnd"]["rest_port"]
        macaroon = app.config["lnd"]["macaroon_admin"]
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

    @lru_cache(maxsize=None)
    def get_edge(self, channel_id):
        url = f"{self.fqdn}/v1/graph/edge/{channel_id}"
        r = requests.get(url, headers=self.headers, verify=self.cert_path)
        return Munch.fromDict(r.json())

    def get_policy_to(self, channel_id):

        edge = self.get_edge(channel_id)
        if edge.get("error"):
            print(edge.error)
            return None
        # node1_policy contains the fee base and rate for payments from node1 to node2
        if edge.node1_pub == self.get_own_pubkey():
            return Munch.fromDict(edge.node1_policy)
        return Munch.fromDict(edge.node2_policy)

    def get_policy_from(self, channel_id):
        edge = self.get_edge(channel_id)
        if edge.get("error"):
            print(edge.error)
            return None
        # node1_policy contains the fee base and rate for payments from node1 to node2
        if edge.node1_pub == self.get_own_pubkey():
            return Munch.fromDict(edge.node2_policy)
        return Munch.fromDict(edge.node1_policy)

    def get_own_pubkey(self):
        return self.get_info().identity_pubkey

    @lru_cache(maxsize=None)
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
        if fee_limit_msat:
            fee_limit = {"fixed_msat": int(fee_limit_msat)}
        else:
            fee_limit = None
        if last_hop_pubkey:
            last_hop_pubkey = base64.b16decode(last_hop_pubkey, True)
        url = f"{self.fqdn}/v1/graph/routes/{pub_key}/{amount}"
        r = requests.get(
            url,
            headers=self.headers,
            verify=self.cert_path,
            data=json.dumps(
                {
                    "amt": amount,
                    "last_hop_pubkey": last_hop_pubkey,
                    "fee_limit.fixed_msat": fee_limit_msat,
                    "ignored_nodes": [x["from"] for x in ignored_pairs],
                    "outgoing_chan_id": outgoing_chan_id,
                }
            ),
        )
        obj = r.json()
        return Munch.fromDict(obj).routes
        # request = ln.QueryRoutesRequest(
        #     pub_key=pub_key,
        #     last_hop_pubkey=last_hop_pubkey,
        #     outgoing_chan_id=outgoing_chan_id,
        #     amt=amount,
        #     ignored_pairs=ignored_pairs,
        #     fee_limit=fee_limit,
        #     ignored_nodes=ignored_nodes,
        #     use_mission_control=True,
        # )
        # try:
        #     response = self.stub.QueryRoutes(request)
        #     return response.routes
        # except:
        #     return None

    def send_payment(self, payment_request, route):
        last_hop = route.hops[-1]
        last_hop.mpp_record.payment_addr = payment_request.payment_addr
        last_hop.mpp_record.total_amt_msat = payment_request.num_msat
        request = lnrouter.SendToRouteRequest(route=route)
        request.payment_hash = self.hex_string_to_bytes(payment_request.payment_hash)
        result = []
        res = self.router_stub.SendToRouteV2(request)
        return res

    def get_htlc_events(self):
        url = f"{self.fqdn}/v2/router/htlcevents"
        return requests.get(url, headers=self.headers, verify=self.cert_path, stream=True)

    def get_channel_events(self):
        pass

    def get_forwarding_history(self, start_time=None, end_time=None, index_offset=0, num_max_events=100):
        data = dict(start_time=start_time, end_time=end_time, index_offset=index_offset, num_max_events=num_max_events)
        url = f"{self.fqdn}/v1/switch"
        r = requests.post(url, headers=self.headers, verify=self.cert_path, data=json.dumps(data))
        return Munch.fromDict(r.json())
