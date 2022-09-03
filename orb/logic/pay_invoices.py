# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-08-05 07:48:23
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-09-03 05:12:33

import threading
from time import sleep
from random import choice
from traceback import format_exc

import arrow

from orb.app import App

from orb.logic.channel_selector import get_low_inbound_channel
from orb.logic.pay_logic import pay_thread, PaymentStatus
from orb.core.stoppable_thread import StoppableThread
from orb.store.db_meta import invoices_db_name
from orb.misc.decorators import db_connect
from orb.ln import Ln


chan_ignore = set([])
lock = threading.Lock()
invoices_lock = threading.Lock()


class PaymentUIOption:
    auto_first_hop = 0
    user_selected_first_hop = 1


class PayInvoices(StoppableThread):
    def __init__(
        self,
        chan_id: str,
        max_paths: int,
        fee_rate: float,
        time_pref: float,
        num_threads: int,
        ln: Ln,
    ):
        super(PayInvoices, self).__init__()
        self.chan_id: int = chan_id
        self.max_paths: int = max_paths
        self.fee_rate: float = fee_rate
        self.time_pref: int = time_pref
        self.num_threads: int = num_threads
        self.inflight = set([])
        self.inflight_times = {}
        self.threads = set([])
        self.ln: Ln = ln

    @db_connect(name=invoices_db_name, lock=True)
    def load(self):
        from orb.store import model

        invoices = (
            model.Invoice()
            .select()
            .where(model.Invoice.expired() == False, model.Invoice.paid == False)
        )
        return [x for x in invoices]

    def get_ignored_chan_ids(self):
        return set(
            [
                k
                for k, v in App.get_running_app()
                .store.get("pay_through_channel", {})
                .items()
                if not v
            ]
        )

    def run(self):
        class PayThread(StoppableThread):
            def __init__(self, inst, name, thread_n, *args, **kwargs):
                super(PayThread, self).__init__(*args, **kwargs)
                self.name = str(thread_n)
                self.inst = inst
                self.thread_n = thread_n

            def sprint(self, *args):
                print(f'PT{self.thread_n}: {" ".join(args)}')

            def run(self):
                super(PayThread, self).run()
                self.sprint("Running payment thread")
                while True:
                    try:
                        self.__run()
                        self.sprint("stopping payment thread in finally")
                        self.stop()
                        break
                    except:
                        self.sprint("exception in payment thread")
                        print(format_exc())
                        sleep(10)

            def __run(self):
                payment_opt = (
                    PaymentUIOption.user_selected_first_hop
                    if self.inst.chan_id
                    else PaymentUIOption.auto_first_hop
                )
                auto = payment_opt == PaymentUIOption.auto_first_hop

                while True:
                    all_invoices = self.inst.load()
                    if not all_invoices:
                        print("Patiently awaiting for invoices before starting")
                        sleep(5)
                    else:
                        break

                while not self.stopped():
                    with invoices_lock:
                        all_invoices = self.inst.load()
                        usable_invoices = list(set(all_invoices) - self.inst.inflight)
                        invoice = choice(usable_invoices) if usable_invoices else None
                        if invoice:
                            self.inst.inflight_times[invoice] = arrow.now().timestamp()
                            self.inst.inflight.add(invoice)
                    if invoice:
                        payment_request = self.inst.ln.decode_payment_request(
                            invoice.raw
                        )
                    else:
                        if not all_invoices:
                            self.sprint("no more usable invoices")
                            self.sprint(f"THREAD {self.thread_n} EXITING")
                            return
                        elif not usable_invoices:
                            self.sprint("all invoices are in-flight, sleeping")
                            sleep(30)
                            continue
                    if not auto:
                        chan_id = self.inst.chan_id
                    else:
                        with lock:
                            chan_id = get_low_inbound_channel(
                                pk_ignore=[],
                                chan_ignore=chan_ignore
                                | self.inst.get_ignored_chan_ids(),
                                num_sats=int(payment_request.num_satoshis)
                                + int(payment_request.num_satoshis)
                                * 0.05,  # 5% for the fees
                            )
                            if chan_id:
                                chan_ignore.add(chan_id)
                    if not chan_id:
                        self.sprint("no more channels left to rebalance")
                        sleep(60)
                    if chan_id:
                        try:
                            status = pay_thread(
                                stopped=self.stopped,
                                thread_n=self.thread_n,
                                fee_rate=self.inst.fee_rate,
                                payment_request=payment_request,
                                time_pref=self.inst.time_pref,
                                outgoing_chan_id=chan_id,
                                last_hop_pubkey=None,
                                max_paths=self.inst.max_paths,
                                ln=self.inst.ln,
                            )
                        except:
                            self.sprint("Exception in pay_thread")
                            print(format_exc())
                            status = PaymentStatus.exception

                        if chan_id in chan_ignore:
                            with lock:
                                chan_ignore.remove(chan_id)
                        if status == PaymentStatus.inflight:
                            print("Payment status is inflight")
                        elif status in [
                            PaymentStatus.success,
                            PaymentStatus.already_paid,
                        ]:
                            with invoices_lock:

                                @db_connect(name=invoices_db_name, lock=True)
                                def update_invoice(invoice):
                                    invoice.paid = True
                                    invoice.save()

                                update_invoice(invoice)

                                self.inst.inflight.remove(invoice)
                        elif (
                            status == PaymentStatus.no_routes
                            or status == PaymentStatus.max_paths_exceeded
                        ):
                            if status == PaymentStatus.no_routes:
                                self.sprint("no routes found")
                            if status == PaymentStatus.max_paths_exceeded:
                                self.sprint("max paths exceeded")
                            with invoices_lock:
                                self.inst.inflight.remove(invoice)
                        else:
                            with invoices_lock:
                                self.inst.inflight.remove(invoice)

                    if not auto:
                        break

                    sleep(5)

        for i in range(self.num_threads):
            t = PayThread(inst=self, name="PayThread", thread_n=i)
            t.start()
            self.threads.add(t)
        super(PayInvoices, self).run()

    def stop(self):
        super(PayInvoices, self).stop()

        for t in self.threads:
            t.stop()
