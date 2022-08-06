# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-15 07:15:28
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-08-06 10:55:51

import os
import sys
import json
import shutil
from time import time
from pathlib import Path
from textwrap import dedent
from threading import Thread
from collections import deque
from importlib import __import__
from traceback import print_exc

from kivy.storage.jsonstore import JsonStore
from kivy.properties import NumericProperty
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
from kivy.properties import DictProperty
from kivy.properties import ListProperty
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.utils import platform
from kivy.config import Config
from kivy.lang import Builder
from kivy.clock import Clock

from orb.logic.cron import Cron
from orb.misc.utils import pref
from orb.misc.prefs import cert_path
from orb.logic import thread_manager
from orb.logic.app_store import Apps
from orb.misc.decorators import guarded
from orb.core.orb_logging import get_logger
from orb.core_ui.app_common import AppCommon
from orb.misc.utils import pref_path, desktop
from orb.core_ui.main_layout import MainLayout
from orb.audio.audio_manager import audio_manager
from orb.misc.conf_defaults import set_conf_defaults
from orb.dialogs.restart_dialog import RestartDialog

from traceback import format_exc

from kivy.properties import BooleanProperty
from kivy.properties import NumericProperty
from kivy.properties import StringProperty
from kivy.event import EventDispatcher

from orb.store.db_meta import *
from orb.misc.channels import Channels
from orb.lnd.lnd import Lnd


ios = platform == "ios"

main_logger = get_logger(__name__)
debug = main_logger.debug

if platform == "windows":
    Config.set("graphics", "multisamples", "0")

sys.path.append("orb/lnd/grpc_generate")
sys.path.append("orb/lnd")

is_dev = "main.py" in sys.argv[0]

try:
    from pytransform import get_license_info

    is_dev = False
except:
    pass

print(f"sys.argv[0] is {sys.argv[0]}")


