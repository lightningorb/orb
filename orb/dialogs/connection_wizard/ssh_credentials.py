# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-06-10 06:35:32
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-07-15 14:40:07

from kivy.properties import StringProperty
from kivy.app import App
from kivy.metrics import dp

from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton

from orb.misc.sec_rsa import *
from orb.components.popup_drop_shadow import PopupDropShadow
from orb.dialogs.connection_wizard.tab import Tab
from orb.misc.fab_factory import Connection


class CertFileChooser(PopupDropShadow):

    selected_path = StringProperty("")


class SSHCredentials(Tab):
    def __init__(self, *args, **kwargs):
        super(SSHCredentials, self).__init__(*args, **kwargs)
        self.password_text_field = None
        self.certificate_text_field = None

    def cert_or_pass(self):
        """
        Callback for when the 'certificate / password' dropdown
        is modified.
        """
        if not self.password_text_field:
            self.password_text_field = MDTextField(
                text="",
                helper_text="Password",
                helper_text_mode="persistent",
                height=dp(60),
                width=dp(200),
                size_hint=(None, None),
            )
        if not self.certificate_text_field:
            self.certificate_text_field = MDTextField(
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
        widgets = {
            "certificate": self.certificate_text_field,
            "password": self.password_text_field,
        }
        self.ids.cert_or_pass.add_widget(widgets[self.ids.spinner_id.text])
        if self.ids.spinner_id.text == "certificate":
            self.ids.cert_or_pass.add_widget(self.load_from_disk)

    def load_cert_from_disk(self, *args):

        dialog = CertFileChooser()
        dialog.open()

        def do_ingest(widget, path):
            self.certificate_text_field.text = path

        dialog.bind(selected_path=do_ingest)

    def test_connection(self):
        with Connection(
            use_prefs=False,
            host=self.ids.address.text,
            port=self.ids.port.text,
            cert_path=self.certificate_text_field.text,
            auth=self.ids.spinner_id.text,
            username=self.ids.username.text,
            password=self.password_text_field.text,
        ) as connection:
            try:
                connection.run("uname -a")
                self.ids.test_connection.md_bg_color = [0.3, 1, 0.3, 1]
                self.ids.test_connection.text = "Success"
                self.save_ssh_creds()
            except Exception as e:
                print(e)
                self.ids.test_connection.md_bg_color = [1, 0.3, 0.3, 1]
                self.ids.test_connection.text = str(e)

    def save_ssh_creds(self):
        app = App.get_running_app()
        if self.ids.address.text:
            app.node_settings["host.hostname"] = self.ids.address.text
        if self.ids.port.text:
            app.node_settings["host.port"] = self.ids.port.text
        if self.ids.username.text:
            app.node_settings["host.username"] = self.ids.username.text
        if self.password_text_field.text:
            priv, pub = get_sec_keys()
            secret = encrypt(self.password_text_field.text.encode(), pub, True)
            app.node_settings["host.password"] = secret.decode("utf-8")
        if self.ids.spinner_id.text:
            app.node_settings["host.auth_type"] = self.ids.spinner_id.text
        if self.certificate_text_field.text:
            app.node_settings["host.certificate"] = self.certificate_text_field.text
