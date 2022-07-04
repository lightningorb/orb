# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-27 04:05:23
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-07-01 16:08:17

import re
from pathlib import Path

from kivy.app import App
from kivy.utils import platform

from orb.math.Vector import Vector


mobile = platform in ("ios", "android")
ios = platform == "ios"
android = platform == "android"
desktop = platform not in ("ios", "android")


def prefs_col(name):
    """
    Get a preference value in the
    form section.key as an RGBA list.
    """
    app = App.get_running_app()
    section, key = name.split(".")
    col = app.config[section][key]
    if "#" in col:
        if len(col) == 7:
            col += "ff"
        r, g, b, a = list(int(col[i : i + 2], base=16) / 255 for i in range(1, 8, 2))
        return r, g, b, a
    return eval(col)


def pref(name):
    """
    Get a preference value in the
    form section.key.
    """
    app = App.get_running_app()
    if app:
        section, key = name.split(".")
        if section not in app.config:
            print(f"CONFIG SECTION NOT FOUND: {section}")
            return ""
        if app.config[section][key] == "False":
            return False
        if app.config[section][key] == "True":
            return True
        try:
            return float(app.config[section][key])
        except:
            return app.config[section][key]


def set_string_pref(name, val):
    app = App.get_running_app()
    if app:
        section, key = name.split(".")
    app.config[section][key] = val
    app.config.write()


def pref_path(name):
    app = App.get_running_app()
    return Path(app.user_data_dir) / pref(f"path.{name}")


class hashabledict(dict):
    def __hash__(self):
        return hash(tuple(sorted(self.items())))


def closest_point_on_line(p1, p2, p3):
    dx, dy = p2.x - p1.x, p2.y - p1.y
    det = dx * dx + dy * dy
    a = (dy * (p3.y - p1.y) + dx * (p3.x - p1.x)) / det
    return Vector(p1.x + a * dx, p1.y + a * dy)


def get_available_nodes():
    app = App.get_running_app()
    data_dir = Path(app._get_user_data_dir()).parent
    nodes = []
    for x in data_dir.glob("orb_*"):
        m = re.match(r"orb_([a-zA-Z0-9]{66})", x.name)
        if m and x.is_dir():
            nodes.append(m.group(1))
    return nodes
