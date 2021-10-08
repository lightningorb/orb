from kivy.event import EventDispatcher
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.properties import NumericProperty
from kivy.uix.screenmanager import Screen
import data_manager
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from decorators import guarded


class Invoice(BoxLayout):
    raw = ObjectProperty("")
    destination = ObjectProperty("")
    num_satoshis = ObjectProperty(0)
    timestamp = ObjectProperty(0)
    expiry = ObjectProperty(0)
    description = ObjectProperty("")


class IngestInvoicesScreen(Screen):
    count = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(IngestInvoicesScreen, self).__init__(**kwargs)
        self.store = data_manager.data_man.store

    @guarded
    def clear_store(self):
        self.store.delete("ingested_invoice")
        self.ids.scroll_view.clear_widgets()

    def on_enter(self):
        self.ids.scroll_view.clear_widgets()
        for inv in self.load():
            self.ids.scroll_view.add_widget(Invoice(**inv))

    def load(self):
        try:
            invoices = self.store.get("ingested_invoice")["invoices"]
        except:
            invoices = []
        self.count.text = f"Invoices: {len(invoices)}"
        return invoices

    def do_ingest(self, text):
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
                    self.ids.scroll_view.add_widget(Invoice(**data))
                except:
                    print(f"Problem decoding: {line}")
                    not_ingested.append(line)
        self.store.put("ingested_invoice", invoices=invs)
        self.count.text = str(len(self.load()))
        self.ids.invoices.text = "\n".join(not_ingested)
