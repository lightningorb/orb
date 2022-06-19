# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-06-10 09:17:49
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-06-19 11:18:46

from threading import Thread
from tempfile import mkdtemp
from pathlib import Path
import codecs

from kivy.app import App

from orb.dialogs.connection_wizard.tab import Tab
from orb.misc.utils import pref
from orb.misc.fab_factory import Connection
from orb.misc.macaroon_secure import MacaroonSecure
from orb.misc.certificate_secure import CertificateSecure


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
                d = mkdtemp()
                mac_local = Path(d) / "admin.macaroon"
                print(f'Getting Macaroon from: {pref("lnd.macaroon_admin_path")}')
                c.get(pref("lnd.macaroon_admin_path"), mac_local.as_posix())
                with mac_local.open("rb") as f:
                    bin_data = f.read()
                hex_data = codecs.encode(bin_data, "hex")
                mac_secure = MacaroonSecure.init_from_plain(hex_data)
                self.set_and_save(
                    "lnd.macaroon_admin", mac_secure.macaroon_secure.decode()
                )
                print(
                    f"Getting TLS Certificate from: {pref('lnd.tls_certificate_path')}"
                )
                cert_local = Path(d) / "tls.cert"
                c.get(pref("lnd.tls_certificate_path"), cert_local.as_posix())
                with cert_local.open("rb") as f:
                    tls_cert = f.read().decode()
                cert_secure = CertificateSecure.init_from_plain(tls_cert)
                self.set_and_save(
                    "lnd.tls_certificate", cert_secure.cert_secure.decode()
                )
                if pref("lnd.protocol") == "mock":
                    self.set_and_save("lnd.protocol", "grpc")
                print("Done. Please restart Orb.")

        Thread(target=func).start()
