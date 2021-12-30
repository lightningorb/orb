# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-15 07:15:28
# @Last Modified by:   lnorb.com
# @Last Modified time: 2021-12-31 06:17:27

from kivy.clock import Clock
import requests

from orb.components.popup_drop_shadow import PopupDropShadow
from orb.misc.decorators import guarded
from orb.lnd import Lnd


class SendCoins(PopupDropShadow):
    def __init__(self, *args, **kwargs):
        super(SendCoins, self).__init__()
        self.schedule = Clock.schedule_interval(self.get_fees, 10)
        Clock.schedule_once(self.get_fees, 1)

    @guarded
    def get_fees(self, *args):
        fees = requests.get("https://mempool.space/api/v1/fees/recommended").json()
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
    def send_coins(self, addr, amount, sat_per_vbyte):
        amount = int(amount)
        sat_per_vbyte = int(sat_per_vbyte)
        print(f"sending: {addr} {amount} {sat_per_vbyte}")
        out = Lnd().send_coins(addr, amount, sat_per_vbyte)
        print(out)
