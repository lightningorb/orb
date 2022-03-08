# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-01-06 20:26:07
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-01-18 07:58:46

from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

from orb.lnd import Lnd
from orb.misc.plugin import Plugin
from orb.components.popup_drop_shadow import PopupDropShadow


class AliasAndPubkey(Plugin):
    def main(self):
        lnd = Lnd()

        info = lnd.get_info()

        popup = PopupDropShadow(
            title="Node Info",
            content=TextInput(
                text=f"Alias:\n\n{info.alias}\n\nPublic Key: \n\n{info.identity_pubkey}"
            ),
            size_hint=(0.5, 0.5),
        )
        popup.open()
