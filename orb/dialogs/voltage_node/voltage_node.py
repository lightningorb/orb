# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-15 07:15:28
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-08-02 17:38:14

from threading import Thread

from kivy.app import App

from orb.misc.macaroon import Macaroon
from kivymd.uix.screen import MDScreen
from orb.misc.decorators import guarded
from orb.misc.macaroon_secure import MacaroonSecure
from orb.dialogs.restart_dialog import RestartDialog


class VoltageNode(MDScreen):
    def on_enter(self, *args):
        super(VoltageNode, self).on_enter(self, *args)
        self.sec = None
        self.connected = False

    @guarded
    def validate_cert(self, text):
        mac = Macaroon.init_from_str(text)
        if mac.is_well_formed():
            self.sec = MacaroonSecure.init_from_plain(mac.macaroon.encode())

    @guarded
    def connect(self):
        app = App.get_running_app()

        if self.connected:
            RestartDialog(
                title="After exit, please restart Orb to launch new settings."
            ).open()
        error = ""
        if not error:
            try:
                from orb.lnd import Lnd

                lnd = Lnd(
                    fallback_to_mock=False,
                    cache=False,
                    use_prefs=False,
                    hostname=self.ids.address.text,
                    protocol="rest",
                    mac_secure=self.sec.macaroon_secure.decode(),
                    rest_port="8080",
                )

                info = lnd.get_info()

                self.ids.connect.text = f"Set {info.identity_pubkey[:5]} as default ..."
                self.connected = True
                self.ids.connect.md_bg_color = (0.2, 0.8, 0.2, 1)
                if self.sec:
                    app.node_settings[
                        "lnd.macaroon_admin"
                    ] = self.sec.macaroon_secure.decode()
                app.node_settings["host.hostname"] = self.ids.address.text
                app.node_settings["lnd.network"] = self.ids.network.text
                app.node_settings["lnd.protocol"] = "rest"
                app.node_settings["lnd.rest_port"] = "8080"
                app.node_settings["lnd.identity_pubkey"] = info.identity_pubkey
            except Exception as e:
                print(e)
                error = "Error connecting to LND"

        if error:
            self.ids.connect.text = f"Error: {error}"
            self.ids.connect.md_bg_color = (0.8, 0.2, 0.2, 1)
