# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-15 07:15:28
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-01-03 07:43:18

import time

from kivy.clock import mainthread
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput

from orb.lnd import Lnd


class FocusTextInput(TextInput):
    def on_touch_down(self, touch):
        import data_manager

        if self.collide_point(*touch.pos):
            if data_manager.menu_visible:
                return False
        return super(FocusTextInput, self).on_touch_down(touch)


class MailScreen(Screen):
    def on_enter(self):
        text = ""
        for invoice in Lnd().list_invoices().invoices:
            if invoice.settled:
                htlc_records = [
                    htlc.custom_records for htlc in invoice.htlcs if htlc.custom_records
                ]
                if htlc_records:
                    text += f"{time.ctime(invoice.settle_date)}:\n\n"
                    for r in htlc_records:
                        if r.get(34349334, ""):
                            msg = str(r.get(34349334, "")).strip("b'")
                            try:
                                msg = r.get(34349334, "").decode()
                            except UnicodeDecodeError:
                                pass
                            if msg:
                                text += f"{msg}\n\n"
        self.ids.input.text = text
