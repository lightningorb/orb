# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-15 07:15:28
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-09-08 16:29:43

import base64

from orb.misc.output import Output

MAX_ROUTES_TO_REQUEST = 100


class Routes:
    num_requested_routes = 0
    all_routes = []
    returned_routes = []
    ignored_pairs = []
    ignored_nodes = []

    def __init__(
        self,
        pub_key,
        payment_request,
        outgoing_chan_id,
        last_hop_pubkey,
        fee_limit_msat,
        time_pref,
        cltv,
        ln,
    ):
        self.pub_key = pub_key
        self.payment_request = payment_request
        self.last_hop_pubkey = last_hop_pubkey
        self.outgoing_chan_id = outgoing_chan_id
        self.fee_limit_msat = fee_limit_msat
        self.time_pref = time_pref
        self.output = Output(ln)
        self.cltv = cltv
        self.ln = ln

    def has_next(self):
        self.update_routes()
        return len(self.returned_routes) < len(self.all_routes)

    def get_next(self):
        self.update_routes()
        for route in self.all_routes:
            if route not in self.returned_routes:
                self.returned_routes.append(route)
                return route
        return None

    def update_routes(self):
        while True:
            if len(self.returned_routes) < len(self.all_routes):
                return
            if self.num_requested_routes >= MAX_ROUTES_TO_REQUEST:
                return
            self.request_route()

    def request_route(self):
        amount = self.get_amount()
        route = self.ln.get_route(
            pub_key=self.pub_key,
            amount_sat=amount,
            ignored_pairs=self.ignored_pairs,
            ignored_nodes=self.ignored_nodes,
            last_hop_pubkey=self.last_hop_pubkey,
            outgoing_chan_id=self.outgoing_chan_id,
            fee_limit_msat=self.fee_limit_msat,
            time_pref=float(self.time_pref),
            cltv=self.cltv,
        )
        if route.hops and route.total_fees_msat > self.fee_limit_msat:
            print("Route too expensive")
            assert False
        if not route.hops:
            self.num_requested_routes = MAX_ROUTES_TO_REQUEST
        else:
            self.num_requested_routes += 1
            self.add_route(route)

    def add_route(self, route):
        if route is None:
            return
        if route not in self.all_routes:
            self.all_routes.append(route)

    def get_amount(self):
        return self.payment_request.num_satoshis

    def ignore_edge_on_route(self, failure_source_pubkey, route):
        ignore_next = False
        for hop in route.hops:
            if ignore_next:
                if self.ln.node_type == "cln":
                    self.ignored_nodes.append(f"{hop.chan_id}/0")
                    self.ignored_nodes.append(f"{hop.chan_id}/1")
                elif self.ln.node_type == "lnd":
                    self.ignore_edge_from_to(
                        hop.chan_id, failure_source_pubkey, hop.pub_key
                    )
                return
            if hop.pub_key == failure_source_pubkey:
                ignore_next = True

    def ignore_edge_from_to(self, chan_id, from_pubkey, to_pubkey, show_message=True):
        pair = {
            "from": base64.b16decode(from_pubkey, True),
            "to": base64.b16decode(to_pubkey, True),
        }
        if pair in self.ignored_pairs:
            return
        if show_message:
            print(
                f"Ignoring {self.output.get_channel_representation(chan_id, to_pubkey, from_pubkey)}"
            )
        self.ignored_pairs.append(pair)
