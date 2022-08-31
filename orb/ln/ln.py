# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-08-06 13:35:10
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-08-31 10:10:42

from configparser import ConfigParser

from pathlib import Path
from orb.lnd.lnd import Lnd
from orb.cln.cln import Cln
from orb.ln.types import *
from orb.app import App


class ResultType:
    intersection = 0
    original = 1


class Ln:
    def __init__(self, node_type=None, **kwargs):
        if not node_type:
            from orb.misc.utils_no_kivy import pref

            node_type = pref("host.type")
        self.node_type = node_type
        self.concrete = {"lnd": Lnd, "cln": Cln}[node_type](**kwargs)

    def get_info(self):
        return Info(impl=self.node_type, **self.concrete.get_info().__dict__)

    def get_node_info(self, pubkey):
        return NodeInfo(
            impl=self.node_type, **self.concrete.get_node_info(pubkey).__dict__
        )

    def get_balance(self):
        return Balance(impl=self.node_type, **self.concrete.get_balance().__dict__)

    def list_peers(self):
        return Peers(impl=self.node_type, response=self.concrete.list_peers())

    def local_remote_bal(self):
        if self.node_type == "cln":
            return LocalRemoteBal(
                impl=self.node_type, **self.concrete.local_remote_bal().__dict__
            )
        elif self.node_type == "lnd":
            channel_bal = Lnd().channel_balance()
            return LocalRemoteBal(
                impl=self.node_type,
                local_balance=channel_bal.local_balance.sat,
                remote_balance=channel_bal.remote_balance.sat,
                pending_balance=channel_bal.unsettled_local_balance.sat
                + channel_bal.unsettled_remote_balance.sat,
                inactive_balance=0,
            )

    def get_route(
        self,
        fee_limit_msat=None,
        pub_key=None,
        outgoing_chan_id=None,
        source_pub_key=None,
        ignored_nodes=[],
        ignored_pairs=[],
        last_hop_pubkey=None,
        amount_sat=None,
        time_pref=None,
        cltv=0,
        **kwargs,
    ):
        if self.node_type == "cln":
            exclude = ignored_nodes[:]
            if outgoing_chan_id:
                app = App.get_running_app()
                for c in app.channels.channels.values():
                    if c.chan_id == outgoing_chan_id:
                        continue
                    direction = int(app.pubkey > c.remote_pubkey)
                    chan_id = f"{c.chan_id}/{direction}"
                    exclude.append(chan_id)

            route = self.concrete.getroute(
                fromid=source_pub_key,
                id=pub_key,
                exclude=exclude,
                msatoshi=amount_sat * 1000,
                riskfactor=0,
                cltv=cltv,
                **kwargs,
            )
        elif self.node_type == "lnd":
            route = next(
                iter(
                    self.concrete.get_route(
                        pub_key=pub_key,
                        source_pub_key=source_pub_key,
                        fee_limit_msat=fee_limit_msat,
                        ignored_nodes=ignored_nodes,
                        ignored_pairs=ignored_pairs,
                        outgoing_chan_id=outgoing_chan_id,
                        amount_sat=amount_sat,
                        last_hop_pubkey=last_hop_pubkey,
                        time_pref=time_pref,
                        **kwargs,
                    )
                ),
                None,
            )

        route = Route(impl=self.node_type, total_amt=amount_sat, route=route)

        if route.total_fees_msat > fee_limit_msat:
            route.hops = []

        return route

    def get_policy_to(self, channel):
        return Policy(
            self.node_type, **self.concrete.get_policy_to(channel.chan_id).__dict__
        )

    def update_channel_policy(self, channel, *args, **kwargs):
        if self.node_type == "cln":
            return self.concrete.set_channel_fee(channel, channel, *args, **kwargs)
        elif self.node_type == "lnd":
            return self.concrete.update_channel_policy(
                channel, channel, *args, **kwargs
            )

    def decode_payment_request(
        self, *args, result_type=ResultType.intersection, **kwargs
    ):
        res = self.concrete.decode_payment_request(*args, **kwargs)
        if result_type == ResultType.intersection:
            return PaymentRequest(
                impl=self.node_type,
                **res.__dict__,
            )
        else:
            return res

    def send_coins(
        self, addr: str, satoshi: int, sat_per_vbyte: int, send_all: bool = False
    ):
        res = self.concrete.send_coins(
            addr=addr, satoshi=satoshi, sat_per_vbyte=sat_per_vbyte, send_all=send_all
        )
        return ChainTransaction(impl=self.node_type, tx=res)

    def send_payment(self, payment_request, route):
        res = self.concrete.send_payment(payment_request, route)
        return SendPaymentResponse(self.node_type, res)

    def get_forwarding_history(
        self, start_time=None, end_time=None, index_offset=0, num_max_events=100
    ):
        res = self.concrete.get_forwarding_history(
            start_time=start_time,
            end_time=end_time,
            index_offset=index_offset,
            num_max_events=num_max_events,
        )

        return ForwardingEvents(impl=self.node_type, fwd=res)

    def get_htlc_events(self, sim=False):
        for e in self.concrete.get_htlc_events():
            yield HTLC(self.node_type, e)

    def __getattr__(self, name):
        return lambda *args, **kwargs: getattr(self.concrete, name)(*args, **kwargs)


from orb.misc.utils_no_kivy import _get_user_data_dir_static


def factory(pk: str) -> Ln:
    lnd_conf = ConfigParser()
    lnd_conf.read(
        (Path(_get_user_data_dir_static()) / f"orb_{pk}/orb_{pk}.ini").as_posix()
    )
    return Ln(
        node_type=lnd_conf.get("host", "type"),
        fallback_to_mock=False,
        cache=False,
        use_prefs=False,
        hostname=lnd_conf.get("host", "hostname"),
        protocol=lnd_conf.get("ln", "protocol"),
        mac_secure=lnd_conf.get("ln", "macaroon_admin"),
        cert_secure=lnd_conf.get("ln", "tls_certificate", fallback=None),
        rest_port=lnd_conf.get("ln", "rest_port"),
        grpc_port=lnd_conf.get("ln", "grpc_port"),
    )
