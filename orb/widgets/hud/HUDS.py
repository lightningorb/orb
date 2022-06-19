# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-15 07:15:28
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-06-19 11:09:06

import threading
import requests
import random
import time

from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.clock import mainthread
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ListProperty
from kivy.properties import ObjectProperty
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.app import App
from kivy.uix.image import AsyncImage

from orb.misc.prefs import is_rest
from orb.misc.decorators import silent, guarded
from orb.misc import mempool, data_manager
from orb.misc.forex import forex
from orb.logic.thread_manager import thread_manager
from orb.lnd import Lnd
from orb.misc.utils import desktop, pref
from orb.logic import licensing
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

    def get_lnd_data(self, *args):
        @mainthread
        def update_gui(text):
            self.hud = text
            self.show()

        @silent
        def func():
            fr = Lnd().fee_report()
            update_gui(
                f"Earned:\nDay: {forex(fr.day_fee_sum)}\nWeek"
                f" {forex(fr.week_fee_sum)}\nMonth:"
                f" {forex(fr.month_fee_sum)}"
            )

        threading.Thread(target=func).start()


class HUDSpentFeeSummary(BorderedLabel):
    """
    Spent Fee Summary HUD
    """

    hud = ObjectProperty("")

    def __init__(self, *args, **kwargs):
        BorderedLabel.__init__(self, *args, **kwargs)
        Clock.schedule_interval(self.get_spent_data, 60)
        Clock.schedule_once(self.get_spent_data, 1)

    def get_spent_data(self, *args):
        @mainthread
        def update_gui(text):
            self.hud = text
            self.show()

        @silent
        def func():
            from orb.store.model import LNDPayment

            today = (
                sum(
                    p.total_fees_msat
                    for p in LNDPayment().select().where(LNDPayment.today() == True)
                )
                / 1000
            )
            this_week = (
                sum(
                    p.total_fees_msat
                    for p in LNDPayment().select().where(LNDPayment.this_week() == True)
                )
                / 1000
            )
            this_month = (
                sum(
                    p.total_fees_msat
                    for p in LNDPayment()
                    .select()
                    .where(LNDPayment.this_month() == True)
                )
                / 1000
            )

            fr = Lnd().fee_report()
            update_gui(
                f"Spent:\nDay: {forex(today)}\nWeek"
                f" {forex(this_week)}\nMonth:"
                f" {forex(this_month)}"
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

    def get_lnd_data(self, *args):
        @mainthread
        def update_gui(text):
            self.hud = text
            self.show()

        @silent
        def func():
            lnd = Lnd()

            ##################
            # Get chain totals
            ##################
            chain_bal = lnd.get_balance()

            hud = f"Chain Balance: {forex(chain_bal.total_balance)}\n"
            if chain_bal.total_balance != chain_bal.confirmed_balance:
                hud += f"Conf. Chain Balance: {forex(chain_bal.confirmed_balance)}\n"
                hud += (
                    f"Unconf. Chain Balance: {forex(chain_bal.unconfirmed_balance)}\n"
                )

            ####################
            # Get channel totals
            ####################
            channel_bal = lnd.channel_balance()
            pending_channels = lnd.get_pending_channels()
            limbo_balance = pending_channels.total_limbo_balance
            pending_open = sum(
                [
                    x.channel.local_balance
                    for x in pending_channels.pending_open_channels
                ]
            )

            # pending_close = sum(
            #     [
            #         x.channel.local_balance
            #         for x in pending_channels.pending_close_channels
            #     ]
            # )

            hud += f"Local Balance: {forex(channel_bal.local_balance.sat)}\n"
            if channel_bal.unsettled_local_balance.sat:
                hud += f"Unset. Local B.: {forex(channel_bal.unsettled_local_balance.sat)}\n"
            if channel_bal.unsettled_remote_balance.sat:
                hud += f"Unset. Remote B.: {forex(channel_bal.unsettled_remote_balance.sat)}\n"
            hud += f"Remote Balance: {forex(channel_bal.remote_balance.sat)}\n"

            if limbo_balance:
                hud += f"Limbo balance: {forex(limbo_balance)}\n"

            if pending_open:
                hud += f"Pending Open: {forex(pending_open)}\n"

            # if pending_close:
            #     hud += f"Pending Close: {forex(pending_close)}\n"

            ln_on_chain = chain_bal.total_balance + int(
                int(channel_bal.local_balance.sat)
                + int(channel_bal.unsettled_remote_balance.sat)
                + int(limbo_balance)
            )

            hud += f"Local + Chain: {forex(ln_on_chain)}\n"
            hud += f"Total: {forex(ln_on_chain + int(channel_bal.remote_balance.sat))}"
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

    def on_release(self, *args):
        if not data_manager.data_man.menu_visible:
            self.thread.stop()
        return super(ThreadWidget, self).on_release(*args)


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
        """
        Initializer sets the timers.
        """
        Button.__init__(self, *args, **kwargs)
        Clock.schedule_interval(self.check_connection, 10)
        Clock.schedule_once(self.check_connection, 1)

    def on_press(self, *args, **kwargs):
        return True

    def on_release(self, *args, **kwargs):
        """
        Allow the switching of protocol if on desktop
        """

        if desktop and not data_manager.data_man.menu_visible:
            app = App.get_running_app()
            opt = {"rest": "grpc", "grpc": "rest"}
            app.config.set("lnd", "protocol", opt[pref("lnd.protocol")])
            app.config.write()
            self.text = pref("lnd.protocol")
            return False
        return super(HUDProtocol, self).on_release(*args, **kwargs)

    @guarded
    def check_connection(self, *_):
        """
        Function on timer that calls get_info. Kills the thread
        after a timeout, and updates the UI saying we're not
        connected.
        """
        import ctypes
        import time

        @mainthread
        def update_gui(text):
            self.text = text

        data = {"success": False, "prev_protocol": pref("lnd.protocol")}

        def func():
            def inner_func():
                data["success"] = False
                try:
                    Lnd().get_info()
                    if pref("lnd.protocol") != data["prev_protocol"]:
                        update_gui(f"connecting")
                    else:
                        update_gui(f"{pref('lnd.protocol')} connected")
                    data["success"] = True
                except:
                    data["success"] = False
                    update_gui(f"{pref('lnd.protocol')} offline")
                data["prev_protocol"] = pref("lnd.protocol")

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


class HUDUIMode(Button):
    """
    UI mode, i.e whether we are in free mode (pan, zoom etc.)
    or gestures mode.
    """

    modes = ["pan / zoom", "gestures"]

    def __init__(self, *args, **kwargs):
        """
        Initializer sets the timers.
        """
        Button.__init__(self, *args, **kwargs)

        self.text = self.modes[0]

        def update_text(widget, val):
            self.text = self.modes[val]

        data_manager.data_man.bind(channels_widget_ux_mode=update_text)

    def on_press(self, *args, **kwargs):
        return True

    def on_release(self, *args, **kwargs):
        """
        Allow the switching of protocol if on desktop
        """

        mode = data_manager.data_man.channels_widget_ux_mode
        data_manager.data_man.channels_widget_ux_mode = [1, 0][mode]


class HUDEvaluation(Label):
    def get_text(self):
        if licensing.is_trial():
            e = licensing.get_edition()
            e = e[0].upper() + e[1:]
            return f"Orb {e} Edition\nEvaluation Copy"
        else:
            return ""


class HUDBanner(AsyncImage):
    def __init__(self, *args, **kwargs):
        super(HUDBanner, self).__init__(*args, **kwargs)
        # if licensing.is_free() or licensing.is_trial():
        if True:
            self.last_motion = time.time()

            def on_motion(*_):
                self.last_motion = time.time()

            self.change_banner()
            Clock.schedule_interval(self.change_banner, 60)
            Window.bind(on_motion=on_motion)

    def change_banner(self, *_):
        if time.time() - self.last_motion < 60:
            self.source = f"https://lnorb.com/api/ads/any?time={random.random()}"
