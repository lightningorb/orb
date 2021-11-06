from kivy.clock import Clock
from kivy.clock import mainthread
from kivy.properties import ObjectProperty
from orb.components.popup_drop_shadow import PopupDropShadow
from kivy.uix.boxlayout import BoxLayout
from threading import Thread
import humanize
import arrow
from datetime import timedelta

from orb.misc.decorators import guarded
from traceback import print_exc
import data_manager


class Invoice(BoxLayout):
    raw = ObjectProperty("")
    destination = ObjectProperty("")
    num_satoshis = ObjectProperty(0)
    timestamp = ObjectProperty(0)
    expiry = ObjectProperty(0)
    description = ObjectProperty("")

    def __init__(self, *args, **kwargs):
        super(Invoice, self).__init__(*args, **kwargs)

        self.schedule = Clock.schedule_interval(self.update, 1)

    def update(self, *args):
        zero = timedelta(hours=0, minutes=0, seconds=0)
        delta = arrow.get(self.timestamp + self.expiry) - arrow.now()
        if delta < zero:
            self.ids.expiry_label.text = 'expired'
        else:
            self.ids.expiry_label.text = humanize.precisedelta(
                delta, minimum_unit="seconds"
            )

    def dismiss(self):
        Clock.unschedule(self.schedule)


class IngestInvoicesScreen(PopupDropShadow):
    count = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(IngestInvoicesScreen, self).__init__(**kwargs)
        self.store = data_manager.data_man.store
        self.ids.scroll_view.clear_widgets()
        for inv in self.load():
            self.ids.scroll_view.add_widget(Invoice(**inv))

    def dismiss(self, *args):
        for invoices in self.ids.scroll_view.children:
            invoices.dismiss()
        return super(IngestInvoicesScreen, self).dismiss(*args)

    @guarded
    def clear_store(self):
        self.store.delete("ingested_invoice")
        self.ids.scroll_view.clear_widgets()
        self.count.text = '0'

    def load(self):
        try:
            invoices = self.store.get("ingested_invoice")["invoices"]
        except:
            invoices = []
        self.count.text = f"Invoices: {len(invoices)}"
        return invoices

    def do_ingest(self, text):
        @mainthread
        def add_invoice_widget(inv):
            self.ids.scroll_view.add_widget(inv)

        @mainthread
        def update(not_ingested):
            self.ids.invoices.text = "\n".join(not_ingested)

        def func():
            invs = self.load()
            not_ingested = []
            for line in text.split("\n"):
                if line:
                    try:
                        req = data_manager.data_man.lnd.decode_payment_request(line)
                        data = dict(
                            raw=line,
                            destination=req.destination,
                            num_satoshis=req.num_satoshis,
                            timestamp=req.timestamp,
                            expiry=req.expiry,
                            description=req.description,
                        )
                        invs.append(data)
                        add_invoice_widget(Invoice(**data))
                    except:
                        print(f"Problem decoding: {line}")
                        print_exc()
                        not_ingested.append(line)
            self.store.put("ingested_invoice", invoices=invs)
            self.count.text = str(len(self.load()))
            update(not_ingested)

        Thread(target=func).start()
