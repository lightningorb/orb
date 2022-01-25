# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-15 07:15:28
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-01-25 18:06:25


import base64
import binascii


from kivymd.uix.tab import MDTabsBase
from kivymd.uix.floatlayout import MDFloatLayout
from kivy.app import App
from kivy.core.clipboard import Clipboard

from orb.components.popup_drop_shadow import PopupDropShadow
from orb.misc.decorators import guarded
from orb.misc.utils import pref
from orb.misc.utils import mobile
from orb.misc.certificate import Certificate
from orb.misc.certificate_secure import CertificateSecure
from orb.misc.macaroon import Macaroon
from orb.misc.macaroon_secure import MacaroonSecure
from orb.misc.sec_rsa import get_sec_keys, get_cert_command, get_mac_command


class Tab(MDFloatLayout, MDTabsBase):
    """Class implementing content for a tab."""


class ConnectionSettings(PopupDropShadow):
    def open(self, *args):

        self.config = App.get_running_app().config
        self.ids.grpc.disabled = mobile

        super(ConnectionSettings, self).open(self, *args)

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
        print(cert.cert)
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
        print(mac.macaroon.decode())
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
