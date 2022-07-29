# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-01-01 10:03:46
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-07-29 14:02:31

from orb.components.popup_drop_shadow import PopupDropShadow
from orb.logic.lnurl_invoice_generator import LNUrlInvoiceGenerator


class PaymentUIOption:
    auto_first_hop = 0
    user_selected_first_hop = 1


class PayLNURLDialog(PopupDropShadow):
    def __init__(self, **kwargs):
        self.in_flight = set([])
        PopupDropShadow.__init__(self, **kwargs)

    def generate_invoices(self):
        self.invoice_generator = LNUrlInvoiceGenerator(
            url=self.ids.lnurl.text,
            total_amount_sat=int(self.ids.sats.text),
            chunks=int(self.ids.chunks.text),
            num_threads=int(self.ids.num_threads.text),
            rate_limit=int(self.ids.rate_limit.text),
        )
        self.invoice_generator.start()
