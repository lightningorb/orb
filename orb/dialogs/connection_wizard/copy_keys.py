# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-06-10 09:17:49
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-08-02 18:29:11

import codecs
from pathlib import Path
from threading import Thread
from tempfile import mkdtemp

from kivy.app import App

from orb.misc.decorators import guarded
from orb.misc.fab_factory import Connection
from orb.dialogs.connection_wizard.tab import Tab
from orb.misc.macaroon_secure import MacaroonSecure
from orb.dialogs.restart_dialog import RestartDialog
from orb.misc.certificate_secure import CertificateSecure


class CopyKeys(Tab):

    connected = False

    def __init__(self, *args, **kwargs):
        super(CopyKeys, self).__init__(*args, **kwargs)

    def copy_keys(self):
        print("Copying keys...")
        app = App.get_running_app()

        def func():
            with Connection(
                use_prefs=False,
                host=app.node_settings.get("host.hostname"),
                port=app.node_settings.get("host.port"),
                auth=app.node_settings.get("host.auth_type"),
                username=app.node_settings.get("host.username"),
                password=app.node_settings.get("host.password"),
                cert_path=app.node_settings.get("host.certificate"),
            ) as c:
                d = mkdtemp()
                mac_local = Path(d) / "admin.macaroon"
                print(
                    f'Getting Macaroon from: {app.node_settings.get("lnd.macaroon_admin_path")}'
                )
                c.get(
                    app.node_settings.get("lnd.macaroon_admin_path"),
                    mac_local.as_posix(),
                )
                with mac_local.open("rb") as f:
                    bin_data = f.read()
                hex_data = codecs.encode(bin_data, "hex")
                mac_secure = MacaroonSecure.init_from_plain(hex_data)
                app.node_settings[
                    "lnd.macaroon_admin"
                ] = mac_secure.macaroon_secure.decode()
                print(
                    f"Getting TLS Certificate from: {app.node_settings.get('lnd.tls_certificate_path')}"
                )
                cert_local = Path(d) / "tls.cert"
                c.get(
                    app.node_settings.get("lnd.tls_certificate_path"),
                    cert_local.as_posix(),
                )
                with cert_local.open("rb") as f:
                    tls_cert = f.read().decode()
                cert_secure = CertificateSecure.init_from_plain(tls_cert)
                app.node_settings[
                    "lnd.tls_certificate"
                ] = cert_secure.cert_secure.decode()
                app.node_settings["lnd.protocol"] = "rest"

        Thread(target=func).start()

    @guarded
    def connect(self):
        app = App.get_running_app()
        if self.connected:
            RestartDialog(
                title="After exit, please restart Orb to launch new settings."
            ).open()
            return
        error = ""
        try:
            from orb.lnd import Lnd

            lnd = Lnd(
                fallback_to_mock=False,
                cache=False,
                use_prefs=False,
                hostname=app.node_settings["host.hostname"],
                protocol=app.node_settings["lnd.protocol"],
                mac_secure=app.node_settings["lnd.macaroon_admin"],
                cert_secure=app.node_settings["lnd.tls_certificate"],
                rest_port=8080,
                grpc_port=10009,
            )

            info = lnd.get_info()

            self.ids.connect.text = f"Set {info.identity_pubkey[:5]} as default ..."
            self.connected = True
            app.node_settings["lnd.identity_pubkey"] = info.identity_pubkey
            self.ids.connect.md_bg_color = (0.2, 0.8, 0.2, 1)
        except Exception as e:
            print(e)
            error = "Error connecting to LND"

        if error:
            self.ids.connect.text = f"Error: {error}"
            self.ids.connect.md_bg_color = (0.8, 0.2, 0.2, 1)
