from kivy.clock import Clock
from kivy.clock import mainthread
from kivy.properties import ObjectProperty, NumericProperty, BooleanProperty
from orb.components.popup_drop_shadow import PopupDropShadow
from kivy.uix.boxlayout import BoxLayout
from threading import Thread
import humanize
import arrow
from datetime import timedelta

from traceback import print_exc
import data_manager


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
        zero = timedelta(hours=0, minutes=0, seconds=0)
        delta = arrow.get(int(self.timestamp) + int(self.expiry)) - arrow.now()
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

            invs = self.load()
            not_ingested = []
            for line in text.split("\n"):
                line = line.strip()
                if line:
                    try:
                        req = data_manager.data_man.lnd.decode_payment_request(line)
                        if model.Invoice().select().where(model.Invoice.raw == line):
                            raise Exception('Already ingested')
                        invoice = model.Invoice(
                            raw=line,
                            destination=req.destination,
                            num_satoshis=req.num_satoshis,
                            timestamp=req.timestamp,
                            expiry=req.expiry,
                            description=req.description,
                        )
                        invoice.save()
                        add_invoice_widget(Invoice(**invoice.__data__))
                    except:
                        print(f"Problem decoding: {line}")
                        print_exc()
                        not_ingested.append(line)
            self.count.text = str(len(self.load()))
            update(not_ingested)

        Thread(target=func).start()
