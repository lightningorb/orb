# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-01-06 20:26:07
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-01-07 07:43:59

from kivy.uix.popup import Popup
from kivy.uix.label import Label

from orb.lnd import Lnd
from orb.misc.plugin import Plugin


class AliasAndPubkey(Plugin):
    def main(self):
        lnd = Lnd()

        info = lnd.get_info()

        popup = Popup(
            title="Node Info",
            content=Label(
                text=f"Alias:\n\n{info.alias}\n\nPublic Key: \n\n{info.identity_pubkey}"
            ),
            size_hint=(None, None),
            size=(1200, 400),
        )
        popup.open()

    @property
    def menu(self):
        return "examples > alias and pubkey"

    @property
    def uuid(self):
        return "374759c0-4abf-4429-b9c7-acc44b67d04a"
