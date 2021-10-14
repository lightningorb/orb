from kivymd.app import MDApp
from main_layout import MainLayout
import data_manager
import json
from kivy.lang import Builder
from pathlib import Path


class OrbApp(MDApp):
    title = "Orb"

    def load_kvs(self):
        """
        This method enables splitting up .kv files,
        currently not used.
        """
        for path in [str(x) for x in Path(".").rglob("*.kv")]:
            if path != "orb.kv" and "tutes" not in path:
                Builder.load_file(path)

    def build(self):
        """
        Main build method for the app.
        """
        self.theme_cls.theme_style = "Dark"  # "Light"
        self.load_kvs()
        data_manager.data_man = data_manager.DataManager(config=self.config)
        print(self.config["debug"]["layouts"])
        print(type(self.config["debug"]["layouts"]))
        # self.theme_cls.primary_palette = "Red"
        # from lnd_rest import Lnd
        # lnd = Lnd()
        # lnd.get_balance()
        return MainLayout()

    def build_config(self, config):
        """
        Default config values.
        """
        config.add_section("lnd")
        config.set("lnd", "hostname", "localhost")
        config.set("lnd", "rest_port", "8080")
        config.set("lnd", "grpc_port", "10009")
        config.set("lnd", "protocol", "mock")
        config.set("lnd", "tls_certificate", "")
        config.set("lnd", "network", "mainnet")
        config.set("lnd", "macaroon_admin", "")
        config.add_section("debug")
        config.set("debug", "layouts", "0")

    def build_settings(self, settings):
        """
        Configuration screen for the app.
        """
        settings.add_json_panel(
            "Orb",
            self.config,
            data=json.dumps(
                [
                    {"type": "title", "title": "Connection Settings"},
                    {
                        "type": "string",
                        "title": "Host",
                        "desc": "The node's IP or domain, e.g 1.1.1.1",
                        "section": "lnd",
                        "key": "hostname",
                    },
                    {
                        "type": "string",
                        "title": "GRPC Port",
                        "desc": "The node's GRPC port, usually 10009",
                        "section": "lnd",
                        "key": "grpc_port",
                    },
                    {
                        "type": "string",
                        "title": "REST Port",
                        "desc": "The node's REST API port, usually 8080",
                        "section": "lnd",
                        "key": "rest_port",
                    },
                    {
                        "type": "options",
                        "title": "Network",
                        "desc": "Network to connect to",
                        "section": "lnd",
                        "key": "network",
                        "options": ["mainnet", "testnet"],
                    },
                    {
                        "type": "options",
                        "title": "API Protocol",
                        "desc": "Whether to use GRPC or REST",
                        "section": "lnd",
                        "key": "protocol",
                        "options": ["grpc", "rest", "mock"],
                    },
                    {
                        "type": "string",
                        "title": "Admin Macaroon",
                        "desc": "hex encoded macaroon: codecs.encode(..., 'hex')",
                        "section": "lnd",
                        "key": "macaroon_admin",
                    },
                    {
                        "type": "string",
                        "title": "tls certificate",
                        "desc": "plain-text TLS certificate",
                        "section": "lnd",
                        "key": "tls_certificate",
                    },
                    {
                        "type": "bool",
                        "title": "debug layouts",
                        "desc": "Display layouts for debugging purposes",
                        "section": "debug",
                        "key": "layouts",
                    },
                ]
            ),
        )

    def on_config_change(self, config, section, key, value):
        """
        What to do when a config value changes. TODO: needs fixing.
        Currently we'd end up with multiple LND instances for example?
        Simply not an option.
        """
        if key == "tls_certificate":
            data_manager.DataManager.save_cert(value)
        data_manager.data_man = data_manager.DataManager(config=self.config)
