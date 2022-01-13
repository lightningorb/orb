# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-15 07:15:28
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-01-13 08:09:11

from kivymd.uix.tab import MDTabsBase
from kivymd.uix.floatlayout import MDFloatLayout
from kivy.app import App

from orb.components.popup_drop_shadow import PopupDropShadow
from orb.misc.decorators import guarded
from orb.misc.utils import pref
from orb.misc.utils import mobile
from orb.misc.certificate import Certificate
from orb.misc.macaroon import Macaroon


class Tab(MDFloatLayout, MDTabsBase):
    """Class implementing content for a tab."""


class ConnectionSettings(PopupDropShadow):
    def open(self, *args):
        from data_manager import data_man

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
        cert = Certificate.init_from_not_sure(text)
        self.ids.feedback.text = cert.debug()

    def save_cert(self, text):
        key = "lnd.tls_certificate"
        cert = Certificate.init_from_not_sure(text)
        if cert.is_well_formed():
            self.set_and_save(key, cert.reformat())
        else:
            self.ids.feedback.text = cert.debug()

    def get_cert(self):
        cert = Certificate.init_from_str(pref("lnd.tls_certificate"))
        if cert.is_well_formed():
            return cert.reformat()
        else:
            self.ids.feedback.text = cert.debug()
            return ""

    def get_macaroon(self):
        mac = Macaroon.init_from_str(pref("lnd.macaroon_admin"))
        return mac.macaroon

    def save_macaroon(self, text):
        key = "lnd.macaroon_admin"
        mac = Macaroon.init_from_not_sure(text)
        self.set_and_save(key, mac.macaroon)

    def validate_macaroon(self, text):
        mac = Macaroon.init_from_not_sure(text)
        self.ids.mac_feedback.text = mac.debug()

    @guarded
    def on_tab_switch(self, instance_tabs, instance_tab, instance_tab_label, tab_text):
        if tab_text == "TLS Certificate":
            self.validate_cert(pref("lnd.tls_certificate"))
