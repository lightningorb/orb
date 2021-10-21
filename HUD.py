from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import RoundedRectangle, Line
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.clock import Clock
from decorators import guarded
import data_manager
import threading
import requests


class Bordered(Widget):
    pass

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

class HUD4(FloatLayout):
    def __init__(self, *args, **kwargs):
        FloatLayout.__init__(self, *args, **kwargs)
        with self.canvas.before:
            Color(1,1,1,1)
            self.line = Line(points=[0,0,500,500], width=1)
        self.bind(pos=self.update_rect, size=self.update_rect)
        Clock.schedule_interval(self.update_price, 60)
        Clock.schedule_once(self.update_price, 1)

    def update_rect(self, *args):
        def func():
            # this probably shouldn't be in update_rect
            d = requests.get("https://api.coindesk.com/v1/bpi/historical/close.json").json()['bpi']
            min_price, max_price, g = min(d.values()), max(d.values()), []
            for i, key in enumerate(d):
                g.append(i/len(d)*self.size[0])
                g.append(self.pos[1]+((d[key]-min_price)/(max_price-min_price))*self.size[1])
            self.line.points = g
            rate = str(int(requests.get("https://api.coindesk.com/v1/bpi/currentprice.json").json()['bpi']['USD']['rate_float']))
            self.ids.rate.text = f'${rate}'
        threading.Thread(target=func).start()

    def update_price(self, *args):
        def func():
            rate = int(requests.get("https://api.coindesk.com/v1/bpi/currentprice.json").json()['bpi']['USD']['rate_float'])
            self.ids.rate.text = f'${rate}'
        threading.Thread(target=func).start()


class HUD5(BorderedLabel):
    hud = ObjectProperty("")

    def __init__(self, *args, **kwargs):
        BorderedLabel.__init__(self, *args, **kwargs)
        Clock.schedule_interval(self.get_fees, 60)
        Clock.schedule_once(self.get_fees, 1)

    @guarded
    def get_fees(self, *args):
        def func():
            fees = requests.get("https://mempool.space/api/v1/fees/recommended").json()
            text = f"""\
Low priority: {fees["hourFee"]} sat/vB
Medium priority: {fees["halfHourFee"]} sat/vB
High priority: {fees["fastestFee"]} sat/vB"""
            self.hud = text
        threading.Thread(target=func).start()