# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-01-20 16:08:36
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-01-22 11:16:26

from threading import Thread

from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog

from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.properties import ObjectProperty

from orb.lnd import Lnd
from orb.misc.decorators import guarded
from orb.logic.app_store_authenticate import get_pasword, register, login, get_creds


class LoginDialogContent(BoxLayout):
    pk = StringProperty()
    password = StringProperty()
    token = StringProperty()

    def __init__(self, *args, **kwargs):
        super(LoginDialogContent, self).__init__(*args, **kwargs)

        def get_pk(*args):
            self.pk = Lnd().get_info().identity_pubkey

        def get_password(*args):
            self.password = get_pasword()

        Thread(target=get_pk).start()
        Thread(target=get_password).start()

        creds = get_creds()
        if "access_token" in creds:
            self.token = creds["access_token"]

    @guarded
    def register(self, *_):
        resp = register(username=self.pk, password=self.password)
        if resp and "access_token" in resp:
            self.token = resp["access_token"]

    @guarded
    def login(self, *_):
        resp = login(username=self.pk, password=self.password)
        if resp and "access_token" in resp:
            self.token = resp["access_token"]


class LoginDialog(MDDialog):
    def __init__(self):
        content = LoginDialogContent()

        super(LoginDialog, self).__init__(
            content_cls=content,
            buttons=[
                MDFlatButton(
                    text="CANCEL", theme_text_color="Custom", on_release=self.dismiss
                ),
                MDFlatButton(
                    text="REGISTER",
                    theme_text_color="Custom",
                    on_release=content.register,
                ),
                MDFlatButton(
                    text="LOGIN", theme_text_color="Custom", on_release=content.login
                ),
                MDFlatButton(
                    text="DONE", theme_text_color="Custom", on_release=self.dismiss
                ),
            ],
        )