class OrbApp(AppCommon):
    title = "Orb"
    selection = ObjectProperty(allownone=True)
    channels = ObjectProperty(allownone=True)
    update_channels_widget = NumericProperty()
    apps = None
    version = StringProperty("")
    window_size = []
    last_window_size_update = 0
    pubkey = StringProperty("")
    show_chords = BooleanProperty(False)
    menu_visible = BooleanProperty(False)
    disable_shortcuts = BooleanProperty(False)
    plugin_registry = DictProperty(False)
    show_chord = NumericProperty(0)
    chords_direction = NumericProperty(0)
    channels_widget_ux_mode = NumericProperty(0)
    highlighter_updated = NumericProperty(0)

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

        if desktop:
            # only bother creating the certs
            # directory on desktop, as on mobile it goes
            # into a temp directory (which belongs to the app
            # so is fairly secure)
            path = pref_path("cert")
            if not path.is_dir():
                os.makedirs(path)
        else:
            path = pref_path("cert")
            if (path / "tls.cert").is_file():
                print("Deleting cert from data dir, as it's no longer needed")
                shutil.rmtree(path.as_posix())

    def on_start(self):
        """
        Perform required tasks before app exists.
        """
        python_paths = self.config["path"]["PYTHONPATH"].split(";")
        for p in python_paths:
            sys.path.append(p)
        self.apps = Apps()
        self.apps.load_from_disk()
        self.apps.load_all_apps()

    def on_stop(self):
        """
        Perform required tasks before app exists.
        """
        if cert_path().is_file():
            print("Deleting TLS cert")
            os.unlink(cert_path().as_posix())
        thread_manager.thread_manager.stop_threads()

    def on_pause(self):
        """
        Perform required tasks before app goes on pause
        e.g saving to disk.
        """
        print("pausing")
        return True

    def on_resume(self):
        """
        Perform required tasks before app resumes
        e.g restoring data from disk.
        """
        print("resuming")
        print("fast forwarding events")
        self.main_layout.do_layout()

        def update_chans():
            print("updating channels")
            self.channels.get()
            print("channels updated")

        Thread(target=update_chans).start()
        return True

    def read_version(self):
        self.version = (
            (Path(__file__).parent.parent.parent / "VERSION").open().read().strip()
        )
        self.config["system"]["orb_version"] = self.version
        self.config.write()

    def update_things(self):
        """
        Sometimes things change from one version to another.
        """
        if (
            self.config["lnd"].get("hostname")
            and self.config["host"]["hostname"] == "localhost"
        ):
            self.config["host"]["hostname"] = self.config["lnd"]["hostname"]
        if (
            self.config["lnd"].get("type") != "default"
            and self.config["host"]["hostname"] == "default"
        ):
            self.config["host"]["type"] = self.config["lnd"]["type"]

    def check_window_size_changed(self, *_):
        if (
            self.window_size != Window.size
            and time() - self.last_window_size_update > 1_000
        ):
            print(Window.size)
            self.window_size = Window.size
            self.root.ids.sm.get_screen("channels").refresh()
            self.last_window_size_update = time()

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

    def build(self):
        """
        Main build method for the app.
        """
        Config.set("graphics", "window_state", "maximized")
        Config.set("graphics", "fullscreen", 0)
        if Window:
            Window.maximize()
        self.window_size = Window.size
        self.last_window_size_update = time()
        Window.bind(size=self.check_window_size_changed)
        debug("overriding stdout")
        self.override_stdout()
        debug("overriding make_dirs")
        self.make_dirs()
        debug("creating json store")
        self.store = JsonStore(
            Path(self._get_user_data_dir()) / pref("path.json") / "orb.json"
        )
        debug("loading kvs")
        self.load_kvs()
        debug("reading version")
        self.read_version()
        debug("updating things")
        self.update_things()
        debug("loading data manager")
        self.lnd = Lnd()
        try:
            self.pubkey = self.lnd.get_info().identity_pubkey
        except:
            print(format_exc())
            print("Error getting pubkey")
        self.channels = Channels(self.lnd)
        debug("setting theme")
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = self.config["display"]["primary_palette"]
        self.icon = "orb.png"
        debug("loading main layout")
        self.main_layout = MainLayout()

        Clock.schedule_interval(
            self.main_layout.ids.sm.get_screen("console").consume, 0
        )
        self.create_tables()
        debug("showing license info")
        self.show_licence_info()
        debug("setting up cron")
        self.cron = Cron()
        debug("returning main layout")
        return self.main_layout

    def on_config_change(self, config, section, key, value):
        if [section, key] == ["debug", "htlcs"]:
            self.update_channels_widget += 1

        self.main_layout.do_layout()

    def show_licence_info(self):
        try:
            from pytransform import get_license_info
            import arrow

            a = (
                arrow.get(get_license_info()["EXPIRED"], "MMM DD HH:mm:ss YYYY")
                - arrow.utcnow()
            )
            if a.days == 0:
                print("Your license is expired.")
            else:
                print(
                    f"Your license is valid for another {a.days} day{'s' if a.days > 1 else ''}"
                )
        except:
            pass

    def run(self, node_config):
        self.node_config = node_config
        super(OrbApp, self).run()

    def build_config(self, config):
        """
        Default config values.
        """
        set_conf_defaults(config, self.node_config)

    def build_settings(self, settings):
        """
        Configuration screen for the app.
        """
        path = Path(__file__).parent.parent.parent / "orb/misc/settings.json"
        print(f"Settings file: {path.as_posix()}")
        settings.add_json_panel("Orb", self.config, filename=path.as_posix())

    def connector(self):
        """
        Clear connector autostart settings so it runs on next start
        """
        from kivymd.uix.dialog import MDDialog
        from kivymd.uix.button import MDFlatButton

        def func(*_):
            conf_path = (
                Path(self._get_user_data_dir()) / "../orbconnector/orbconnector.ini"
            )
            if conf_path.exists():
                os.unlink(conf_path.as_posix())
                self.stop()

        dialog = MDDialog(
            title="Please click 'Quit' and restart Orb to use connector",
            buttons=[
                MDFlatButton(
                    text="Cancel",
                    theme_text_color="Custom",
                    text_color=self.theme_cls.primary_color,
                    on_release=lambda x: dialog.dismiss(),
                ),
                MDFlatButton(
                    text="Quit",
                    theme_text_color="Custom",
                    text_color=self.theme_cls.primary_color,
                    on_release=func,
                ),
            ],
        )

        dialog.open()
