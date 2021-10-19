from kivy.uix.popup import Popup
from kivy.clock import mainthread
from kivy.app import App
from kivy.uix.screenmanager import Screen

from time import sleep
import threading
from simple_chalk import *
from pay_widget import *
import traceback
import data_manager
from collections import Counter
from random import choice
from kivy.uix.label import Label
from routes import Routes
from output import *
import time
from ui_actions import console_output

# from grandalf.layouts import SugiyamaLayout
# from grandalf.graphs import Vertex, Edge, Graph, graph_core

avoid = Counter()


class defaultview(object):
    w, h = 1000, 500


def get_failure_source_pubkey(response, route):
    if response.failure.failure_source_index == 0:
        failure_source_pubkey = route.hops[-1].pub_key
    else:
        failure_source_pubkey = route.hops[
            response.failure.failure_source_index - 1
        ].pub_key
    return failure_source_pubkey


def handle_error(inst, response, route, routes, pk=None):
    if response:
        code = response.failure.code
        failure_source_pubkey = get_failure_source_pubkey(response, route)
    else:
        code = -1000
        failure_source_pubkey = route.hops[-1].pub_key
    if code == 15:
        console_output("Temporary channel failure")
        routes.ignore_edge_on_route(failure_source_pubkey, route)
        if pk == failure_source_pubkey:
            return "Temporary channel failure"
    elif code == 18:
        console_output("Unknown next peer")
        routes.ignore_edge_on_route(failure_source_pubkey, route)
        if pk == failure_source_pubkey:
            return "Unknown next peer"
    elif code == 12:
        console_output("Fee insufficient")
        if pk == failure_source_pubkey:
            return "Fee insufficient"
    elif code == 14:
        console_output("Channel disabled")
        routes.ignore_edge_on_route(failure_source_pubkey, route)
        if pk == failure_source_pubkey:
            return "Channel disabled"
    elif code == 13:
        console_output("Incorrect CLTV expiry")
        routes.ignore_edge_on_route(failure_source_pubkey, route)
        if pk == failure_source_pubkey:
            return "Incorrect CLTV expiry"
    elif code == -1000:
        console_output("Timeout")
        routes.ignore_edge_on_route(failure_source_pubkey, route)
        if pk == failure_source_pubkey:
            return "Timeout"
    else:
        console_output(f"Unknown error code {repr(code)}:")
        console_output(repr(response))
        if pk == failure_source_pubkey:
            return f"Unknown error code {repr(code)}:"


def get_low_inbound_channel(avoid):
    chans = []
    channels = data_manager.data_man.lnd.get_channels(active_only=True)
    for chan in channels:
        if (chan.remote_balance + 1e6) / chan.capacity < 0.5:
            if chan.chan_id in [*avoid.keys()]:
                avoid[chan.chan_id] += 1
                if avoid[chan.chan_id] > 5:
                    del avoid[chan.chan_id]
                else:
                    continue
            alias = data_manager.data_man.lnd.get_node_alias(chan.remote_pubkey)
            if alias in ["LOOP"]:
                continue
            chans.append(chan)
    if chans:
        return choice(chans).chan_id


class PaymentUIOption:
    auto_first_hop = 0
    user_selected_first_hop = 1


