# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-15 07:15:28
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-01-15 04:48:13

import os
import sys
import json
from pathlib import Path
from traceback import print_exc
from importlib import __import__
from glob import glob
import shutil

from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.utils import platform

from orb.misc.monkey_patch import do_monkey_patching
from orb.misc.conf_defaults import set_conf_defaults
from orb.audio.audio_manager import audio_manager
from orb.misc.decorators import guarded
from orb.core_ui.main_layout import MainLayout
from orb.misc.ui_actions import console_output
from orb.misc.plugin import Plugin
from orb.logic import thread_manager
from orb.misc.utils import pref, pref_path

from orb.misc import data_manager

ios = platform == "ios"

sys.path.append("orb/lnd/grpc_generate")
sys.path.append("orb/lnd")

do_monkey_patching()
is_dev = "main.py" in sys.argv[0]


class OrbApp(MDApp):
    title = "Orb"

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
                join(os.environ.get("XDG_CONFIG_HOME", "~/.config"), self.name)
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

    def save_user_scripts(self):
        """
        Load the scripts from 'user_scripts.json' and save the
        scripts in the users's user_data_dir.
        """

        if os.path.exists("user_scripts.json"):
            with open("user_scripts.json") as f:
                user_scripts = json.loads(f.read())
                scripts_dir = pref_path("script")
                for path in user_scripts:
                    with open(scripts_dir / os.path.basename(path), "w") as f:
                        f.write(user_scripts[path])

    def load_user_scripts(self):
        if ios:
            scripts_dir = pref_path("script")
        else:
            scripts_dir = Path("user/scripts")
        plugins = {}
        for plugin_file_path in scripts_dir.glob("*.py"):
            plugin_module_name = os.path.basename(os.path.splitext(plugin_file_path)[0])
            try:
                plugins[plugin_module_name] = __import__(plugin_module_name)
            except:
                print_exc()
                print(f"Unable to load {plugin_module_name}")

        for cls in Plugin.__subclasses__():
            print(f"Loading plugin: {cls.__name__} (from {cls.__module__})")
            plugin_instance = cls()
            plugin_instance.install(
                script_name=f"{cls.__module__}.py", class_name=cls.__name__
            )
            if plugin_instance.autorun:
                plugin_instance.main()

    def make_dirs(self):
        """
        Create data directories if required
        """
        for key in ["video", "yaml", "json", "db", "cert", "script"]:
            path = pref_path(key)
            if not path.is_dir():
                os.makedirs(path)

    def upgrade_tasks(self):
        """
        Perform tasks that need to be run from one version to another.
        Avoid doing this as it most likely leads to breaking backward
        compatability.
        """

        data_dir = Path(self.user_data_dir)

        if ios:
            old_data_dir = Path(self.user_data_dir) / "orb"
            if old_data_dir.is_dir():
                data_dir = old_data_dir

        # move db files into a dbs directory
        def do_move(pattern, key):
            for f in data_dir.glob(pattern):
                shutil.move(f, pref_path(key) / f.parts[-1])

        for pattern, key in [
            ["*.db", "db"],
            ["*.mp4", "video"],
            ["*.yaml", "yaml"],
            ["*.json", "json"],
            ["*.cert", "cert"],
        ]:
            do_move(pattern, key)

    def on_start(self):
        """
        Perform required tasks before app exists.
        """
        if ios:
            sys.path.append(pref_path("script").as_posix())
        else:
            sys.path.append(Path("user/scripts").as_posix())
        audio_manager.set_volume()
        self.load_user_scripts()

        _write = sys.stdout.write

        def write(*args):
            content = " ".join(args)
            _write(content)
            console_output(content)

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
        self.make_dirs()
        self.upgrade_tasks()
        self.save_user_scripts()

        data_manager.DataManager.ensure_cert()
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
        elif key == "tls_certificate":
            data_manager.DataManager.save_cert(value)
        self.main_layout.do_layout()

    @guarded
    def run(self, *args):
        super(OrbApp, self).run(*args)
