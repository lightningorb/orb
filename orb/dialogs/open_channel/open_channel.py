# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-15 07:15:28
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-08-08 09:55:01

from kivy.uix.textinput import TextInput
from kivy.metrics import dp

from orb.components.popup_drop_shadow import PopupDropShadow
from orb.misc.decorators import guarded
from orb.misc.utils import pref
from orb.ln import Ln


class OpenChannel:
    def __init__(self):
        self.impl = dict(cln=CLNOpenChannel, lnd=LNDOpenChannel)[pref("host.type")]()

    def open(self):
        self.impl.open()


class CLNOpenChannel(PopupDropShadow):
    @guarded
    def open_channel(self, chan_id: str, satoshis: str, fee_rate: str):
        out = Ln().open_channel(
            id=chan_id,
            fee_rate=fee_rate,
            satoshis=int(satoshis),
        )
        popup = PopupDropShadow(
            title="Open Channel Result", size_hint=(None, None), size=(dp(200), dp(200))
        )
        popup.add_widget(TextInput(text=str(out)))
        popup.open()
        print(out)


class LNDOpenChannel(PopupDropShadow):
    @guarded
    def open_channel(self, pk, sats, sats_per_vbyte):
        out = Ln().open_channel(
            node_pubkey_string=pk,
            sat_per_vbyte=int(sats_per_vbyte),
            amount_sat=int(sats),
        )
        popup = PopupDropShadow(
            title="Open Channel Result", size_hint=(None, None), size=(dp(200), dp(200))
        )
        popup.add_widget(TextInput(text=str(out)))
        popup.open()
        print(out)
