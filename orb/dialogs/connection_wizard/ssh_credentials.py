# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-06-10 06:35:32
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-06-15 06:18:41

from kivy.properties import StringProperty
from kivy.app import App
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivy.metrics import dp

from orb.misc.sec_rsa import *
from orb.misc.utils import pref
from orb.components.popup_drop_shadow import PopupDropShadow
from orb.dialogs.connection_wizard.tab import Tab
from orb.misc.fab_factory import Connection


class CertFileChooser(PopupDropShadow):

    selected_path = StringProperty("")


class SSHCredentials(Tab):
    def __init__(self, *args, **kwargs):
        super(SSHCredentials, self).__init__(*args, **kwargs)
        self.password = None
        self.certificate = None

    def cert_or_pass(self):
        if not self.password:
            password = pref("host.password")
            if password:
                priv, pub = get_sec_keys()
                password = decrypt(password, priv)
            self.password = MDTextField(
                text=password,
                helper_text="Password",
                helper_text_mode="persistent",
                height=dp(60),
                width=dp(200),
                size_hint=(None, None),
            )
        if not self.certificate:
            self.certificate = MDTextField(
                text=pref("host.certificate"),
                helper_text="Certificate Path",
                helper_text_mode="persistent",
                height=dp(60),
                width=dp(200),
                size_hint=(None, None),
            )
        self.load_from_disk = MDRaisedButton(
            text="Find...",
            on_release=self.load_cert_from_disk,
            size_hint_x=None,
            width=dp(100),
            height=dp(40),
            md_bg_color=[0.3, 0.3, 0.3, 1],
        )

        self.ids.cert_or_pass.clear_widgets()
        widgets = {"certificate": self.certificate, "password": self.password}
        self.ids.cert_or_pass.add_widget(widgets[self.ids.spinner_id.text])
        if self.ids.spinner_id.text == "certificate":
            self.ids.cert_or_pass.add_widget(self.load_from_disk)

    def load_cert_from_disk(self, *args):

        dialog = CertFileChooser()
        dialog.open()

        def do_ingest(widget, path):
            self.certificate.text = path

        dialog.bind(selected_path=do_ingest)

    def test_connection(self):

        with Connection(
            use_prefs=False,
            host=self.ids.address.text,
            port=self.ids.port.text,
            cert_path=self.certificate.text,
            auth=self.ids.spinner_id.text,
            username=self.ids.username.text,
            password=self.password.text,
        ) as connection:
            try:
                connection.run("uname -a")
                self.ids.test_connection.md_bg_color = [0.3, 1, 0.3, 1]
                self.ids.test_connection.text = "Success"
            except Exception as e:
                print(e)
                self.ids.test_connection.md_bg_color = [1, 0.3, 0.3, 1]
                self.ids.test_connection.text = str(e)

    def save_ssh_creds(self):
        print("Saving")
        if self.ids.address.text:
            self.set_and_save("host.hostname", self.ids.address.text)
        if self.ids.port.text:
            self.set_and_save("host.port", self.ids.port.text)
        if self.ids.username.text:
            self.set_and_save("host.username", self.ids.username.text)
        if self.password.text:
            priv, pub = get_sec_keys()
            secret = encrypt(self.password.text.encode(), pub, True)
            self.set_and_save("host.password", secret.decode("utf-8"))
        if self.ids.spinner_id.text:
            self.set_and_save("host.auth_type", self.ids.spinner_id.text)
        if self.certificate.text:
            self.set_and_save("host.certificate", self.certificate.text)

    def set_and_save(self, key, val):
        self.config = App.get_running_app().config
        section, name = key.split(".")
        self.config.set(section, name, val)
        self.config.write()
