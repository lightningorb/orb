# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-01-20 16:08:36
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-08-07 14:09:59


from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog

from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty

from orb.ln import Ln
from orb.misc.decorators import guarded


class TipDialogContent(BoxLayout):
    app = ObjectProperty()


class TipDialog(MDDialog):
    def __init__(self, app):
        content = TipDialogContent(app=app)

        @guarded
        def send_tip(widget):
            print("sending tip")
            sats = int(content.ids.sats.text)
            Ln().keysend(app.author, content.ids.message.text, sats, 5, 60)

        super(TipDialog, self).__init__(
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
