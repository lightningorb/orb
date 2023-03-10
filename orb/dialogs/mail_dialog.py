# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-15 07:15:28
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-08-10 18:38:40

import base64
import time
from threading import Thread

from kivy.uix.textinput import TextInput
from kivy.clock import mainthread

from orb.app import App
from orb.ln import Ln
from orb.misc.prefs import is_rest
from orb.misc.decorators import guarded, public_restrict
from orb.components.popup_drop_shadow import PopupDropShadow


class FocusTextInput(TextInput):
    def on_touch_down(self, touch):
        app = App.get_running_app()

        if self.collide_point(*touch.pos):
            if app.menu_visible:
                return False
        return super(FocusTextInput, self).on_touch_down(touch)


class MailDialog(PopupDropShadow):
    def open(self, *args):
        self.get_mail()
        super(MailDialog, self).open(self, *args)

    @guarded
    @public_restrict
    def get_mail(self):
        @mainthread
        def update(text):
            self.ids.input.text = text

        def func():
            text = ""
            for invoice in Ln().list_invoices().invoices:
                if invoice.settled:
                    htlc_records = [
                        htlc.custom_records
                        for htlc in invoice.htlcs
                        if htlc.custom_records
                    ]
                    if htlc_records:
                        for r in htlc_records:
                            keysend = r.get("34349334" if is_rest() else 34349334, "")
                            if keysend:
                                if is_rest():
                                    msg = base64.b64decode(keysend)
                                else:
                                    msg = str(keysend).strip("b'")
                                    try:
                                        msg = keysend.decode()
                                    except UnicodeDecodeError:
                                        pass
                                if msg:
                                    text += f"{time.ctime(invoice.settle_date)}:\n\n"
                                    text += f"{msg}\n\n"
            update(text)

        update("fetching...")
        Thread(target=func).start()
