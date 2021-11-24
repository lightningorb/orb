from threading import Thread
from queue import Queue
from time import sleep
import threading
from collections import Counter
from random import choice
from traceback import print_exc

from kivy.clock import mainthread

from orb.misc.output import *
from orb.misc.ui_actions import console_output
from orb.logic.channel_selector import get_low_inbound_channel
from orb.logic.pay_logic import pay_thread, PaymentStatus
from orb.misc.utils import hashabledict
from orb.components.popup_drop_shadow import PopupDropShadow
from orb.logic.thread_manager import thread_manager

import data_manager


LOOP = "021c97a90a411ff2b10dc2a8e32de2f29d2fa49d41bfbb52bd416e460db0747d0d"
GAMMA = "02769a851d7d11eaeaef899b2ed8c34fd387828fa13f6fe27928de2b9fa75a0cd8"
DIVER = "03aa49c1e98ff4f216d886c09da9961c516aca22812c108af1b187896ded89807e"
pk_ignore = set([LOOP, GAMMA, DIVER])
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
            .where(model.Invoice.expired() == False, model.Invoice.paid == False)
        )
        return invoices

    def get_ignored_pks(self):
        return [
            k
            for k, v in data_manager.data_man.store.get(
                "pay_through_channel", {}
            ).items()
            if not v
        ]

    def pay(self):
        class PayThread(threading.Thread):
            def __init__(self, inst, name, thread_n, *args, **kwargs):
                super(PayThread, self).__init__(*args, **kwargs)
                self._stop_event = threading.Event()
                self.name = name
                self.inst = inst
                self.thread_n = thread_n
                thread_manager.add_thread(self)

            def run(self):
                try:
                    self.__run()
                except:
                    print_exc()
                finally:
                    self.stop()

            def __run(self):
                payment_opt = (
                    PaymentUIOption.user_selected_first_hop
                    if self.inst.chan_id
                    else PaymentUIOption.auto_first_hop
                )
                auto = payment_opt == PaymentUIOption.auto_first_hop

                print(f"self.stopped() {self.stopped()}")

                while not self.stopped():
                    with invoices_lock:
                        invoices = self.inst.load()
                        invoice = choice(invoices) if invoices else None
                    if not invoices:
                        console_output("no more usable invoices")
                        return
                    payment_request = data_manager.data_man.lnd.decode_request(
                        invoice.raw
                    )
                    if payment_opt == PaymentUIOption.user_selected_first_hop:
                        chan_id = self.inst.chan_id
                    else:
                        with lock:
                            chan_id = get_low_inbound_channel(
                                lnd=data_manager.data_man.lnd,
                                pk_ignore=self.inst.get_ignored_pks(),
                                chan_ignore=chan_ignore,
                                num_sats=payment_request.num_satoshis,
                            )
                            if chan_id:
                                chan_ignore.add(chan_id)
                    if not chan_id:
                        console_output("no more channels left to rebalance")
                        sleep(60)
                    print(f"CHAN: {chan_id}")
                    if chan_id:
                        with invoices_lock:
                            self.inst.inflight.add(invoice)
                        status = pay_thread(
                            inst=self.inst,
                            stopped=self.stopped,
                            thread_n=self.thread_n,
                            fee_rate=int(self.inst.ids.fee_rate.text),
                            payment_request=payment_request,
                            outgoing_chan_id=chan_id,
                            last_hop_pubkey=None,
                            max_paths=int(self.inst.ids.max_paths.text),
                            payment_request_raw=invoice.raw,
                        )
                        if chan_id in chan_ignore:
                            with lock:
                                chan_ignore.remove(chan_id)
                        if status == PaymentStatus.inflight:
                            pass
                        elif status in [
                            PaymentStatus.success,
                            PaymentStatus.already_paid,
                        ]:
                            with invoices_lock:
                                invoice.paid = True
                                invoice.save()
                        elif (
                            status == PaymentStatus.no_routes
                            or status == PaymentStatus.max_paths_exceeded
                        ):
                            if status == PaymentStatus.no_routes:
                                console_output("no routes found")
                            if status == PaymentStatus.max_paths_exceeded:
                                console_output("max paths exceeded")
                    sleep(5)

            def stop(self):
                self._stop_event.set()

            def stopped(self):
                return self._stop_event.is_set()

        for i in range(int(self.ids.num_threads.text)):
            self.thread = PayThread(inst=self, name="PayThread", thread_n=i)
            self.thread.daemon = True
            self.thread.start()

    def kill(self):
        self.thread.stop()
