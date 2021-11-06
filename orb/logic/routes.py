import base64
from orb.misc.ui_actions import console_output

MAX_ROUTES_TO_REQUEST = 100


class Routes:
    num_requested_routes = 0
    all_routes = []
    returned_routes = []
    ignored_pairs = []
    ignored_nodes = []

    def __init__(
        self,
        lnd,
        pub_key,
        payment_request,
        outgoing_chan_id,
        last_hop_pubkey,
        fee_limit_msat,
        inst,
    ):
        self.lnd = lnd
        self.pub_key = pub_key
        self.payment_request = payment_request
        self.last_hop_pubkey = last_hop_pubkey
        self.outgoing_chan_id = outgoing_chan_id
        self.fee_limit_msat = fee_limit_msat
        self.inst = inst

    def has_next(self):
        self.update_routes()
        return self.returned_routes < self.all_routes

    def get_next(self):
        self.update_routes()
        for route in self.all_routes:
            if route not in self.returned_routes:
                self.returned_routes.append(route)
                return route
        return None

    def update_routes(self):
        while True:
            if self.returned_routes < self.all_routes:
                return
            if self.num_requested_routes >= MAX_ROUTES_TO_REQUEST:
                return
            self.request_route()

    def request_route(self):
        amount = self.get_amount()
        routes = self.lnd.get_route(
            pub_key=self.pub_key,
            amount=amount,
            ignored_pairs=self.ignored_pairs,
            ignored_nodes=self.ignored_nodes,
            last_hop_pubkey=self.last_hop_pubkey,
            outgoing_chan_id=self.outgoing_chan_id,
            fee_limit_msat=self.fee_limit_msat,
        )
        if routes is None:
            self.num_requested_routes = MAX_ROUTES_TO_REQUEST
        else:
            self.num_requested_routes += 1
            for route in routes:
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
            console_output(
                f"Ignoring {self.inst.output.get_channel_representation(chan_id, to_pubkey, from_pubkey)}"
            )
        self.ignored_pairs.append(pair)
