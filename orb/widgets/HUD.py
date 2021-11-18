import threading
import requests

from kivy.clock import mainthread
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Line
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ListProperty
from kivy.properties import ObjectProperty
from kivy.properties import NumericProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.clock import Clock

from orb.misc.decorators import silent, guarded
from orb.misc import mempool
from orb.misc.forex import forex

import data_manager


class Bordered(Widget):
    pass


class Hideable:
    alpha = NumericProperty(0)

    def show(self):
        self.alpha = 1


class BorderedLabel(Label, Hideable):
    pass


class HUD(BoxLayout):
    pass


class HUD1(BorderedLabel):
    """
    Fee Summary HUD
    """

    hud = ObjectProperty("")

    def __init__(self, *args, **kwargs):
        BorderedLabel.__init__(self, *args, **kwargs)
        Clock.schedule_interval(self.get_lnd_data, 60)
        Clock.schedule_once(self.get_lnd_data, 1)

    @guarded
    def get_lnd_data(self, *args):
        @mainthread
        def update_gui(text):
            self.hud = text
            self.show()

        @guarded
        def func():
            lnd = data_manager.data_man.lnd
            fr = lnd.fee_report()
            update_gui(
                f"Day: {forex(fr.day_fee_sum)}\nWeek"
                f" {forex(fr.week_fee_sum)}\nMonth:"
                f" {forex(fr.month_fee_sum)}"
            )

        threading.Thread(target=func).start()


class HUD2(BorderedLabel):
    """
    Balance HUD
    """

    hud = ObjectProperty("")

    def __init__(self, *args, **kwargs):
        BorderedLabel.__init__(self, *args, **kwargs)
        Clock.schedule_interval(self.get_lnd_data, 60)
        Clock.schedule_once(self.get_lnd_data, 1)

    @guarded
    def get_lnd_data(self, *args):
        @mainthread
        def update_gui(text):
            self.hud = text
            self.show()

        @guarded
        def func():
            lnd = data_manager.data_man.lnd
            bal = lnd.get_balance()
            tot = int(bal.total_balance)
            conf = int(bal.confirmed_balance)
            unconf = int(bal.unconfirmed_balance)
            pending_channels = lnd.get_pending_channels()
            pending_open = sum(
                channel.channel.local_balance
                for channel in pending_channels.pending_open_channels
            )

            hud = f"Chain Balance: {forex(tot)}\n"
            if tot != conf:
                hud += f"Conf. Chain Balance: {conf}\n"
                hud += f"Unconf. Chain Balance: {unconf}\n"

            cbal = lnd.channel_balance()
            hud += f"Local Balance: {forex(cbal.local_balance.sat)}\n"
            if cbal.unsettled_local_balance.sat:
                hud += f"Unset. Local B.: {forex(cbal.unsettled_local_balance.sat)}\n"
            if cbal.unsettled_remote_balance.sat:
                hud += f"Unset. Remote B.: {forex(cbal.unsettled_remote_balance.sat)}\n"
            hud += f"Remote Balance: {forex(cbal.remote_balance.sat)}\n"

            if pending_open:
                hud += f'Pending Open: {forex(pending_open)}\n'

            total = tot + int(
                int(cbal.local_balance.sat)
                + int(cbal.unsettled_remote_balance.sat)
                + int(pending_open)
            )

            hud += f"Total Balance: {forex(total)}"
            update_gui(hud)

        threading.Thread(target=func).start()


class HUD3(BorderedLabel):
    """
    DPI HUD
    """

    hud = ObjectProperty("")

    def __init__(self, *args, **kwargs):
        BorderedLabel.__init__(self, *args, **kwargs)
        from kivy.metrics import Metrics

        dpi_info = Metrics.dpi
        pixel_density_info = Metrics.density
        self.hud = f"DPI: {dpi_info}, Pixel Density: {pixel_density_info}"
        self.show()


class HUD4(FloatLayout, Hideable):
    """
    BTC Price HUD
    """

    line_points = ListProperty([])

    def __init__(self, *args, **kwargs):
        FloatLayout.__init__(self, *args, **kwargs)
        self.bind(pos=self.update_rect, size=self.update_rect)
        Clock.schedule_interval(self.update_price, 60)
        Clock.schedule_once(self.update_price, 1)

    @mainthread
    def update_gui(self, text, points):
        self.ids.rate.text = text
        if points:
            self.line_points = points
        self.show()

    @silent
    def update_rect(self, *args):
        @silent
        def func():
            # this probably shouldn't be in update_rect
            d = requests.get(
                "https://api.coindesk.com/v1/bpi/historical/close.json"
            ).json()['bpi']
            min_price, max_price, g = min(d.values()), max(d.values()), []
            for i, key in enumerate(d):
                g.append(i / len(d) * self.size[0])
                g.append(
                    ((d[key] - min_price) / (max_price - min_price)) * self.size[1]
                )
            rate = str(
                int(
                    requests.get(
                        "https://api.coindesk.com/v1/bpi/currentprice.json"
                    ).json()['bpi']['USD']['rate_float']
                )
            )
            self.update_gui(f'${rate}', g)

        threading.Thread(target=func).start()

    def update_price(self, *args):
        @silent
        def func():
            rate = int(
                requests.get(
                    "https://api.coindesk.com/v1/bpi/currentprice.json"
                ).json()['bpi']['USD']['rate_float']
            )
            self.update_gui(f'${rate}', None)

        threading.Thread(target=func).start()


class HUD5(BorderedLabel):
    hud = ObjectProperty("")

    def __init__(self, *args, **kwargs):
        BorderedLabel.__init__(self, *args, **kwargs)
        Clock.schedule_interval(self.get_fees, 60)
        Clock.schedule_once(self.get_fees, 1)

    def get_fees(self, *args):
        @mainthread
        def update_gui(text):
            self.hud = text
            self.show()

        @silent
        def func():
            fees = mempool.get_fees()
            text = f"""\
Low priority: {fees["hourFee"]} sat/vB
Medium priority: {fees["halfHourFee"]} sat/vB
High priority: {fees["fastestFee"]} sat/vB"""
            update_gui(text)

        threading.Thread(target=func).start()
