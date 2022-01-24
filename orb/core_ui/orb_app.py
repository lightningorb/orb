# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-15 07:15:28
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-01-24 13:51:02

import os
import sys
import json
from pathlib import Path
from traceback import print_exc
from importlib import __import__
import shutil
from collections import deque

from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.utils import platform
from kivy.properties import ObjectProperty
from kivy.properties import ListProperty

from orb.logic.app_store import Apps
from orb.misc.monkey_patch import do_monkey_patching
from orb.misc.conf_defaults import set_conf_defaults
from orb.audio.audio_manager import audio_manager
from orb.misc.decorators import guarded
from orb.core_ui.main_layout import MainLayout
from orb.logic import thread_manager
from orb.misc.utils import pref_path, desktop

from orb.misc import data_manager

ios = platform == "ios"

sys.path.append("orb/lnd/grpc_generate")
sys.path.append("orb/lnd")

do_monkey_patching()
is_dev = "main.py" in sys.argv[0]


class OrbApp(MDApp):
    title = "Orb"
    consumables = deque()
    selection = ObjectProperty(allownone=True)
    apps = None

    def get_application_config(self, defaultpath=f"{os.getcwd()}/orb.ini"):
        """
        Get location of the orb.ini file. This may differ from
        one OS to the next.
        """
        if platform == "android":
            defaultpath = "/sdcard/.%(appname)s.ini"
        elif platform == "ios":
            defaultpath = "~/Documents/%(appname)s.ini"
        elif platform == "win":
            defaultpath = defaultpath.replace("/", "//")
        path = os.path.expanduser(defaultpath) % {
            "appname": self.name,
            "appdir": self.directory,
        }
        return path

    def _get_user_data_dir(self):
        data_dir = ""
        if platform == "ios":
            data_dir = os.path.expanduser("~/Documents")
        elif platform == "android":
            from jnius import autoclass, cast

            PythonActivity = autoclass("org.kivy.android.PythonActivity")
            context = cast("android.content.Context", PythonActivity.mActivity)
            file_p = cast("java.io.File", context.getFilesDir())
            data_dir = file_p.getAbsolutePath()
        elif platform == "win":
            data_dir = os.path.join(os.environ["APPDATA"], self.name)
        elif platform == "macosx":
            data_dir = os.path.expanduser(f"~/Library/Application Support/{self.name}")
        else:
            data_dir = os.path.expanduser(
                os.path.join(os.environ.get("XDG_CONFIG_HOME", "~/.config"), self.name)
            )
        if not os.path.exists(data_dir):
            os.mkdir(data_dir)
        return data_dir

    def load_kvs(self):
        for path in [str(x) for x in Path(".").rglob("*.kv")]:
            if any(
                x in path for x in ["kivy_garden", "build/", "tutes/", "dist/", "user/"]
            ):
                continue
            if "orb.kv" in path:
                continue
            print(f"Loading: {path}")
            Builder.load_file(path)
        # if not is_dev:
        # Builder.load_file("kivy_garden/contextmenu/app_menu.kv")
        # Builder.load_file("kivy_garden/contextmenu/context_menu.kv")

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
        audio_manager.set_volume()
        self.apps = Apps()
        self.apps.load_from_disk()
        self.apps.load_all_apps()

    def override_stdout(self):
        """
        Override stdout, so the standard 'print' command goes
        to Orb's console.
        """
        # _write is the original stdout
        _write = sys.stdout.write

        def write(*args):
            """
            New 'write' command
            """
            # simply join the arguments passed in
            content = " ".join(args)
            # print them out the regular way
            _write(content)
            # print them out to Orb's console
            self.consumables.append(content)
            # console_output(content)

        # do the override
        sys.stdout.write = write

    def on_stop(self):
        """
        Perform required tasks before app exists.
        """
        thread_manager.thread_manager.stop_threads()

    def on_pause(self):
        """
        Perform required tasks before app goes on pause
        e.g saving to disk.
        """
        pass

    def on_resume(self):
        """
        Perform required tasks before app resumes
        e.g restoring data from disk.
        """
        pass

    def build(self):
        """
        Main build method for the app.
        """
        self.override_stdout()
        self.make_dirs()

        self.load_kvs()
        data_manager.data_man = data_manager.DataManager()
        window_sizes = Window.size

        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = self.config["display"]["primary_palette"]
        self.icon = "orb.png"
        self.main_layout = MainLayout()

        return self.main_layout

    def build_config(self, config):
        """
        Default config values.
        """
        set_conf_defaults(config)

    def build_settings(self, settings):
        """
        Configuration screen for the app.
        """
        settings.add_json_panel("Orb", self.config, filename="orb/misc/settings.json")

    def on_config_change(self, config, section, key, value):
        """
        What to do when a config value changes. TODO: needs fixing.
        Currently we'd end up with multiple LND instances for example?
        Simply not an option.
        """
        if f"{section}.{key}" == "audio.volume":
            audio_manager.set_volume()
        self.main_layout.do_layout()

    @guarded
    def run(self, *args):
        super(OrbApp, self).run(*args)
