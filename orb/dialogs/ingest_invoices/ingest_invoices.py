# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-15 07:15:28
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-08-07 14:07:59

from traceback import print_exc
from kivy.properties import ObjectProperty

from orb.ln import Ln
from orb.logic import licensing
from orb.misc.decorators import db_connect
from orb.store.db_meta import invoices_db_name
from orb.dialogs.ingest_invoices.invoice import Invoice
from orb.components.popup_drop_shadow import PopupDropShadow


class IngestInvoices(PopupDropShadow):
    count = ObjectProperty(None)
    ignore = []

    def __init__(self, **kwargs):
        super(IngestInvoices, self).__init__(**kwargs)
        self.ids.scroll_view.clear_widgets()

    def open(self, *args):
        super(IngestInvoices, self).open()
        for inv in self.load():
            self.ids.scroll_view.add_widget(Invoice(**inv.__data__))

    def update(self, *args):
        from kivy.core.clipboard import Clipboard

        clip = Clipboard.paste()
        if clip:
            if clip.startswith("ln"):
                if clip not in self.ids.invoices.text and clip not in self.ignore:
                    self.ids.invoices.text += f"\n{clip}\n"
                    self.ignore.append(clip)

    def dismiss(self, *args):
        for invoices in self.ids.scroll_view.children:
            invoices.dismiss()
        return super(IngestInvoices, self).dismiss(*args)

    @db_connect(invoices_db_name)
    def load(self):
        from orb.store import model

        invoices = (
            model.Invoice()
            .select()
            .where(model.Invoice.expired() == False, model.Invoice.paid == False)
        )
        self.count.text = f"{len(invoices)}"
        is_satoshi = licensing.is_satoshi()
        is_trial = licensing.is_trial()
        restrict = (not is_satoshi) or is_trial
        if restrict and len(invoices) >= 1:
            self.ids.ingest_button.disabled = True

        return [x for x in invoices]

    def do_ingest(self, text):
        def add_invoice_widget(inv):
            self.ids.scroll_view.add_widget(inv)

        def update(not_ingested):
            self.ids.invoices.text = "\n".join(not_ingested)

        @db_connect(invoices_db_name)
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
                        req = Ln().decode_payment_request(line)
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
            self.count.text = str(num_invoices)
            update(not_ingested)
            if restrict and num_invoices >= 1:
                self.ids.ingest_button.disabled = True

        func()
