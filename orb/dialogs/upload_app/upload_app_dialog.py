# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-01-19 03:26:09
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-07-13 15:07:34

import base64
import time
from threading import Thread

from kivy.app import App
from kivy.uix.textinput import TextInput
from kivy.properties import StringProperty
from kivy.clock import mainthread
from kivy.metrics import dp
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.list import OneLineIconListItem

from orb.lnd import Lnd
from orb.components.popup_drop_shadow import PopupDropShadow
from orb.logic.upload_app import UploadApp


class AppFileChooser(PopupDropShadow):

    selected_path = StringProperty("")


class IconListItem(OneLineIconListItem):
    icon = StringProperty()


class UploadAppDialog(PopupDropShadow):
    def open(self, *args):
        super(UploadAppDialog, self).open(self, *args)
        self.app = None
        self.upload_app = None

        # phew!
        apps = App.get_running_app().apps.apps

        menu_items = [
            {
                "viewclass": "IconListItem",
                "icon": "application",
                "text": app.name,
                "height": dp(56),
                "on_release": lambda x=app: self.set_item(x),
            }
            for app in apps.values()
        ]
        self.menu = MDDropdownMenu(
            caller=self.ids.drop_item,
            items=menu_items,
            position="center",
            width_mult=4,
        )
        self.menu.bind()

    def set_item(self, app):
        self.ids.upload_button.disabled = True
        self.ids.archive_button.disabled = True
        self.ids.drop_item.text = app.name

        self.menu.dismiss()
        self.sprint(f"App selected: {app.name}")
        self.sprint("Checking...")
        self.upload_app = UploadApp(app)
        validation = self.upload_app.validate_for_upload()
        if validation == "ok":
            self.sprint("App is valid for archive creation")
            self.ids.archive_button.disabled = False
        else:
            self.sprint(validation)
            return

    def sprint(self, txt):
        self.ids.output.text += f"{txt}\n"

    def sign(self):
        self.menu.dismiss()
        self.upload_app.sign()

    def archive(self):
        self.sprint("Starting archiving")
        self.menu.dismiss()
        if self.upload_app.zip():
            self.sprint("App is valid for uplading to the app-store")
            self.ids.upload_button.disabled = False
        else:
            self.sprint("Archive creation failed")
            self.ids.upload_button.disabled = True

    def upload(self):
        self.sprint("Starting archive upload")
        self.menu.dismiss()
        ret = self.upload_app.upload()
        self.sprint(str(ret))
        self.sprint("Archive uploaded")
