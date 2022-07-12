# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-06-29 12:20:35
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-07-02 23:12:38

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
from orb.orb_connector import OrbConnector
from orb.core_ui.app_common import AppCommon
from orb.misc.utils import get_available_nodes
from orb.misc.macaroon_secure import MacaroonSecure


class OrbConnectorApp(AppCommon):
    data = {
        "LNDConnect URL": "alpha-u-circle-outline",
        "Voltage": "lightning-bolt-outline",
        "SSH Connection Wizard": "wizard-hat",
        "Manual Config": "cogs",
        "Import Connection Settings": "import",
        "Export Connection Settings": "export",
    }

    node_buttons = []
    node_settings = {}

    def add_public_testnet_node(self, *args):
        self.node_settings["host.hostname"] = "orb-public.t.voltageapp.io"
        self.node_settings["lnd.macaroon_admin"] = MacaroonSecure.init_from_plain(
            "0201036C6E6402F801030A102E2F33256E0173F3226178B99CC38AD01201301A160A0761646472657373120472656164120577726974651A130A04696E666F120472656164120577726974651A170A08696E766F69636573120472656164120577726974651A210A086D616361726F6F6E120867656E6572617465120472656164120577726974651A160A076D657373616765120472656164120577726974651A170A086F6666636861696E120472656164120577726974651A160A076F6E636861696E120472656164120577726974651A140A057065657273120472656164120577726974651A180A067369676E6572120867656E657261746512047265616400000620948B88E4F7ABB8F5CC0BD78FD31AAE9994809C29B8B704F86D893E6B850FFC82".encode()
        ).macaroon_secure.decode()
        self.node_settings["lnd.network"] = "testnet"
        self.node_settings["lnd.protocol"] = "rest"
        self.node_settings["lnd.rest_port"] = "8080"
        self.node_settings[
            "lnd.identity_pubkey"
        ] = "03373b5287484d081153491f674c023164c2343954e2f56e4ae4b23e686d8cf07d"
        self.stop()

    @guarded
    def update_node_buttons(self):
        grid = self.screen.ids.sm.get_screen("main").ids.grid
        has_nodes = False
        for b in self.node_buttons:
            grid.remove_widget(b)
        self.node_buttons = []
        for pk in get_available_nodes():

            def do_open(_, pk):
                self.node_settings["lnd.identity_pubkey"] = pk
                self.stop()

            def rm_node(_, pk, bl):
                p = Path(self._get_user_data_dir()).parent / f"orb_{pk}"
                if p.exists():
                    shutil.rmtree(p.as_posix())
                self.update_node_buttons()

            has_nodes = True
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
            bl.add_widget(button)
            self.node_buttons.append(bl)
            bl.add_widget(ib)
            grid.add_widget(bl)
        if not has_nodes:
            button = MDRaisedButton(
                text=f"Open orb-public (testnet)",
                size_hint=[1, None],
                height=dp(40),
                md_bg_color=[79 / 255.0, 51 / 255.0, 95 / 255.0, 1],
                on_release=self.add_public_testnet_node,
            )
            grid.add_widget(button)
        filler = Widget()
        self.node_buttons.append(filler)
        grid.add_widget(filler)

    def build(self):
        if mobile:
            if "SSH Connection Wizard" in self.data:
                del self.data["SSH Connection Wizard"]
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
