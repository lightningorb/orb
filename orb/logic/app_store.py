# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-01-18 09:39:01
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-08-06 10:43:40

import os
import sys
from traceback import print_exc
from pathlib import Path
from textwrap import dedent
import shutil

from kivy.properties import BooleanProperty
from kivy.event import EventDispatcher
from kivy.app import App as KivyApp
from orb.misc.utils import pref_path
from orb.misc.plugin import Plugin
from orb.logic.app_store_api import API
import orb
import uuid
import zipfile


from yaml import load

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


class Apps(EventDispatcher):
    def __init__(self):
        self.apps = {}

    def load_from_disk(self):
        user_apps_dir = pref_path("app")
        default_apps_dir = Path(orb.__file__).parent / "apps"
        for d in [user_apps_dir, default_apps_dir]:
            print(f"Searching: {str(d)}")
            for plugin_info_file in d.glob("*/appinfo.yaml"):
                print(f"Found: {str(plugin_info_file)}")
                app = LocalApp(plugin_info_file)
                print(f"Created local app: {app.uuid}")
                self.apps[app.uuid] = app

    def load_all_apps(self):
        for app in self.apps.values():
            app._import()
            app.load()
            app.debug()

    def get_remote_apps(self):
        print("Requesting available apps")
        remote_apps = []
        for app in API().list_apps().apps:
            installed_app = KivyApp.get_running_app().apps.apps.get(app.uuid)
            if installed_app:
                remote_apps.append(installed_app)
            else:
                remote_apps.append(RemoteApp(app))
        print("Got remote apps.")
        return remote_apps

    def uninstall(self, app):
        if app.uuid in self.apps:
            del self.apps[app.uuid]
        app.uninstall()
        print("Uninstalled.")
        return True

    def install(self, remote_app):
        archive_path = API().download(remote_app.uuid)
        dest_path = pref_path("app") / remote_app.uuid
        if dest_path.is_dir():
            print("destination path exists - aborting")
            return None
        if not archive_path.is_file():
            print("download archive missing - aborting")
            return None
        os.makedirs(dest_path.as_posix(), exist_ok=True)
        with zipfile.ZipFile(archive_path.as_posix()) as file:
            file.extractall(dest_path.as_posix())
        info_file = dest_path / "appinfo.yaml"
        if info_file.is_file():
            app = LocalApp(info_file)
            app._import()
            app.load()
            print(f"Installed.")
            self.apps[app.uuid] = app
            return app
        else:
            print("appinfo.yaml is missing - aborting")
            return None

    def delete_from_store(self, app):
        API().delete_from_store(app.uuid)


class RemoteApp(EventDispatcher):

    installed = BooleanProperty(False)

    def __init__(self, remote_app):
        self.name = remote_app.name
        self.description = remote_app.description
        self.uuid = remote_app.uuid
        self.is_remote = True
        self.icon = API().get_icon_path(self.uuid)


class LocalApp(EventDispatcher):

    installed = BooleanProperty(True)

    def __init__(self, info_file):
        plugin_info = load(info_file.open(), Loader=Loader)
        self.plugin_info = plugin_info
        self.info_file = info_file
        self.menu = plugin_info.get("menu", None)
        if self.menu:
            self.menu = ">".join(x.strip() for x in self.menu.split(">"))
        self.name = plugin_info.get("name", None)
        self.description = plugin_info.get("description", None)
        self.author = plugin_info.get("author", None)
        self.uuid = plugin_info.get("uuid", None)
        self.directory = self.info_file.parent
        self.py = self.plugin_info.get("main")
        if not self.py:
            for ft in ["*.py", "*.pyc"]:
                self.py = next(self.directory.glob(ft), None)
                if self.py:
                    break
        if self.plugin_info.get("icon"):
            self.icon = (self.directory / self.plugin_info.get("icon")).as_posix()

        self.module_name = (
            os.path.basename(os.path.splitext(self.py)[0]) if self.py else None
        )
        self.__import = None
        self.instance = None
        self.classname = None
        self.is_remote = False

    def debug(self):
        print(
            f"""Main Python file: {self.py}
            Directory: {self.directory}
            Module name: {self.module_name}
            Class Name: {self.classname}
            Is Remote: {self.is_remote}
            """
        )

    @property
    def menu_run_code(self):
        code = dedent(
            f"""
            import sys
            from kivy.app import App

            dm = App.get_running_app()
            if '{self.module_name}' in dm.plugin_registry:
                dm.plugin_registry['{self.module_name}'].cleanup()
                del dm.plugin_registry['{self.module_name}']
            import {self.module_name}
            from importlib import reload
            reload({self.module_name})
            plug = {self.module_name}.{self.classname}()
            dm.plugin_registry['{self.module_name}'] = plug
            plug.main()
            """
        )
        return code

    def _import(self):
        sys.path.append(self.directory.as_posix())
        try:
            self.__import = __import__(self.module_name)
        except:
            print_exc()
            print(f"Unable to load {self.module_name}")

    def load(self):
        cls = next(
            iter(
                [
                    c
                    for c in Plugin.__subclasses__()
                    if (c.__module__).split(".")[-1] == self.module_name
                    # hack: this means apps need unique module names; not good.
                ]
            ),
            None,
        )
        if not cls:
            print(f"class could not be determined for plugin {self.name}")
        else:
            inst = cls()
            self.classname = cls.__name__
            self.instance = inst
            self.instance.set_app(self)

    def uninstall(self):
        if self.module_name in sys.modules:
            del sys.modules[self.module_name]
        dest = pref_path("trash") / str(uuid.uuid4())
        shutil.move(self.directory, dest.as_posix())
