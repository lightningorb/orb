from kivy.clock import mainthread
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
import data_manager
import time
#from plyer import notification
#from plyer.platforms.macosx.notification import OSXNotification


class MailScreen(Screen):
    def on_enter(self):
        @mainthread
        def run():
            print("notif")
            #OSXNotification().notify(title="Test", message="123")

        run()
        self.ids.inbox.clear_widgets()
        for invoice in data_manager.data_man.lnd.list_invoices().invoices:
            if not invoice.settled:
                continue
            print(invoice)
            htlc_records = []
            for htlc in invoice.htlcs:
                custom_records = htlc.custom_records
                if custom_records:
                    htlc_records.append(custom_records)

            if htlc_records:
                self.ids.inbox.add_widget(Label(text=time.ctime(invoice.settle_date)))
                for custom_records in htlc_records:
                    for k, v in custom_records.items():
                        if k == 34349334:
                            try:
                                msg = v.decode()
                            except UnicodeDecodeError:
                                msg = str(v).strip("b'")
                            if not msg:
                                msg = "<empty message>"
                            self.ids.inbox.add_widget(Label(text=msg))
