# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-06-18 12:39:39
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-09-19 07:53:12

import codecs
from traceback import format_exc

from kivy.app import App
from kivymd.uix.screen import MDScreen

from orb.ln import Ln
from orb.misc.decorators import guarded
from orb.misc.lndconnect_url import decode_ln_url
from orb.misc.macaroon_secure import MacaroonSecure
from orb.dialogs.restart_dialog import RestartDialog
from orb.misc.certificate_secure import CertificateSecure

prot = {8080: "rest", 10009: "grpc"}


class UmbrelNode(MDScreen):
    connected = False

    def on_enter(self, *args):
        super(UmbrelNode, self).on_enter(self, *args)

    @guarded
    def get(self):
        url = self.ids.lndurl.text
        host, port, cert, mac = decode_ln_url(url)
        mac_hex_data = codecs.encode(mac, "hex")
        return host, port, mac_hex_data, cert

    @guarded
    def connect(self):
        if self.connected:
            rd = RestartDialog(
                title="After exit, please restart Orb to launch new settings."
            )

            app = App.get_running_app()

            def save_and_quit(*args):
                app.save_node_settings_to_config()
                app.stop()

            rd.buttons[-1].on_release = save_and_quit

            rd.open()
            return
        error = ""
        try:
            host, port, mac, cert = self.get()
        except:
            error = "Error parsing LNDConnect URL"

        if not error:
            try:
                mac_secure = MacaroonSecure.init_from_plain(mac)
                mac_encrypted = mac_secure.macaroon_secure.decode()
                cert_secure = CertificateSecure.init_from_plain(cert)
                cert_encrypted = cert_secure.cert_secure.decode()

                ln = Ln(
                    node_type="lnd",
                    fallback_to_mock=False,
                    cache=False,
                    use_prefs=False,
                    hostname=host,
                    protocol=prot[port],
                    mac_secure=mac_encrypted,
                    cert_secure=cert_encrypted,
                    rest_port=port,
                    grpc_port=port,
                )

                info = ln.get_info()

                self.ids.connect.text = f"Set {info.identity_pubkey[:5]} as default ..."
                self.connected = True
                self.ids.connect.md_bg_color = (0.2, 0.8, 0.2, 1)
                app = App.get_running_app()

                app.node_settings["ln.macaroon_admin"] = mac_encrypted
                app.node_settings["host.hostname"] = host
                app.node_settings["host.type"] = "lnd"
                app.node_settings["ln.tls_certificate"] = cert_encrypted
                app.node_settings["ln.protocol"] = prot[port]
                app.node_settings["ln.identity_pubkey"] = info.identity_pubkey
                app.node_settings[f"ln.{prot[port]}_port"] = str(port)
            except Exception as e:
                print(e)
                print(format_exc)
                error = "Error connecting to LND"

        if error:
            self.ids.connect.text = f"Error: {error}"
            self.ids.connect.md_bg_color = (0.8, 0.2, 0.2, 1)
