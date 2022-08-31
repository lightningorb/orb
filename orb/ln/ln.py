# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-08-06 13:35:10
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-08-31 15:51:46

from configparser import ConfigParser

from pathlib import Path
from orb.lnd.lnd import Lnd
from orb.cln.cln import Cln
from orb.ln.types import *
from orb.app import App


class Ln:

    """The :class:`orb.ln.Ln` class can be used to perform RPC/REST
    calls on LND / CLN nodes using a unified interface.

    :param node_type: either "lnd" or "cln"
    :param fallback_to_mock: wehther to provide a mock class if construction fails
    :param cache: whether to cache the result, or rebuilt the concrete class each time
    :param use_prefs: whether to use the user prefs to initialize
    :param hostname: the hostname or ip address to the node
    :param protocol: rest or grpc
    :param mac_secure: the rsa encrypted macaroon
    :param mac: the plain macaroon
    :param cert_secure: the rsa encrypted certificate string
    :param cert: the plain certificate string
    :param rest_port: the REST protocol port
    :param grpc_port: the GRPC protocol port
    :param version: the API version
    """

    def __init__(
        self,
        node_type: str = None,
        fallback_to_mock: bool = True,
        cache: bool = True,
        use_prefs: bool = True,
        hostname: str = None,
        protocol: str = None,
        mac_secure: str = None,
        mac: str = None,
        cert_secure: str = None,
        cert: str = None,
        rest_port: int = None,
        grpc_port: int = None,
        version: str = None,
    ):
        if not node_type:
            from orb.misc.utils_no_kivy import pref

            node_type = pref("host.type")
        self.node_type = node_type
        self.concrete = {"lnd": Lnd, "cln": Cln}[node_type](
            fallback_to_mock=fallback_to_mock,
            cache=cache,
            use_prefs=use_prefs,
            hostname=hostname,
            protocol=protocol,
            mac_secure=mac_secure,
            mac=mac,
            cert_secure=cert_secure,
            cert=cert,
            rest_port=rest_port,
            grpc_port=grpc_port,
            version=version,
        )

    def get_info(self) -> Info:
        """Get basic info."""
        return Info(impl=self.node_type, **self.concrete.get_info().__dict__)

    def get_node_info(self, pubkey) -> NodeInfo:
        """Get information on the node provided in params.

        :param pubkey: The pubkey of the node for which to get information.
        """
        return NodeInfo(
            impl=self.node_type, **self.concrete.get_node_info(pubkey).__dict__
        )

    def get_balance(self) -> Balance:
        """Get balance for current node."""
        return Balance(impl=self.node_type, **self.concrete.get_balance().__dict__)

    def list_peers(self) -> Peers:
        """List peers for the current node."""
        return Peers(impl=self.node_type, response=self.concrete.list_peers())

    def local_remote_bal(self) -> LocalRemoteBal:
        """Get balance for current node."""
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
        source_pub_key=None,
        outgoing_chan_id=None,
        ignored_nodes=[],
        ignored_pairs=[],
        last_hop_pubkey=None,
        amount_sat=None,
        time_pref=None,
        cltv=0,
        **kwargs,
    ) -> Route:
        """Get a route to the given pubkey.

        :param fee_limit_msat: the fee limit in millisatoshis. This is ignored by CLN.
        :param pub_key: the pub_key of the node to which to find a route.
        :param source_pub_key: the pub_key of the node from which to find a route.
        :param outgoing_chan_id: the channel id the first hop o the route.
        :param ignored_nodes: list of nodes to ignore.
        :param ignored_pairs: list of pairs to ignore (LND only).
        :param last_hop_pubkey: the last node before 'pub_key' (LND only).
        :param amount_sat: the amount in satoshis the route should accomodate.
        :param time_pref: the time preference of the route, from 0 to 1. (LND only).
        :param cltv: absolute lock time. (CLN only).
        """
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

    def get_policy_to(self, channel) -> Policy:
        """Get policy for the given channel.

        :param channel: the channel for which to get policy.
        :type channel: :class:`orb.misc.Channel`
        """
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

    def decode_payment_request(self, bolt11: str) -> PaymentRequest:
        """Decodes a bolt11 payment request.

        :param bolt11: the bolt11 payment request string
        :return: The payment request as a :class:`orb.ln.types.PaymentRequest`
        :rtype: PaymentRequest
        """

        """
        Keyword arguments:
        bolt11 --  (default None)
        """
        res = self.concrete.decode_payment_request(bolt11)
        return PaymentRequest(
            impl=self.node_type,
            **res.__dict__,
        )

    def send_coins(
        self, addr: str, satoshi: int, sat_per_vbyte: int, send_all: bool = False
    ) -> ChainTransaction:
        res = self.concrete.send_coins(
            addr=addr, satoshi=satoshi, sat_per_vbyte=sat_per_vbyte, send_all=send_all
        )
        return ChainTransaction(impl=self.node_type, tx=res)

    def send_payment(self, payment_request, route) -> SendPaymentResponse:
        res = self.concrete.send_payment(payment_request, route)
        return SendPaymentResponse(self.node_type, res)

    def get_forwarding_history(
        self, index_offset=0, num_max_events=100
    ) -> ForwardingEvents:
        """Get the settled forwarding events for the current node.

        :param index_offset: starting index.
        :param num_max_events: number of paginated events to fetch.
        """
        res = self.concrete.get_forwarding_history(
            index_offset=index_offset,
            num_max_events=num_max_events,
        )

        return ForwardingEvents(impl=self.node_type, fwd=res)

    def get_htlc_events(self) -> HTLC:
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
