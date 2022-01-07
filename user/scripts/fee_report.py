# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-01-06 20:14:38
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-01-07 07:59:20

from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.metrics import dp

from orb.lnd import Lnd
from orb.misc.plugin import Plugin


class FeeReport(Plugin):
    @property
    def menu(self):
        return "examples > fee report"

    @property
    def uuid(self):
        return "123b8e17-98da-4281-85c0-848385437a06"

    def main(self):
        lnd = Lnd()

        fr = lnd.fee_report()

        text = f"""
        Day: S{fr.day_fee_sum:,}\n
        Week S{fr.week_fee_sum:,}\n
        Month: S{fr.month_fee_sum:,}
        """

        Popup(
            title="Fee Report",
            content=Label(text=text),
            size_hint=(None, None),
            size=(dp(200), dp(200)),
        ).open()
