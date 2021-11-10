from orb.components.popup_drop_shadow import PopupDropShadow
from kivy.clock import mainthread
from threading import Thread

from queue import Queue
from time import sleep
import threading
import data_manager
from collections import Counter
from random import choice
from orb.misc.output import *
from orb.misc.ui_actions import console_output
from orb.logic.channel_selector import get_low_inbound_channel
from orb.logic.pay_logic import pay_thread, PaymentStatus
from orb.misc.utils import hashabledict

avoid = Counter()
LOOP = '021c97a90a411ff2b10dc2a8e32de2f29d2fa49d41bfbb52bd416e460db0747d0d'
GAMMA = '02769a851d7d11eaeaef899b2ed8c34fd387828fa13f6fe27928de2b9fa75a0cd8'
pk_ignore = set([LOOP, GAMMA])
chan_ignore = set([])
lock = threading.Lock()
invoices_lock = threading.Lock()


class PaymentUIOption:
    auto_first_hop = 0
    user_selected_first_hop = 1


class PayScreen(PopupDropShadow):
    def __init__(self, **kwargs):
        self.in_flight = set([])
        PopupDropShadow.__init__(self, **kwargs)
        self.output = Output(None)
        self.output.lnd = data_manager.data_man.lnd
        lnd = data_manager.data_man.lnd
        self.chan_id = None
        self.inflight = set([])

        @mainthread
        def delayed(channels):
            for c in channels:
                self.ids.spinner_id.values.append(
                    f"{c.chan_id}: {lnd.get_node_alias(c.remote_pubkey)}"
                )

        threading.Thread(target=lambda: delayed(lnd.get_channels())).start()

    def first_hop_spinner_click(self, chan):
        self.chan_id = int(chan.split(":")[0])

    def load(self):
        from orb.store import model

        invoices = (
            model.Invoice()
            .select()
            .where(model.Invoice.expired == False and model.Invoice.paid == False)
        )
        return invoices

    def pay(self):
        def thread_function(thread_n):
            payment_opt = (
                PaymentUIOption.user_selected_first_hop
                if self.chan_id
                else PaymentUIOption.auto_first_hop
            )
            auto = payment_opt == PaymentUIOption.auto_first_hop

            while True:
                with invoices_lock:
                    invoices = self.load()
                    invoice = choice(invoices) if invoices else None
                if not invoices:
                    console_output("no more usable invoices")
                    return
                payment_request = data_manager.data_man.lnd.decode_request(invoice.raw)
                if payment_opt == PaymentUIOption.user_selected_first_hop:
                    chan_id = self.chan_id
                else:
                    with lock:
                        chan_id = get_low_inbound_channel(
                            lnd=data_manager.data_man.lnd,
                            avoid=avoid,
                            pk_ignore=pk_ignore,
                            chan_ignore=chan_ignore,
                            num_sats=payment_request.num_satoshis,
                        )
                        if chan_id:
                            chan_ignore.add(chan_id)
                if not chan_id:
                    console_output('no more channels left to rebalance')
                    sleep(60)
                print(f"CHAN: {chan_id}")
                if chan_id:
                    with invoices_lock:
                        self.inflight.add(invoice)
                    status = pay_thread(
                        inst=self,
                        thread_n=thread_n,
                        fee_rate=int(self.ids.fee_rate.text),
                        payment_request=payment_request,
                        outgoing_chan_id=chan_id,
                        last_hop_pubkey=None,
                        max_paths=int(self.ids.max_paths.text),
                        payment_request_raw=invoice.raw,
                    )
                    if chan_id in chan_ignore:
                        with lock:
                            chan_ignore.remove(chan_id)
                    if status == PaymentStatus.inflight:
                        pass
                    elif status in [PaymentStatus.success, PaymentStatus.already_paid]:
                        with invoices_lock:
                            invoice.paid = True
                            invoice.save()
                    elif (
                        status == PaymentStatus.no_routes
                        or status == PaymentStatus.max_paths_exceeded
                    ):
                        if status == PaymentStatus.no_routes:
                            console_output('no routes found')
                        if status == PaymentStatus.max_paths_exceeded:
                            console_output('max paths exceeded')
                        if auto:
                            console_output(f"adding {chan_id} to avoid list")
                            avoid[chan_id] += 1
                sleep(5)

        avoid.clear()
        for i in range(int(self.ids.num_threads.text)):
            self.thread = threading.Thread(target=thread_function, args=(i,))
            self.thread.daemon = True
            self.thread.start()

    def kill(self):
        self.thread.stop()
