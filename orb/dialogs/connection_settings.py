# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-15 07:15:28
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-06-23 05:52:34

from tempfile import mkdtemp
from pathlib import Path
import os

from kivy.app import App
from kivy.core.clipboard import Clipboard
from kivy.properties import StringProperty
from kivy.uix.spinner import SpinnerOption
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.floatlayout import MDFloatLayout
from kivy.config import ConfigParser

from orb.misc.decorators import guarded
from orb.components.popup_drop_shadow import PopupDropShadow
from orb.misc.decorators import guarded
from orb.misc.utils import mobile
from orb.misc.certificate_secure import CertificateSecure
from orb.misc.macaroon_secure import MacaroonSecure
from orb.misc.sec_rsa import get_sec_keys, get_cert_command, get_mac_command
from orb.misc.utils import pref


class TypeSpinnerOption(SpinnerOption):
    pass


class Tab(MDFloatLayout, MDTabsBase):
    """Class implementing content for a tab."""


class ConnectionSettings(PopupDropShadow):

    node_type = StringProperty("default")
    lnd_settings_to_copy = [
        "rest_port",
        "tls_certificate",
        "network",
        "macaroon_admin",
        "type",
    ]

    def open(self, *args):

        self.config = App.get_running_app().config
        self.ids.grpc.disabled = mobile

        super(ConnectionSettings, self).open(self, *args)

        self.ids.spinner_in_id.values = ["default", "umbrel"]

    def node_type_selected(self, val):
        self.node_type = val

    def set_and_save(self, key, val):
        section, name = key.split(".")
        print(f"Setting: {section}, {name}")
        self.config.set(section, name, val)
        self.config.write()

    def save_protocol(self, prot):
        self.set_and_save("lnd.protocol", prot)
        if prot == "mock" and self.ids.mock.active:
            self.ids.grpc.active = False
            self.ids.rest.active = False
        if prot == "rest" and self.ids.rest.active:
            self.ids.grpc.active = False
            self.ids.mock.active = False
        if prot == "grpc" and self.ids.grpc.active:
            self.ids.rest.active = False
            self.ids.mock.active = False

    def validate_cert(self, text):
        cert_secure = CertificateSecure.init_from_encrypted(text.encode())
        cert = cert_secure.as_plain_certificate()
        self.ids.feedback.text = cert.debug()

    def save_cert(self, text):
        key = "lnd.tls_certificate"
        cert_secure = CertificateSecure.init_from_encrypted(text.encode())
        cert = cert_secure.as_plain_certificate()
        if cert.is_well_formed():
            self.set_and_save(key, cert_secure.cert_secure.decode())
        else:
            self.ids.feedback.text = cert.debug()

    def get_cert(self):
        cert_secure = CertificateSecure.init_from_encrypted(
            pref("lnd.tls_certificate").encode()
        )
        cert = cert_secure.as_plain_certificate()
        if cert.is_well_formed():
            return cert_secure.cert_secure.decode()
        else:
            self.ids.feedback.text = cert.debug()
            return ""

    def get_macaroon(self):
        mac = MacaroonSecure.init_from_encrypted(pref("lnd.macaroon_admin").encode())
        return mac.macaroon_secure

    def save_macaroon(self, text):
        key = "lnd.macaroon_admin"
        mac_secure = MacaroonSecure.init_from_encrypted(text.encode())
        self.set_and_save(key, mac_secure.macaroon_secure.decode())

    def validate_macaroon(self, text):
        mac_secure = MacaroonSecure.init_from_encrypted(text.encode())
        mac = mac_secure.as_plain_macaroon()
        self.ids.mac_feedback.text = mac.debug()

    @guarded
    def on_tab_switch(self, instance_tabs, instance_tab, instance_tab_label, tab_text):
        if tab_text == "TLS Certificate":
            self.validate_cert(pref("lnd.tls_certificate"))
        if tab_text == "Macaroon":
            self.validate_macaroon(pref("lnd.macaroon_admin"))

    def copy_cert_encrypt_command(self):
        _, public_key = get_sec_keys()
        Clipboard.copy(get_cert_command(public_key))

    def copy_mac_encrypt_command(self):
        _, public_key = get_sec_keys()
        Clipboard.copy(get_mac_command(public_key))

    def export_node_settings(self):
        config = ConfigParser()
        config.adddefaultsection("host")
        config.adddefaultsection("lnd")
        config.setdefaults("host", {k: self.config["host"][k] for k in ["hostname"]})
        config.setdefaults(
            "lnd",
            {k: self.config["lnd"][k] for k in self.lnd_settings_to_copy},
        )
        cert_secure = CertificateSecure(self.config["lnd"]["tls_certificate"].encode())
        plain_cert = cert_secure.as_plain_certificate().cert
        cert_new_uid = CertificateSecure.init_from_plain(
            plain_cert, uid=int(self.ids.device_id.text)
        )
        config["lnd"]["tls_certificate"] = cert_new_uid.cert_secure.decode()

        mac_secure = MacaroonSecure(self.config["lnd"]["macaroon_admin"].encode())
        plain_mac = mac_secure.as_plain_macaroon().macaroon
        mac_new_uid = MacaroonSecure.init_from_plain(
            plain_mac, uid=int(self.ids.device_id.text)
        )
        config["lnd"]["macaroon_admin"] = mac_new_uid.macaroon_secure.decode()

        d = mkdtemp()
        p = Path(d) / "orb.ini"
        config.filename = p.as_posix()
        config.write()
        with p.open() as f:
            self.ids.text_export.text = f.read()
        os.unlink(p.as_posix())

    @guarded
    def import_node_settings(self):
        d = mkdtemp()
        p = Path(d) / "orb.ini"
        with p.open("w") as f:
            f.write(self.ids.text_export.text)
        config = ConfigParser()
        config.read(p.as_posix())
        os.unlink(p.as_posix())
        self.config["host"]["hostname"] = config["host"]["hostname"]
        for s in self.lnd_settings_to_copy:
            self.config["lnd"][s] = config["lnd"][s]
        self.config.write()
