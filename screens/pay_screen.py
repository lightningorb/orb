from kivy.uix.popup import Popup
from kivy.clock import mainthread
from kivy.app import App
from kivy.uix.screenmanager import Screen
from threading import Thread

from queue import Queue
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
import concurrent.futures
from channel_selector import get_low_inbound_channel
# from grandalf.layouts import SugiyamaLayout
# from grandalf.graphs import Vertex, Edge, Graph, graph_core

avoid = Counter()
pk_ignore = set(['021c97a90a411ff2b10dc2a8e32de2f29d2fa49d41bfbb52bd416e460db0747d0d'])
chan_ignore = set([])

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

class PaymentUIOption:
    auto_first_hop = 0
    user_selected_first_hop = 1


class PaymentStatus:
    success = 0
    exception = 1
    failure = 2
    no_routes = 3
    error = 4
    none = 5
    max_paths_exceeded = 6


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
        return self.store.get("ingested_invoice", {}).get("invoices", [])

    def get_random_invoice(self):
        invoices = self.load()
        if invoices:
            return choice(invoices)

    def remove_invoice(self, inv):
        invs = [x for x in self.load() if x["raw"] != inv]
        self.store.put("ingested_invoice", invoices=invs)

    def pay(self):

        def pay_thread(thread_n, fee_rate, payment_request, payment_request_raw, chan_id, payment_opt, max_paths):
            print(f"starting payment thread {thread_n} for chan: {chan_id}")
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
            has_next = False
            count = 0
            while routes.has_next():
                if count > max_paths:
                    return payment_request_raw, chan_id, PaymentStatus.max_paths_exceeded
                count += 1
                has_next = True
                route = routes.get_next()
                for j, hop in enumerate(route.hops):
                    node_alias = data_manager.data_man.lnd.get_node_alias(
                        hop.pub_key
                    )
                    text = f"{j:<5}:        {node_alias}"
                    console_output(f'T{thread_n}: {text}')
                try:
                    response = data_manager.data_man.lnd.send_payment(
                        payment_request, route
                    )
                except:
                    console_output(f'T{thread_n}: {str(traceback.print_exc())}')
                    console_output(f"T{thread_n}: exception - removing invoice")
                    return payment_request_raw, chan_id, PaymentStatus.exception
                is_successful = response and response.failure.code == 0
                if is_successful:
                    console_output(f"T{thread_n}: SUCCESS")
                    return payment_request_raw, chan_id, PaymentStatus.success
                else:
                    handle_error(self, response, route, routes)
            if not has_next:
                console_output(f"T{thread_n}: No routes found!")
                return payment_request_raw, chan_id, PaymentStatus.no_routes
            return payment_request_raw, chan_id, PaymentStatus.none

        def thread_function():
            payment_opt = (
                PaymentUIOption.user_selected_first_hop
                if self.chan_id
                else PaymentUIOption.auto_first_hop
            )
            auto = payment_opt == PaymentUIOption.auto_first_hop

            while True:
                que = Queue()
                threads_list = list()
                invoices = self.load()
                if not invoices:
                    console_output("no more invoices")
                    return
                for i in range(min(len(invoices), int(self.ids.num_threads.text))):
                    payment_request = data_manager.data_man.lnd.decode_request(
                        invoices[i]["raw"]
                    )
                    if payment_opt == PaymentUIOption.user_selected_first_hop:
                        chan_id = self.chan_id
                    else:
                        chan_id = get_low_inbound_channel(
                            lnd=data_manager.data_man.lnd,
                            avoid=avoid,
                            pk_ignore=pk_ignore,
                            chan_ignore=chan_ignore,
                            num_sats=payment_request.num_satoshis
                            )
                    print(f"CHAN: {chan_id}")
                    if chan_id:
                        chan_ignore.add(chan_id)
                        t = Thread(
                            target=lambda q, kwargs: q.put(pay_thread(**kwargs)),
                            args=(que, dict(
                                thread_n=i,
                                fee_rate=int(self.ids.fee_rate.text),
                                payment_request=payment_request,
                                payment_request_raw=invoices[i]['raw'],
                                chan_id=chan_id,
                                payment_opt=payment_opt,
                                max_paths=int(self.ids.max_paths.text)))
                        )
                        t.start()
                        threads_list.append(t)
                for t in threads_list:
                    t.join()
                while not que.empty():
                    payment_request_raw, chan_id, status = que.get()
                    if chan_id in chan_ignore:
                        chan_ignore.remove(chan_id)
                    if status in [PaymentStatus.success, PaymentStatus.exception]:
                        self.remove_invoice(payment_request_raw)
                    elif status == PaymentStatus.no_routes or status == PaymentStatus.max_paths_exceeded:
                        if auto:
                            console_output(f"adding {chan_id} to avoid list")
                            avoid[chan_id] += 1
                if not threads_list:
                    console_output("No channels left to rebalance")
                    sleep(60)
                sleep(60)



        avoid.clear()
        self.thread = threading.Thread(target=thread_function)
        self.thread.daemon = True
        self.thread.start()

    def kill(self):
        self.thread.stop()
