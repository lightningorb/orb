# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-08-08 20:31:17
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-08-20 12:07:45

import os
import shutil
from orb.logic.cron import Cron
from orb.misc.utils_no_kivy import platform
from orb.store.db_meta import *
from orb.misc.conf_defaults import set_conf_defaults
from orb.misc.utils_no_kivy import pref_path, pref
from orb.misc.monkey_patch import patch_store
from configparser import ConfigParser


class MockKivyConfigParser:
    def get(self, *args, fallback, **kwargs):
        return fallback


class AppMode:
    cli = 0
    ui = 1


class App:
    """
    This app could / should contain data that can be useful both
    from the kivy app and the CLI app.
    """

    running_app = None
    mode: AppMode = None
    pubkey: str = ""
    config = None
    ln = None
    channels = None
    title = "Orb"

    def __init__(self, mode: AppMode = AppMode.cli):
        self.mode = mode

    def run(self, pubkey: str):
        if not self.running_app:
            patch_store()
            App.running_app = self
            App.pubkey = pubkey
            App.config = ConfigParser()
            set_conf_defaults(App.config, MockKivyConfigParser())
            path = (
                Path(App._get_user_data_dir_static()) / f"orb_{pubkey}/orb_{pubkey}.ini"
            )
            App.config.read(path)

    def create_json_store(self):
        from kivy.storage.jsonstore import JsonStore

        App.store = JsonStore(
            Path(App()._get_user_data_dir()) / pref("path.json") / "orb.json"
        )

    def build(self, ln):
        from orb.misc.channels import Channels

        App.ln = ln
        self.make_dirs()
        self.create_tables()
        self.create_json_store()
        self.cron = Cron()
        App.channels = Channels(App.ln)

    def run_ui(self, config):
        if not self.running_app:
            App.running_app = self
            App.pubkey = config.get("ln", "identity_pubkey")
            App.config = config

    @staticmethod
    def get_running_app():
        if App.mode == AppMode.ui:
            from kivy.app import App as KivyApp

            return KivyApp.get_running_app()
        else:
            return App.running_app

    @property
    def user_data_dir(self):
        return (Path(App._get_user_data_dir_static()) / f"orb_{self.pubkey}").as_posix()

    def _get_user_data_dir(self):
        return App().user_data_dir

    @classmethod
    def _get_user_data_dir_static(cls):
        if platform == "win":
            data_dir = os.environ["APPDATA"]
        elif platform == "macosx":
            data_dir = os.path.expanduser(f"~/Library/Application Support/")
        else:
            data_dir = os.path.expanduser(
                os.path.join(os.environ.get("XDG_CONFIG_HOME", "~/.config"))
            )
        if not os.path.exists(data_dir):
            os.mkdir(data_dir)
        return data_dir

    def make_dirs(self):
        """
        Create data directories if required
        """
        for key in [
            "video",
            "yaml",
            "json",
            "db",
            "app",
            "backup",
            "export",
            "app_archive",
            "trash",
            "download",
        ]:
            path = pref_path(key)
            if not path.is_dir():
                os.makedirs(path)

        path = pref_path("cert")
        if not path.is_dir():
            os.makedirs(path)
        else:
            path = pref_path("cert")
            if (path / "tls.cert").is_file():
                print("Deleting cert from data dir, as it's no longer needed")
                shutil.rmtree(path.as_posix())

    def create_tables(self):
        from orb.store import db_create_tables

        dbs = [
            aliases_db_name,
            forwarding_events_db_name,
            invoices_db_name,
            htlcs_db_name,
            channel_stats_db_name,
            payments_db_name,
        ]
        for db in dbs:
            try:
                get_db(db).connect()
            except Exception as e:
                print(e)
                print(format_exc())
                print(f"issue connecting with: {db}")
                assert False

        db_create_tables.create_forwarding_tables()
        db_create_tables.create_aliases_tables()
        db_create_tables.create_invoices_tables()
        db_create_tables.create_htlcs_tables()
        db_create_tables.create_channel_stats_tables()
        db_create_tables.create_payments_tables()
        db_create_tables.create_path_finding_tables()

        for db in dbs:
            get_db(db).close()
