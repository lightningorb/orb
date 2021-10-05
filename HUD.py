import data_manager
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget


class HUD(BoxLayout):
    hud = ObjectProperty("")

    def __init__(self, *args, **kwargs):
        BoxLayout.__init__(self, *args, **kwargs)
        lnd = data_manager.data_man.lnd
        bal = lnd.get_balance()
        tot = bal.total_balance
        conf = bal.confirmed_balance
        unconf = bal.unconfirmed_balance

        self.hud = f"  Chain Balance: S{tot:,}\n"
        if tot != conf:
            self.hud += f"  Conf. Chain Balance: S{conf:,}\n"
            self.hud += f"  Unconf. Chain Balance: S{unconf:,}\n"

        cbal = lnd.channel_balance()
        self.hud += f"  Local Balance: S{cbal.local_balance.sat:,}\n"
        self.hud += f"  Remote Balance: S{cbal.remote_balance.sat:,}"
