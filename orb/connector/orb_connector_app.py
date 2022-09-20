# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-06-29 12:20:35
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-09-20 16:13:37

import shutil
from pathlib import Path
from collections import deque
from functools import partial

from kivy.metrics import dp
from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.storage.jsonstore import JsonStore

from kivymd.uix.button import MDIconButton
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout

from orb.misc.utils import mobile
from orb.misc.macaroon import Macaroon
from orb.misc.decorators import guarded
from orb.core_ui.app_common import AppCommon
from orb.misc.utils import get_available_nodes
from orb.misc.macaroon_secure import MacaroonSecure
from orb.dialogs.restart_dialog import RestartDialog
from orb.connector.orb_connector import OrbConnector
from orb.misc.certificate_secure import CertificateSecure
from orb.misc.conf_defaults import set_ln_defaults, set_host_defaults


class OrbConnectorApp(AppCommon):
    data = {
        "LNDConnect URL": "alpha-u-circle-outline",
        "Voltage": "lightning-bolt-outline",
        "Manual Config": "cogs",
        "Import Connection Settings": "import",
        "Export Connection Settings": "export",
    }

    node_buttons = []
    node_settings = {}

    def add_public_testnet_node(self, *args):
        self.node_settings["host.hostname"] = "signet.lnd.lnorb.com"
        self.node_settings["host.type"] = "lnd"
        self.node_settings["ln.macaroon_admin"] = MacaroonSecure.init_from_plain(
            "0201036c6e6402f801030a106fb784f1598e0ce2f89c050b98139c8e1201301a160a0761646472657373120472656164120577726974651a130a04696e666f120472656164120577726974651a170a08696e766f69636573120472656164120577726974651a210a086d616361726f6f6e120867656e6572617465120472656164120577726974651a160a076d657373616765120472656164120577726974651a170a086f6666636861696e120472656164120577726974651a160a076f6e636861696e120472656164120577726974651a140a057065657273120472656164120577726974651a180a067369676e6572120867656e6572617465120472656164000006205d186c6864b437cd5d723eef6d064eae85467e7913f876a8b49bfe962028a2e8".encode()
        ).macaroon_secure.decode()
        self.node_settings["ln.tls_certificate"] = CertificateSecure.init_from_plain(
            "-----BEGIN CERTIFICATE-----\nMIICOjCCAeCgAwIBAgIQE3My2g1g5yRsD35v2/4qfDAKBggqhkjOPQQDAjA4MR8w\nHQYDVQQKExZsbmQgYXV0b2dlbmVyYXRlZCBjZXJ0MRUwEwYDVQQDEww4NjBiYTVj\nNTQ3NzAwHhcNMjIwODIwMjE1MDQ1WhcNMjMxMDE1MjE1MDQ1WjA4MR8wHQYDVQQK\nExZsbmQgYXV0b2dlbmVyYXRlZCBjZXJ0MRUwEwYDVQQDEww4NjBiYTVjNTQ3NzAw\nWTATBgcqhkjOPQIBBggqhkjOPQMBBwNCAARRnSKy3uNVVrQXWhxEHoTXzwqCu4YC\ndSRDVqQyrJwR313Op0SChZZanZxigjFBKlapmQvNRy1IhNUxdkN2eTQ4o4HLMIHI\nMA4GA1UdDwEB/wQEAwICpDATBgNVHSUEDDAKBggrBgEFBQcDATAPBgNVHRMBAf8E\nBTADAQH/MB0GA1UdDgQWBBTu4yTg9J01l3rojEzSiDSd3RFwzzBxBgNVHREEajBo\nggw4NjBiYTVjNTQ3NzCCCWxvY2FsaG9zdIIUc2lnbmV0LmxuZC5sbm9yYi5jb22C\nBHVuaXiCCnVuaXhwYWNrZXSCB2J1ZmNvbm6HBH8AAAGHEAAAAAAAAAAAAAAAAAAA\nAAGHBKwWAAQwCgYIKoZIzj0EAwIDSAAwRQIgcwRSvTNqJPrV6xd+SFKZVg8AjIQw\njYcQ6dNQ0P9wTyECIQD4Vj3ac+b+35tVedYRX5sOJ7KWAEdHemwvl5OQS4Eg3w==\n-----END CERTIFICATE-----\n"
        ).cert_secure.decode()
        self.node_settings["ln.network"] = "signet"
        self.node_settings["ln.protocol"] = "rest"
        self.node_settings["ln.rest_port"] = "8080"
        self.node_settings[
            "ln.identity_pubkey"
        ] = "0227750e13a6134c1f1e510542a88e3f922107df8ef948fc3ff2a296fca4a12e47"
        rd = RestartDialog(
            title="After exit, please restart Orb to launch new settings."
        )

        def save_and_quit(*args):
            app.save_node_settings_to_config()
            app.stop()

        rd.buttons[-1].on_release = save_and_quit

        rd.open()

    @guarded
    def update_node_buttons(self):
        grid = self.screen.ids.sm.get_screen("main").ids.grid
        for b in self.node_buttons:
            grid.remove_widget(b)
        self.node_buttons = []

        def do_open(_, pk):
            self.node_settings["ln.identity_pubkey"] = pk
            p = (
                Path(self._get_user_data_dir()).parent
                / f"orbconnector/orbconnector.ini"
            )
            from kivy.config import ConfigParser

            rs = RestartDialog(
                title="After exit, please restart Orb to launch new settings."
            )

            def ok(*args):
                from kivy.app import App

                config = ConfigParser()
                config.add_section("ln")
                config.set("ln", "identity_pubkey", pk)
                config.filename = p.as_posix()
                print(p.as_posix())
                config.write()
                self.stop()

            rs.buttons[-1].on_release = ok
            rs.open()

        def rm_node(_, pk, bl):
            p = Path(self._get_user_data_dir()).parent / f"orb_{pk}"
            if p.exists():
                shutil.rmtree(p.as_posix())
            self.update_node_buttons()

        for pk in get_available_nodes():
            button = MDRaisedButton(
                text=f"Open {pk[:5]}",
                size_hint=[1, None],
                height=dp(40),
                md_bg_color=[79 / 255.0, 51 / 255.0, 95 / 255.0, 1],
                on_release=partial(do_open, pk=pk),
            )
            bl = MDBoxLayout(orientation="horizontal", size_hint_y=None, height=dp(50))
            ib = MDIconButton(
                icon="delete-forever", on_release=partial(rm_node, pk=pk, bl=bl)
            )
            bl.add_widget(ib)
            bl.add_widget(button)
            self.node_buttons.append(bl)
            grid.add_widget(bl)
        button = MDRaisedButton(
            text=f"Open orb-public (signet)",
            size_hint=[1, None],
            height=dp(40),
            md_bg_color=[79 / 255.0, 51 / 255.0, 95 / 255.0, 1],
            on_release=self.add_public_testnet_node,
        )
        bl = MDBoxLayout(orientation="horizontal", size_hint_y=None, height=dp(50))
        self.node_buttons.append(bl)
        ib = MDIconButton(
            icon="delete-forever",
            on_release=partial(
                rm_node,
                pk="0227750e13a6134c1f1e510542a88e3f922107df8ef948fc3ff2a296fca4a12e47",
                bl=bl,
            ),
        )
        bl.add_widget(ib)
        bl.add_widget(button)
        grid.add_widget(bl)
        filler = Widget()
        self.node_buttons.append(filler)
        grid.add_widget(filler)

    def build(self):
        self.store = JsonStore(Path(self._get_user_data_dir()) / "orb.json")
        self.override_stdout()
        self.load_kvs()
        self.screen = OrbConnector()
        self.update_node_buttons()
        self.theme_cls.theme_style = "Dark"
        self.interval = Clock.schedule_interval(
            self.screen.ids.sm.get_screen("console").consume, 0
        )
        return self.screen

    def stop(self):
        Clock.unschedule(self.interval)
        super(OrbConnectorApp, self).stop()

    def build_config(self, config):
        """
        Default config values.
        """
        config.add_section("host")
        config.add_section("ln")

    def save_node_settings_to_config(self):
        for section in self.config.sections():
            self.config.remove_section(section)
        for k, v in self.node_settings.items():
            section, option = k.split(".")
            if not self.config.has_section(section):
                self.config.add_section(section)
            self.config.set(section, option, v)
            self.config.write()