class PayScreen(Popup):
    def __init__(self, **kwargs):
        Popup.__init__(self, **kwargs)
        self.output = Output(None)
        self.output.lnd = data_manager.data_man.lnd
        lnd = data_manager.data_man.lnd
        self.store = data_manager.data_man.store
        self.chan_id = None

        @mainthread
        def delayed():
            channels = lnd.get_channels()
            for c in channels:
                self.ids.spinner_id.values.append(
                    f"{c.chan_id}: {lnd.get_node_alias(c.remote_pubkey)}"
                )

        delayed()

    def first_hop_spinner_click(self, chan):
        self.chan_id = int(chan.split(":")[0])

    def load(self):
        try:
            return self.store.get("ingested_invoice")["invoices"]
        except:
            return []

    def get_invoice(self):
        try:
            return choice(self.load())
        except:
            return []

    def remove_invoice(self, inv):
        invs = [x for x in self.load() if x["raw"] != inv["raw"]]
        self.store.put("ingested_invoice", invoices=invs)

    def pay(self):
        def thread_function():
            info = data_manager.data_man.lnd.get_info()
            alias = info.alias
            console_output("pay")
            console_output("loading invoices")
            console_output("loaded")
            # nodes = set([alias])
            # edges = set()
            payment_opt = (
                PaymentUIOption.user_selected_first_hop
                if self.chan_id
                else PaymentUIOption.auto_first_hop
            )
            while True:
                inv = self.get_invoice()
                if not inv:
                    console_output("no more invoices")
                    return
                else:
                    if payment_opt == PaymentUIOption.user_selected_first_hop:
                        chan_id = self.chan_id
                    else:
                        chan_id = get_low_inbound_channel(avoid)
                    if chan_id:
                        payment_request = data_manager.data_man.lnd.decode_request(
                            inv["raw"]
                        )
                        fee_rate = int(self.ids.fee_rate.text)
                        fee_limit_sat = fee_rate * (
                            1_000_000 / payment_request.num_satoshis
                        )
                        fee_limit_msat = fee_limit_sat * 1_000
                        routes = Routes(
                            lnd=data_manager.data_man.lnd,
                            pub_key=payment_request.destination,
                            payment_request=payment_request,
                            outgoing_chan_id=chan_id,
                            last_hop_pubkey=None,
                            fee_limit_msat=fee_limit_msat,
                            inst=self,
                        )
                        start = time.time()
                        attempts = []
                        has_next = False
                        count = 0
                        while routes.has_next():
                            if payment_opt == PaymentUIOption.auto_first_hop:
                                if count > 10:
                                    break
                            count += 1
                            has_next = True
                            route = routes.get_next()
                            #             paths = []
                            #             for h in route.hops:
                            #                 p = schemas.Path(
                            #                     alias="",
                            #                     pk=h.pub_key,
                            #                     rate=int(h.fee * (1e6 / payment_request.num_satoshis)),
                            #                     fee=h.fee,
                            #                     succeeded=False,
                            #                 )
                            #                 paths.append(p)

                            prev = None
                            for j, hop in enumerate(route.hops):
                                node_alias = data_manager.data_man.lnd.get_node_alias(
                                    hop.pub_key
                                )
                                # nodes.add(node_alias)
                                text = f"{j:<5}:        {node_alias}"
                                console_output(text)
                                # if prev:
                                #     edges.add((node_alias, prev))
                                # prev = node_alias
                            try:
                                response = data_manager.data_man.lnd.send_payment(
                                    payment_request, route
                                )
                            except:
                                print(traceback.print_exc())
                                print("exception - removing invoice", inv)
                                self.remove_invoice(inv)
                                break
                            is_successful = response and response.failure.code == 0
                            #             attempt = schemas.Attempt(
                            #                 path=paths,
                            #                 code=response.failure.code if response else -1000,
                            #                 weakest_link="",
                            #                 weakest_link_pk="",
                            #                 succeeded=is_successful,
                            #             )
                            #             attempts.append(attempt)
                            # V = [Vertex(n) for n in nodes]
                            # Vd = {v.data: v for v in V}
                            # g = Graph(V, [Edge(Vd[a], Vd[b]) for a, b in edges])

                            # for v in g.V():
                            #     v.view = defaultview()

                            # if False:
                            #     sug = SugiyamaLayout(g.C[0])
                            #     sug.init_all(roots=[Vd[alias]])
                            #     sug.draw()
                            #     for v in g.C[0].sV:
                            #         print(
                            #             "%s: (%d,%d)"
                            #             % (v.data, v.view.xy[0], v.view.xy[1])
                            #         )

                            if is_successful:
                                console_output("SUCCESS")
                                self.remove_invoice(inv)
                                sleep(0.5)
                                break

                            #                 log = schemas.Log(
                            #                     tokens=payment_request.num_satoshis,
                            #                     dest=lnd.get_info().identity_pubkey,
                            #                     attempts=attempts,
                            #                     failed_attempts=attempts[:-1],
                            #                     succeeded_attempt=attempts[-1] if is_successful else None,
                            #                     succeeded=is_successful,
                            #                     log_id="",
                            #                     fee=route.total_fees,
                            #                     paid=payment_request.num_satoshis,
                            #                     preimage="",
                            #                     relays=[],
                            #                     success=[],
                            #                     latency=int((time.time() - start) * 1000),
                            #                 )
                            #                 fn = routable.ingest(log)
                            #                 output.print_line("")
                            #                 output.print_line("Routable.space ingest:")
                            #                 output.print_line(fn, end="  ")
                            #                 output.print_line(f"http://localhost/log/{fn}")
                            #                 break
                            else:
                                #                 attempt.weakest_link_pk = (
                                #                     get_failure_source_pubkey(response, route)
                                #                     if response
                                #                     else route.hops[-1].pub_key
                                #                 )
                                handle_error(self, response, route, routes)

                        if not has_next:
                            console_output("No routes found!")
                            if payment_opt == PaymentUIOption.auto_first_hop:
                                sleep(2)
                                console_output(f"adding {chan_id} to avoid list")
                                avoid[chan_id] += 1
                            else:
                                sleep(60)
                    else:
                        console_output("No channels left to rebalance")
                        sleep(60)

        avoid.clear()
        self.thread = threading.Thread(target=thread_function)
        self.thread.daemon = True
        self.thread.start()

    def kill(self):
        self.thread.stop()
