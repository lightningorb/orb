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
from path_finding_widget import *
import time
from kivy.clock import mainthread

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
        inst.print("Temporary channel failure")
        routes.ignore_edge_on_route(failure_source_pubkey, route)
        if pk == failure_source_pubkey:
            return "Temporary channel failure"
    elif code == 18:
        inst.print("Unknown next peer")
        routes.ignore_edge_on_route(failure_source_pubkey, route)
        if pk == failure_source_pubkey:
            return "Unknown next peer"
    elif code == 12:
        inst.print("Fee insufficient")
        if pk == failure_source_pubkey:
            return "Fee insufficient"
    elif code == 14:
        inst.print("Channel disabled")
        routes.ignore_edge_on_route(failure_source_pubkey, route)
        if pk == failure_source_pubkey:
            return "Channel disabled"
    elif code == 13:
        inst.print("Incorrect CLTV expiry")
        routes.ignore_edge_on_route(failure_source_pubkey, route)
        if pk == failure_source_pubkey:
            return "Incorrect CLTV expiry"
    elif code == -1000:
        inst.print("Timeout")
        routes.ignore_edge_on_route(failure_source_pubkey, route)
        if pk == failure_source_pubkey:
            return "Timeout"
    else:
        inst.print(f"Unknown error code {repr(code)}:")
        inst.print(repr(response))
        if pk == failure_source_pubkey:
            return f"Unknown error code {repr(code)}:"


def get_low_inbound_peer(avoid):
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
        return choice(chans)


class PayScreen(Screen):
    def __init__(self, **kwargs):
        Screen.__init__(self, **kwargs)
        self.output = Output(None)
        self.output.lnd = data_manager.data_man.lnd
        self.store = data_manager.data_man.store

    @mainthread
    def print(self, text):
        app = App.get_running_app()
        console = app.root.ids.sm.get_screen("console")
        out = "\n".join(console.ids.console_output.output.split("\n")[:100])
        console.ids.console_output.output = out + "\n" + str(text)
        app.root.ids.status_line.ids.line_output.output = str(text)
        self.ids.output.add_widget(Label(text=str(text)))

    def load(self):
        try:
            return self.store.get("ingested_invoice")["invoices"]
        except:
            return []

    def get_invoice(self):
        try:
            return next(iter(self.load()), None)
        except:
            return []

    def remove_invoice(self, inv):
        invs = [x for x in self.load() if x["raw"] != inv["raw"]]
        self.store.put("ingested_invoice", invoices=invs)

    def pay(self):
        def thread_function():
            info = data_manager.data_man.lnd.get_info()
            alias = info.alias
            self.print("pay")
            self.print("loading invoices")
            self.print("loaded")
            # nodes = set([alias])
            # edges = set()
            while True:
                inv = self.get_invoice()
                if not inv:
                    self.print("no more invoices")
                    return
                else:
                    peer = get_low_inbound_peer(avoid)
                    if peer:
                        peer_alias = data_manager.data_man.lnd.get_node_alias(
                            peer.remote_pubkey
                        )
                        # nodes.add(peer_alias)
                        self.print(peer_alias)
                        # edges.add((alias, peer_alias))
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
                            outgoing_chan_id=peer.chan_id,
                            last_hop_pubkey=None,
                            fee_limit_msat=fee_limit_msat,
                            inst=self,
                        )
                        start = time.time()
                        attempts = []
                        has_next = False
                        count = 0
                        while routes.has_next():
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
                                self.print(text)
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
                                self.print("SUCCESS")
                                self.remove_invoice(inv)
                                sleep(10)
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
                            self.print("No routes found!")
                            sleep(2)
                            self.print(f"adding {peer.chan_id} to avoid list")
                            avoid[peer.chan_id] += 1
                    else:
                        self.print("No channels left to rebalance")
                        sleep(60)

        avoid.clear()
        self.thread = threading.Thread(target=thread_function)
        self.thread.daemon = True
        self.thread.start()

    def kill(self):
        self.thread.stop()
