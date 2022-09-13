# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-08-08 14:32:04
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-09-13 14:55:08

import os
from pathlib import Path
import tempfile

from sys import platform as _sys_platform


def _get_platform():
    if _sys_platform in ("win32", "cygwin"):
        return "win"
    elif _sys_platform == "darwin":
        return "macosx"
    elif _sys_platform.startswith("linux"):
        return "linux"
    elif _sys_platform.startswith("freebsd"):
        return "linux"
    return "unknown"


platform = _get_platform()


def get_user_data_dir_static():
    if platform == "ios":
        data_dir = os.path.expanduser("~/Documents")
    elif platform == "android":
        from jnius import autoclass, cast

        PythonActivity = autoclass("org.kivy.android.PythonActivity")
        context = cast("android.content.Context", PythonActivity.mActivity)
        file_p = cast("java.io.File", context.getFilesDir())
        data_dir = (Path(file_p.getAbsolutePath())).as_posix()
    elif platform == "win":
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


def cert_path(caller_id):
    return Path(tempfile.gettempdir()) / f"{caller_id}_f66d6b24ccfb"


def pref(name):
    """
    Get a preference value in the
    form section.key.
    """
    from orb.app import App

    app = App.get_running_app()
    if app:
        section, key = name.split(".")
        if app.config.get(section, key) == "False":
            return False
        if app.config.get(section, key) == "True":
            return True
        try:
            return float(app.config.get(section, key))
        except:
            return app.config.get(section, key)


def pref_path(name):
    from orb.app import App

    app = App.get_running_app()
    return Path(app.user_data_dir) / pref(f"path.{name}")
