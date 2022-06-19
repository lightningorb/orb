# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-06-18 12:39:39
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-06-18 15:26:14

from orb.misc.macaroon_secure import MacaroonSecure
from orb.misc.certificate_secure import CertificateSecure
import codecs

from threading import Thread

from kivy.app import App

from orb.misc.decorators import guarded
from orb.components.popup_drop_shadow import PopupDropShadow
from orb.misc.utils import pref
from orb.misc.macaroon import Macaroon
from orb.misc.macaroon_secure import MacaroonSecure
from orb.misc.lndconnect_url import decode_ln_url


class UmbrelNode(PopupDropShadow):
    def open(self, *args):
        self.config = App.get_running_app().config
        super(UmbrelNode, self).open(self, *args)

    @guarded
    def save(self):
        url = self.ids.lndurl.text

        host, cert, mac = decode_ln_url(url)

        mac_hex_data = codecs.encode(mac, "hex")
        mac_secure = MacaroonSecure.init_from_plain(mac_hex_data)
        mac = mac_secure.macaroon_secure.decode()

        cert_secure = CertificateSecure.init_from_plain(cert)
        cert = cert_secure.cert_secure.decode()

        self.set_and_save("lnd.macaroon_admin", mac)
        self.set_and_save("host.hostname", host)
        self.set_and_save("lnd.tls_certificate", cert)
        self.set_and_save("lnd.network", "mainnet")
        self.set_and_save("lnd.protocol", "grpc")
        self.set_and_save("lnd.rest_port", "8080")
        self.set_and_save("lnd.grpc_port", "10009")
        print("Saved - please restart Orb")

    def set_and_save(self, key, val):
        self.config = App.get_running_app().config
        section, name = key.split(".")
        self.config.set(section, name, val)
        self.config.write()
