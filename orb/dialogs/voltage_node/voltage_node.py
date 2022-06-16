# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-15 07:15:28
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-06-15 07:01:44

from threading import Thread

from kivy.app import App

from orb.misc.decorators import guarded
from orb.components.popup_drop_shadow import PopupDropShadow
from orb.misc.utils import pref
from orb.misc.macaroon import Macaroon
from orb.misc.macaroon_secure import MacaroonSecure


class VoltageNode(PopupDropShadow):
    def open(self, *args):
        self.config = App.get_running_app().config
        super(VoltageNode, self).open(self, *args)
        self.sec = None

    @guarded
    def get_cert(self):
        str_cert = pref("lnd.macaroon_admin").encode()
        if str_cert:
            cert = MacaroonSecure(str_cert)
            return cert.as_plain_macaroon().macaroon or ""
        return ""

    @guarded
    def validate_cert(self, text):
        mac = Macaroon.init_from_str(text)
        print(mac.debug())
        if mac.is_well_formed():
            self.sec = MacaroonSecure.init_from_plain(mac.macaroon.encode())

    @guarded
    def save(self):
        if self.sec:
            self.set_and_save("lnd.macaroon_admin", self.sec.macaroon_secure.decode())
        self.set_and_save("host.hostname", self.ids.address.text)
        self.set_and_save("lnd.tls_certificate", "")
        self.set_and_save("lnd.network", self.ids.network.text)
        self.set_and_save("lnd.protocol", "rest")
        self.set_and_save("lnd.rest_port", "8080")
        print("Saved - please restart Orb")

    def set_and_save(self, key, val):
        self.config = App.get_running_app().config
        section, name = key.split(".")
        self.config.set(section, name, val)
        self.config.write()
