# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-15 07:15:28
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-08-07 14:18:44

from kivy.metrics import dp
from kivy.clock import Clock
from kivy.uix.textinput import TextInput

from orb.components.popup_drop_shadow import PopupDropShadow
from orb.misc.decorators import guarded
from orb.misc.mempool import get_fees
from orb.ln import Ln


class SendCoins(PopupDropShadow):
    def __init__(self, *args, **kwargs):
        super(SendCoins, self).__init__()
        self.schedule = Clock.schedule_interval(self.get_fees, 10)
        Clock.schedule_once(self.get_fees, 1)

    @guarded
    def get_fees(self, *args):

        fees = get_fees()
        text = f"""\
        Low priority: {fees["hourFee"]} sat/vB\n
        Medium priority: {fees["halfHourFee"]} sat/vB\n
        High priority: {fees["fastestFee"]} sat/vB
        """
        self.ids.fees.text = text

    def dismiss(self, *args):
        Clock.unschedule(self.schedule)
        super(SendCoins, self).dismiss()

    @guarded
    def send_coins(self, addr, satoshi, sat_per_vbyte):
        satoshi = int(satoshi)
        sat_per_vbyte = int(sat_per_vbyte)
        print(f"sending: {satoshi} sats to {addr} at {sat_per_vbyte}")
        self.ids.send_button.disabled = True
        out = Ln().send_coins(addr, satoshi, sat_per_vbyte)
        popup = PopupDropShadow(
            title="Send Output", size_hint=(None, None), size=(dp(200), dp(200))
        )
        popup.add_widget(TextInput(text=str(out)))
        popup.open()
        print(out)
