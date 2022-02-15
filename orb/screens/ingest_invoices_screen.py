# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-15 07:15:28
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-02-15 15:28:40

import arrow
from datetime import timedelta
from traceback import print_exc
from threading import Thread

from kivy.clock import Clock
from kivy.clock import mainthread
from kivy.properties import ObjectProperty, NumericProperty, BooleanProperty
from kivy.uix.boxlayout import BoxLayout

from orb.components.popup_drop_shadow import PopupDropShadow
from orb.lnd import Lnd
from orb.logic import licensing


class Invoice(BoxLayout):
    raw = ObjectProperty("")
    destination = ObjectProperty("")
    num_satoshis = ObjectProperty(0)
    timestamp = ObjectProperty(0)
    expiry = ObjectProperty(0)
    description = ObjectProperty("")
    paid = BooleanProperty(False)
    id = NumericProperty(0)

    def __init__(self, *args, **kwargs):
        super(Invoice, self).__init__(*args, **kwargs)

        self.schedule = Clock.schedule_interval(self.update, 1)

    def update(self, *args):
        delta = int(self.timestamp) + int(self.expiry) - int(arrow.utcnow().timestamp())
        if delta < 0:
            self.ids.expiry_label.text = "expired"
        else:
            self.ids.expiry_label.text = (
                arrow.utcnow()
                .shift(seconds=delta)
                .humanize(granularity=["hour", "minute", "second"])
            )

    def dismiss(self):
        Clock.unschedule(self.schedule)


class IngestInvoicesScreen(PopupDropShadow):
    count = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(IngestInvoicesScreen, self).__init__(**kwargs)
        self.ids.scroll_view.clear_widgets()
        for inv in self.load():
            self.ids.scroll_view.add_widget(Invoice(**inv.__data__))

    def dismiss(self, *args):
        for invoices in self.ids.scroll_view.children:
            invoices.dismiss()
        return super(IngestInvoicesScreen, self).dismiss(*args)

    def load(self):
        from orb.store import model

        invoices = (
            model.Invoice()
            .select()
            .where(model.Invoice.expired() == False, model.Invoice.paid == False)
        )
        self.count.text = f"Invoices: {len(invoices)}"
        is_satoshi = licensing.is_satoshi()
        is_trial = licensing.is_trial()
        restrict = (not is_satoshi) or is_trial
        if restrict and len(invoices) >= 1:
            self.ids.ingest_button.disabled = True

        return invoices

    def do_ingest(self, text):
        @mainthread
        def add_invoice_widget(inv):
            self.ids.scroll_view.add_widget(inv)

        @mainthread
        def update(not_ingested):
            self.ids.invoices.text = "\n".join(not_ingested)

        def func():
            from orb.store import model

            is_satoshi = licensing.is_satoshi()
            is_trial = licensing.is_trial()
            restrict = (not is_satoshi) or is_trial

            ingested_count = 0
            not_ingested = []
            for line in text.split("\n"):
                line = line.strip()
                if line:
                    try:
                        req = Lnd().decode_payment_request(line)
                        if model.Invoice().select().where(model.Invoice.raw == line):
                            raise Exception("Already ingested")
                        invoice = model.Invoice(
                            raw=line,
                            destination=req.destination,
                            num_satoshis=req.num_satoshis,
                            timestamp=req.timestamp,
                            expiry=req.expiry,
                            description=req.description,
                        )
                        ingested_count += 1
                        invoice.save()
                        add_invoice_widget(Invoice(**invoice.__data__))
                        if restrict:
                            print(f"Non Satoshi & trial edition invoice limit: 1")
                            break
                    except:
                        print(f"Problem decoding: {line}")
                        print_exc()
                        not_ingested.append(line)

            num_invoices = int(self.count.text) + ingested_count
            self.count.text = num_invoices
            update(not_ingested)
            if restrict and num_invoices >= 1:
                self.ids.ingest_button.disabled = True

        Thread(target=func).start()
