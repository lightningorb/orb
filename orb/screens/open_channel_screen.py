# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-15 07:15:28
# @Last Modified by:   lnorb.com
# @Last Modified time: 2021-12-31 05:47:11

from orb.components.popup_drop_shadow import PopupDropShadow

from orb.misc.decorators import guarded
from orb.lnd import Lnd


class OpenChannelScreen(PopupDropShadow):
    @guarded
    def open_channel(self, pk, sats, sats_per_vbyte):
        out = Lnd().open_channel(
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
