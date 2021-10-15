import data_manager
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.clock import Clock
from decorators import guarded


class BorderedLabel(Label):
    pass


class HUD(BoxLayout):
    pass


class HUD1(BorderedLabel):
    hud = ObjectProperty("")

    def __init__(self, *args, **kwargs):
        BorderedLabel.__init__(self, *args, **kwargs)
        Clock.schedule_interval(self.get_lnd_data, 60)
        Clock.schedule_once(self.get_lnd_data, 1)

    @guarded
    def get_lnd_data(self, *args):
        lnd = data_manager.data_man.lnd
        fr = lnd.fee_report()
        self.hud = f"Day: S{int(fr.day_fee_sum):,}\nWeek S{int(fr.week_fee_sum):,}\nMonth: S{int(fr.month_fee_sum):,}"


class HUD2(BorderedLabel):
    hud = ObjectProperty("")

    def __init__(self, *args, **kwargs):
        BorderedLabel.__init__(self, *args, **kwargs)
        Clock.schedule_interval(self.get_lnd_data, 60)
        Clock.schedule_once(self.get_lnd_data, 1)

    @guarded
    def get_lnd_data(self, *args):
        lnd = data_manager.data_man.lnd
        bal = lnd.get_balance()
        tot = int(bal.total_balance)
        conf = int(bal.confirmed_balance)
        unconf = int(bal.unconfirmed_balance)

        self.hud = f"  Chain Balance: S{tot:,}\n"
        if tot != conf:
            self.hud += f"  Conf. Chain Balance: S{conf:,}\n"
            self.hud += f"  Unconf. Chain Balance: S{unconf:,}\n"

        cbal = lnd.channel_balance()
        self.hud += f"  Local Balance: S{int(cbal.local_balance.sat):,}\n"
        self.hud += f"  Remote Balance: S{int(cbal.remote_balance.sat):,}"


class HUD3(BorderedLabel):
    hud = ObjectProperty("")

    def __init__(self, *args, **kwargs):
        BorderedLabel.__init__(self, *args, **kwargs)
        from kivy.metrics import Metrics

        dpi_info = Metrics.dpi
        pixel_density_info = Metrics.density
        self.hud = f"DPI: {dpi_info}, Pixel Density: {pixel_density_info}"
