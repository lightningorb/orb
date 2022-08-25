# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-01-06 20:23:12
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-08-07 12:23:24

from orb.misc.plugin import Plugin
from kivymd.uix.button import MDFlatButton
from kivy.lang import Builder
from kivymd.uix.dialog import MDDialog
from pathlib import Path
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty

from orb.ln import Ln
from orb.misc.decorators import guarded


class KeysendDialogContent(BoxLayout):
    def update_alias(self, pk):
        try:
            self.ids.alias.text = Ln().get_node_alias(pk)
        except:
            self.ids.alias.text = "Could not find alias"


class KeysendDialog(MDDialog):
    def __init__(self):
        content = KeysendDialogContent()

        @guarded
        def send_tip(widget):
            print("sending")
            sats = int(content.ids.sats.text)
            recipient = content.ids.pubkey.text
            message = content.ids.message.text
            Ln().keysend(recipient, message, sats, 5, 60)

        super(KeysendDialog, self).__init__(
            content_cls=content,
            buttons=[
                MDFlatButton(
                    text="CANCEL", theme_text_color="Custom", on_release=self.dismiss
                ),
                MDFlatButton(
                    text="SEND", theme_text_color="Custom", on_release=send_tip
                ),
            ],
        )


class Keysend(Plugin):
    def main(self):
        kv_path = (Path(__file__).parent / "keysend.kv").as_posix()
        Builder.unload_file(kv_path)
        Builder.load_file(kv_path)
        KeysendDialog().open()
