# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-06-28 14:50:53
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-07-02 06:27:10

import os
import sys
from collections import deque
from pathlib import Path

from kivymd.app import MDApp
from kivy.utils import platform

is_dev = "main.py" in sys.argv[0]


class AppCommon(MDApp):
    consumables = deque()

    def get_application_config(self, defaultpath=f"~/orb.ini"):
        """
        Get location of the orb.ini file. This may differ from
        one OS to the next.
        """
        print(f"APP NAME: {self.name}")
        if platform == "android":
            defaultpath = f"{self._get_user_data_dir()}/%(appname)s.ini"
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
        if platform == "ios":
            data_dir = os.path.expanduser("~/Documents")
        elif platform == "android":
            from jnius import autoclass, cast

            PythonActivity = autoclass("org.kivy.android.PythonActivity")
            context = cast("android.content.Context", PythonActivity.mActivity)
            file_p = cast("java.io.File", context.getFilesDir())
            data_dir = (Path(file_p.getAbsolutePath()) / self.name).as_posix()
            print(f"DATA DIR: {data_dir}")
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
