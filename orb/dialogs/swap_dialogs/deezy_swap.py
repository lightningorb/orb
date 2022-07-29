# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-01-01 10:03:46
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-07-29 11:34:58

import threading

from kivy.clock import mainthread
from memoization import cached

from orb.components.popup_drop_shadow import PopupDropShadow
from orb.dialogs.swap_dialogs.deezy import Deezy, Network
from orb.misc.decorators import guarded
from orb.misc.mempool import get_fees
from orb.misc.utils import pref
from orb.lnd import Lnd


class PaymentUIOption:
    auto_first_hop = 0
    user_selected_first_hop = 1


class DeezySwapDialog(PopupDropShadow):
    def __init__(self, **kwargs):
        self.in_flight = set([])
        PopupDropShadow.__init__(self, **kwargs)
        self.chan_id = None
        self.inflight = set([])
        self.inflight_times = {}
        self.address = None

    def open(self):
        super(DeezySwapDialog, self).open()
        self.deezy = Deezy(
            mode=Network.testnet
            if pref("lnd.network") == "testnet"
            else Network.mainnet
        )

        def func():
            self.estimate_cost(self.ids.amount_sats.text)

        threading.Thread(target=func).start()
        self.ids.generate_invoice.disabled = True

    @cached(ttl=60)
    def get_fees(self):
        r = self.deezy.info()
        mp_fee = get_fees("halfHourFee")
        return r, mp_fee

    @guarded
    def estimate_cost(self, amount_sats: str, fee_rate: str = "500"):
        amount_sats, fee_rate = int(amount_sats), int(fee_rate)
        r, self.mp_fee = self.get_fees()

        @mainthread
        def update(disabled):
            self.ids.generate_invoice.disabled = disabled

        update(disabled=True)
        if self.deezy.amount_sats_is_above_max(amount_sats=amount_sats):
            print(f"Specified amount is too big, max: {r.max_swap_amount_sats}")
            return
        elif self.deezy.amount_sats_is_below_min(amount_sats=amount_sats):
            print(f"Specified amount is too small, min: {r.min_swap_amount_sats}")
            return
        estimate = self.deezy.estimate_cost(
            amount_sats=amount_sats, fee_rate=fee_rate, mp_fee=self.mp_fee
        )
        self.ids.cost_estimate.text = f"{estimate:,}"
        print(f"Fee estimate is: {self.ids.cost_estimate.text} Sats")
        update(disabled=not r.available)
        if not r.available:
            print("deezy.io is not currently availble!")

    @guarded
    def generate_invoice(self):
        from orb.store import model

        if not self.address:
            self.address = Lnd().new_address().address
        r = self.deezy.swap(
            amount_sats=int(self.ids.amount_sats.text),
            address=self.address,
            mp_fee=self.mp_fee,
        )
        req = Lnd().decode_payment_request(r.bolt11_invoice)
        invoice = model.Invoice(
            raw=r.bolt11_invoice,
            destination=req.destination,
            num_satoshis=req.num_satoshis,
            timestamp=req.timestamp,
            expiry=req.expiry,
            description=req.description,
        )
        invoice.save()
        print(f"Invoice generated: {invoice}")
