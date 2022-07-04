# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-06-29 12:20:35
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-07-02 23:12:38

from collections import deque
from pathlib import Path
from functools import partial

from kivy.metrics import dp
from kivy.uix.widget import Widget
from kivy.storage.jsonstore import JsonStore
from kivy.clock import Clock

from orb.misc.utils import mobile
from orb.orb_connector import OrbConnector
from orb.core_ui.app_common import AppCommon
from orb.misc.utils import get_available_nodes
from orb.misc.macaroon_secure import MacaroonSecure
from orb.misc.macaroon import Macaroon


class OrbConnectorApp(AppCommon):
    # consumables = deque()
    data = {
        "LNDConnect URL": "alpha-u-circle-outline",
        "Voltage": "lightning-bolt-outline",
        "SSH Connection Wizard": "wizard-hat",
        "Manual Config": "cogs",
        "Import Connection Settings": "import",
        "Export Connection Settings": "export",
    }

    node_settings = {}

    def add_public_testnet_node(self, *args):
        self.node_settings["host.hostname"] = "orb-public.t.voltageapp.io"
        self.node_settings["lnd.macaroon_admin"] = MacaroonSecure.init_from_plain(
            "0201036C6E6402F801030A10B0219C29BC3F6CD202A1E387AB0334D91201301A160A0761646472657373120472656164120577726974651A130A04696E666F120472656164120577726974651A170A08696E766F69636573120472656164120577726974651A210A086D616361726F6F6E120867656E6572617465120472656164120577726974651A160A076D657373616765120472656164120577726974651A170A086F6666636861696E120472656164120577726974651A160A076F6E636861696E120472656164120577726974651A140A057065657273120472656164120577726974651A180A067369676E6572120867656E65726174651204726561640000062036C21B1B8870B718022781C8AE926972600D51D17ACA3EDAA5DB6EE941AFB8B9".encode()
        ).macaroon_secure.decode()
        self.node_settings["lnd.network"] = "testnet"
        self.node_settings["lnd.protocol"] = "rest"
        self.node_settings["lnd.rest_port"] = "8080"
        self.node_settings[
            "lnd.identity_pubkey"
        ] = "0275788cdc494266908729e47056c1175ba536d41c38a7e32f525d518942511f85"
        self.stop()

    def on_main_enter(self):
        from pathlib import Path
        from kivymd.uix.button import MDRaisedButton

        grid = self.screen.ids.sm.get_screen("main").ids.grid
        has_nodes = False
        for pk in get_available_nodes():

            def do_open(button, pk):
                self.node_settings["lnd.identity_pubkey"] = pk
                self.stop()

            has_nodes = True
            button = MDRaisedButton(
                text=f"Open {pk[:5]}",
                size_hint=[1, None],
                height=dp(40),
                md_bg_color=[79 / 255.0, 51 / 255.0, 95 / 255.0, 1],
                on_release=partial(do_open, pk=pk),
            )
            grid.add_widget(button)
        if not has_nodes:
            button = MDRaisedButton(
                text=f"Open orb-public (testnet)",
                size_hint=[1, None],
                height=dp(40),
                md_bg_color=[79 / 255.0, 51 / 255.0, 95 / 255.0, 1],
                on_release=self.add_public_testnet_node,
            )
            grid.add_widget(button)
        grid.add_widget(Widget())

    def build(self):
        # if mobile:
        # if "SSH Connection Wizard" in self.data:
        # del self.data["SSH Connection Wizard"]
        self.store = JsonStore(Path(self._get_user_data_dir()) / "orb.json")
        self.override_stdout()
        self.load_kvs()
        self.screen = OrbConnector()
        self.on_main_enter()
        self.theme_cls.theme_style = "Dark"
        self.interval = Clock.schedule_interval(self.screen.ids.sm.get_screen('console').consume, 0)
        return self.screen

    def stop(self):
        Clock.unschedule(self.interval)
        super(OrbConnectorApp, self).stop()