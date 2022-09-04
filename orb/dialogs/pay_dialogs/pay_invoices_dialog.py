# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-01-01 10:03:46
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-09-04 13:33:54

import threading

from kivy.clock import mainthread

from orb.app import App
from orb.ln import Ln
from orb.logic.pay_invoices import PayInvoices
from orb.components.popup_drop_shadow import PopupDropShadow


class PayInvoicesDialog(PopupDropShadow):
    def __init__(self, **kwargs):
        PopupDropShadow.__init__(self, **kwargs)
        self.chan_id = None
        app = App.get_running_app()
        channels = app.channels

        @mainthread
        def delayed(chans_pk):
            self.ids.spinner_id.values = chans_pk

        def func():
            ln = Ln()
            chans_pk = [
                f"{c.chan_id}: {ln.get_node_alias(c.remote_pubkey)}" for c in channels
            ]
            delayed(chans_pk)

        threading.Thread(target=func).start()

    def first_hop_spinner_click(self, chan):
        self.chan_id = chan.split(":")[0]

    def pay(self):
        self.pay_invoices = PayInvoices(
            chan_id=self.chan_id,
            max_paths=int(self.ids.max_paths.text),
            fee_rate=int(self.ids.fee_rate.text),
            time_pref=float(self.ids.time_pref.value),
            num_threads=int(self.ids.num_threads.text),
            ln=Ln(),
        )
        self.pay_invoices.start()
