# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-06-30 14:26:36
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-09-13 15:45:41

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
        from orb.misc import utils_no_kivy

        d = mkdtemp()
        p = (
            Path(utils_no_kivy.get_user_data_dir_static())
            / "orbconnector/orbconnector_tmp.ini"
        )
        with p.open("w") as f:
            f.write(self.ids.text_import.text)

    @guarded
    def connect(self):
        from orb.misc import utils_no_kivy

        app = App.get_running_app()
        config = ConfigParser()
        config_path = (
            Path(utils_no_kivy.get_user_data_dir_static())
            / "orbconnector/orbconnector_tmp.ini"
        )
        config.read(config_path.as_posix())
        if self.connected:
            rd = RestartDialog(
                title="After exit, please restart Orb to launch new settings."
            )

            def save_and_quit(*args):
                config_path.rename(config_path.parents[0] / "orbconnector.ini")
                from kivy.app import App

                if App.get_running_app():
                    App.get_running_app().stop()

            rd.buttons[-1].on_release = save_and_quit
            rd.open()
            return

        error = ""
        try:
            from orb.ln import Ln

            ln = Ln(
                fallback_to_mock=False,
                cache=False,
                use_prefs=False,
                hostname=config.get("host", "hostname"),
                node_type=config.get("host", "type"),
                protocol=config.get("ln", "protocol"),
                mac_secure=config.get("ln", "macaroon_admin"),
                cert_secure=config.get("ln", "tls_certificate"),
                rest_port=config.get("ln", "rest_port"),
                grpc_port=config.get("ln", "grpc_port"),
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
