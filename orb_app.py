from kivy.app import App
from main_layout import MainLayout
import data_manager
import json
from kivy.lang import Builder
from pathlib import Path


class OrbApp(App):
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
        self.load_kvs()
        data_manager.data_man = data_manager.DataManager(config=self.config)
        return MainLayout()

    def build_config(self, config):
        """
        Default config values.
        """
        config.add_section("lnd")
        config.set("lnd", "hostname", "localhost:10009")
        config.set("lnd", "tls_certificate", "")
        config.set("lnd", "network", "mainnet")
        config.set("lnd", "macaroon_admin", "")

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
                        "desc": "The node's FQDN:PORT, e.g localhost:10009",
                        "section": "lnd",
                        "key": "hostname",
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
                ]
            ),
        )

    def on_config_change(self, config, section, key, value):
        """
        What to do when a config value changes. TODO: needs fixing.
        Currently we'd end up with multiple LND instances for example?
        Simply not an option.
        """
        data_manager.data_man = data_manager.DataManager(config=self.config)
