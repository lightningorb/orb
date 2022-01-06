# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-01-06 20:26:07
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-01-06 20:29:48

from kivy.uix.popup import Popup
from kivy.uix.label import Label
from orb.lnd import Lnd
from orb.misc.plugin import Plugin


Plugin().install(
    script_name="alias_and_pubkey.py",
    menu="examples > alias and pubkey",
    uuid="374759c0-4abf-4429-b9c7-acc44b67d04a",
)


def main():
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
