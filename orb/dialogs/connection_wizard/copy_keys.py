# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-06-10 09:17:49
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-06-12 13:31:10

import time
from threading import Thread
import codecs

from kivy.app import App
from kivy.clock import mainthread

from orb.misc.decorators import guarded
from orb.dialogs.connection_wizard.tab import Tab
from orb.misc.utils import pref
from orb.misc.fab_factory import Connection
from orb.misc.macaroon_secure import MacaroonSecure
from orb.misc.certificate_secure import CertificateSecure

from kivy.uix.textinput import TextInput


class CopyKeys(Tab):
    def __init__(self, *args, **kwargs):
        super(CopyKeys, self).__init__(*args, **kwargs)
        self.config = App.get_running_app().config

    def set_and_save(self, key, val):
        section, name = key.split(".")
        print(f"Setting: {section}, {name}")
        self.config.set(section, name, val)
        self.config.write()

    def copy_keys(self):
        print("Copying keys...")

        def func():
            with Connection() as c:
                print("Getting Macaroon")
                bin_data = c.run(
                    f"cat {pref('lnd.macaroon_admin_path')}", hide=True
                ).stdout
                hex_data = codecs.encode(bin_data.encode(), "hex")
                mac_secure = MacaroonSecure.init_from_plain(hex_data)
                self.set_and_save("lnd.macaroon", mac_secure.macaroon_secure.decode())
                print("Getting TLS Certificate")
                tls_cert = c.run(
                    f"cat {pref('lnd.tls_certificate_path')}", hide=True
                ).stdout
                cert_secure = CertificateSecure.init_from_plain(tls_cert)
                self.set_and_save(
                    "lnd.tls_certificate", cert_secure.cert_secure.decode()
                )
                if pref("lnd.protocol") == "mock":
                    self.set_and_save("lnd.protocol", "grpc")
                print("Done. Please restart Orb.")

        Thread(target=func).start()
