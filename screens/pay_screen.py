from kivy.uix.popup import Popup
from kivy.clock import mainthread
from threading import Thread

from queue import Queue
from time import sleep
import threading
import data_manager
from collections import Counter
from random import choice
from output import *
from ui_actions import console_output
from channel_selector import get_low_inbound_channel
from pay_logic import pay_thread, PaymentStatus

avoid = Counter()
pk_ignore = set(['021c97a90a411ff2b10dc2a8e32de2f29d2fa49d41bfbb52bd416e460db0747d0d'])
chan_ignore = set([])

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
        return self.store.get("ingested_invoice", {}).get("invoices", [])

    def get_random_invoice(self):
        invoices = self.load()
        if invoices:
            return choice(invoices)

    def remove_invoice(self, inv):
        invs = [x for x in self.load() if x["raw"] != inv]
        self.store.put("ingested_invoice", invoices=invs)

    def pay(self):

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
                                inst=self,
                                thread_n=i,
                                fee_rate=int(self.ids.fee_rate.text),
                                payment_request=payment_request,
                                payment_request_raw=invoices[i]['raw'],
                                outgoing_chan_id=chan_id,
                                last_hop_pubkey=None,
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
