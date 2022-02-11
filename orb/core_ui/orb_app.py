# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-15 07:15:28
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-02-11 11:37:26

import os
import sys
import json
from pathlib import Path
from textwrap import dedent
from traceback import print_exc
from importlib import __import__
from threading import Thread
import shutil
from collections import deque

from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.utils import platform
from kivy.config import Config
from kivy.properties import ObjectProperty
from kivy.properties import NumericProperty
from kivy.properties import ListProperty
from kivy.uix.button import Button

from orb.misc.utils import pref
from orb.logic.app_store import Apps
from orb.misc.monkey_patch import do_monkey_patching
from orb.misc.conf_defaults import set_conf_defaults
from orb.audio.audio_manager import audio_manager
from orb.misc.decorators import guarded
from orb.core_ui.main_layout import MainLayout
from orb.logic import thread_manager
from orb.misc.utils import pref_path, desktop
from orb.misc.prefs import cert_path

from orb.misc import data_manager

ios = platform == "ios"

print(platform)

if platform == "windows":
    Config.set("graphics", "multisamples", "0")

sys.path.append("orb/lnd/grpc_generate")
sys.path.append("orb/lnd")

do_monkey_patching()
is_dev = "main.py" in sys.argv[0]

print(f"sys.argv[0] is {sys.argv[0]}")


class OrbApp(MDApp):
    title = "Orb"
    consumables = deque()
    selection = ObjectProperty(allownone=True)
    update_channels_widget = NumericProperty()
    apps = None

    def get_application_config(self, defaultpath=f"~/orb.ini"):
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
        elif platform == "macosx":
            defaultpath = f"{self._get_user_data_dir()}/%(appname)s.ini"
        path = os.path.expanduser(defaultpath) % {
            "appname": self.name,
            "appdir": self.directory,
        }
        print(f"Application config: {path}")
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
        """
        Compile all the kvs into an orb/kvs.py file.
        This greatly simplifies deployment.
        """
        if is_dev:
            kvs = ["from kivy.lang import Builder"]
            kvs_found = False
            main_dir = Path(sys.argv[0]).parent
            print(f"main_dir: {main_dir}")

            def load_kvs_from(d):
                kvs_found = False
                for path in d.rglob("*.kv"):
                    kvs_found = True
                    if apps_path.as_posix() in path.as_posix():
                        # apps handle their kvs themselves
                        continue
                    print(f"compiling: {path}")
                    kv = path.open().read().replace("\\n", "\\\n")
                    kvs.append(f"Builder.load_string('''\n{kv}\n''')")
                return kvs_found

            apps_path = main_dir / "orb/apps"
            kvs_found = load_kvs_from(main_dir / "orb")
            kvs_found |= load_kvs_from(main_dir / "third_party")
            if kvs_found:
                path = main_dir / "orb/kvs.py"
                print(f"Saving to: {path}")
                open(path, "w").write("\n".join(kvs))

        import orb.kvs

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
            data_manager.data_man.channels.get()
            print("channels updated")

        Thread(target=update_chans).start()
        return True

    def check_cert_and_mac(self):
        from orb.misc.certificate import Certificate
        from orb.misc.certificate_secure import CertificateSecure

        from orb.misc.macaroon import Macaroon
        from orb.misc.macaroon_secure import MacaroonSecure

        cert = Certificate.init_from_str(pref("lnd.tls_certificate"))
        if cert.is_well_formed():
            cert_secure = CertificateSecure.init_from_plain(cert.cert)
            self.config["lnd"]["tls_certificate"] = cert_secure.cert_secure.decode()
            self.config.write()

        mac = Macaroon.init_from_str(pref("lnd.macaroon_admin"))
        if mac.is_well_formed():
            mac_secure = MacaroonSecure.init_from_plain(mac.macaroon.encode())
            self.config["lnd"]["macaroon_admin"] = mac_secure.macaroon_secure.decode()
            self.config.write()

    def build(self):
        """
        Main build method for the app.
        """
        Config.set("graphics", "window_state", "maximized")
        Config.set("graphics", "fullscreen", "auto")
        if Window:
            Window.maximize()
        self.override_stdout()
        self.make_dirs()
        self.check_cert_and_mac()
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
        path = Path(__file__).parent.parent.parent / "orb/misc/settings.json"
        print(f"Settings file: {path.as_posix()}")
        settings.add_json_panel("Orb", self.config, filename=path.as_posix())

    def on_config_change(self, config, section, key, value):
        if [section, key] == ["debug", "htlcs"]:
            self.update_channels_widget += 1

        self.main_layout.do_layout()

    @guarded
    def run(self, *args):
        super(OrbApp, self).run(*args)
