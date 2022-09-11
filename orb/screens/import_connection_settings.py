# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-06-30 14:26:36
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-09-05 16:23:13

from kivymd.uix.screen import MDScreen

import os

from pathlib import Path
from tempfile import mkdtemp

from kivy.app import App
from kivy.config import ConfigParser
from kivymd.uix.screen import MDScreen

from orb.misc.utils import mobile
from orb.misc.decorators import guarded
from orb.misc.utils import get_available_nodes
from orb.dialogs.restart_dialog import RestartDialog


class ImportConnectionSettings(MDScreen):

    connected = False

    ln_settings_to_copy = [
        "rest_port",
        "tls_certificate",
        "network",
        "protocol",
        "macaroon_admin",
        "identity_pubkey",
    ]

    @guarded
    def import_node_settings(self):
        d = mkdtemp()
        p = Path(d) / "orb.ini"
        with p.open("w") as f:
            f.write(self.ids.text_import.text)
        config = ConfigParser()
        config.read(p.as_posix())
        target_config = ConfigParser()
        pk = config["ln"]["identity_pubkey"]
        app = App.get_running_app()
        app.node_settings["host.hostname"] = config["host"]["hostname"]
        app.node_settings["host.type"] = config["host"]["type"]
        for s in self.ln_settings_to_copy:
            app.node_settings[f"ln.{s}"] = config["ln"][s]
        if mobile:
            app.node_settings["ln.protocol"] = "rest"

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
            from orb.ln import Ln

            ln = Ln(
                fallback_to_mock=False,
                cache=False,
                use_prefs=False,
                hostname=app.node_settings["host.hostname"],
                node_type=app.node_settings["host.type"],
                protocol=app.node_settings["ln.protocol"],
                mac_secure=app.node_settings["ln.macaroon_admin"],
                cert_secure=app.node_settings["ln.tls_certificate"],
                rest_port=app.node_settings["ln.rest_port"],
                grpc_port=10009,
            )

            info = ln.get_info()

            self.ids.connect.text = f"Set {info.identity_pubkey[:5]} as default ..."
            self.connected = True
            self.ids.connect.md_bg_color = (0.2, 0.8, 0.2, 1)
        except Exception as e:
            print(e)
            error = "Error connecting to ln"

        if error:
            self.ids.connect.text = f"Error: {error}"
            self.ids.connect.md_bg_color = (0.8, 0.2, 0.2, 1)
