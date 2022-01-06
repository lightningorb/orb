# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-15 07:15:28
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-01-06 15:24:03

import threading
import requests

from kivy.clock import mainthread
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ListProperty
from kivy.properties import ObjectProperty
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.clock import Clock

from orb.misc.decorators import silent, guarded
from orb.misc import mempool
from orb.misc.forex import forex
from orb.logic.thread_manager import thread_manager
from orb.lnd import Lnd
from orb.misc.utils import pref

import data_manager
from orb.widgets.hud.hud_common import Hideable, BorderedLabel


class HUDFeeSummary(BorderedLabel):
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
            fr = Lnd().fee_report()
            update_gui(
                f"Day: {forex(fr.day_fee_sum)}\nWeek"
                f" {forex(fr.week_fee_sum)}\nMonth:"
                f" {forex(fr.month_fee_sum)}"
            )

        threading.Thread(target=func).start()


class HUDBalance(BorderedLabel):
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
            bal = Lnd().get_balance()
            tot = int(bal.total_balance)
            conf = int(bal.confirmed_balance)
            unconf = int(bal.unconfirmed_balance)
            pending_channels = Lnd().get_pending_channels()
            pending_open = sum(
                channel.channel.local_balance
                for channel in pending_channels.pending_open_channels
            )
            pending_close = (
                sum(
                    channel.limbo_balance
                    for channel in pending_channels.pending_force_closing_channels
                )
                if hasattr(pending_channels, "pending_force_closing_channels")
                else 0
            )

            hud = f"Chain Balance: {forex(tot)}\n"
            if tot != conf:
                hud += f"Conf. Chain Balance: {forex(conf)}\n"
                hud += f"Unconf. Chain Balance: {forex(unconf)}\n"

            cbal = Lnd().channel_balance()
            hud += f"Local Balance: {forex(cbal.local_balance.sat)}\n"
            if cbal.unsettled_local_balance.sat:
                hud += f"Unset. Local B.: {forex(cbal.unsettled_local_balance.sat)}\n"
            if cbal.unsettled_remote_balance.sat:
                hud += f"Unset. Remote B.: {forex(cbal.unsettled_remote_balance.sat)}\n"
            hud += f"Remote Balance: {forex(cbal.remote_balance.sat)}\n"

            if pending_open:
                hud += f"Pending Open: {forex(pending_open)}\n"

            ln_on_chain = tot + int(
                int(cbal.local_balance.sat)
                + int(cbal.unsettled_remote_balance.sat)
                + int(pending_open)
            )

            tlv = ln_on_chain + int(cbal.remote_balance.sat)

            hud += f"Local + Chain: {forex(ln_on_chain)}\n"
            hud += f"Total: {forex(tlv)}"
            update_gui(hud)

        threading.Thread(target=func).start()


class HUDDPI(BorderedLabel):
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


class HUDBTCPrice(FloatLayout, Hideable):
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
            ).json()["bpi"]
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
                    ).json()["bpi"]["USD"]["rate_float"]
                )
            )
            self.update_gui(f"${rate}", g)

        threading.Thread(target=func).start()

    @silent
    def update_price(self, *args):
        @silent
        def func():
            rate = int(
                requests.get(
                    "https://api.coindesk.com/v1/bpi/currentprice.json"
                ).json()["bpi"]["USD"]["rate_float"]
            )
            self.update_gui(f"${rate}", None)

        threading.Thread(target=func).start()


class HUDMempool(BorderedLabel):
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


class ThreadWidget(Widget):
    thread = ObjectProperty(None, allownone=True)


class HUDThreadManager(GridLayout, Hideable):
    def __init__(self, *args, **kwargs):
        GridLayout.__init__(self, *args, cols=5, **kwargs)
        self.lock = threading.Lock()
        thread_manager.bind(threads=self.update_rect)
        self.show()

    @mainthread
    def update_rect(self, *args):
        with self.lock:
            self.clear_widgets()
            for t in thread_manager.threads:
                self.add_widget(ThreadWidget(thread=t))


class HUDProtocol(Button):
    """
    Connected HUD
    """

    def __init__(self, *args, **kwargs):
        Button.__init__(self, *args, **kwargs)
        Clock.schedule_interval(self.check_connection, 10)
        Clock.schedule_once(self.check_connection, 1)

    def on_release(self, *args, **kwargs):
        from kivy.app import App
        from orb.misc.prefs import is_rest

        app = App.get_running_app()
        app.config.set("lnd", "protocol", "grpc" if is_rest() else "rest")
        self.text = pref("lnd.protocol")

    @guarded
    def check_connection(self, *_):
        import ctypes
        import time

        @mainthread
        def update_gui(text):
            self.text = text

        data = {"success": False}

        def func():
            def inner_func():
                data["success"] = False
                try:
                    Lnd().get_info()
                    update_gui(f"{pref('lnd.protocol')} connected")
                    data["success"] = True
                except:
                    data["success"] = False
                    update_gui(f"{pref('lnd.protocol')} offline")

            thread = threading.Thread(target=inner_func)
            thread.start()
            time.sleep(5)
            if not data["success"]:
                update_gui(f"{pref('lnd.protocol')} offline")
                ctypes.pythonapi.PyThreadState_SetAsyncExc(
                    ctypes.c_long(thread.ident), ctypes.py_object(SystemExit)
                )

        threading.Thread(target=func).start()


class HUDGlobalRatio(BorderedLabel):
    """
    Global Ratio
    """

    def __init__(self, *args, **kwargs):
        BorderedLabel.__init__(self, *args, **kwargs)
        Clock.schedule_interval(self.check_connection, 60)
        Clock.schedule_once(self.check_connection, 1)

    @guarded
    def check_connection(self, *_):
        @mainthread
        def update_gui(text):
            self.text = text
            self.show()

        @guarded
        def func():
            channels = data_manager.data_man.channels
            update_gui(f"Global Ratio: {channels.global_ratio:.2f}")

        threading.Thread(target=func).start()
