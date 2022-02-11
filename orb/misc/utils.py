# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-27 04:05:23
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-02-11 11:26:56

from pathlib import Path

from kivy.app import App
from kivy.utils import platform

from orb.math.Vector import Vector


def prefs_col(name):
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
    app = App.get_running_app()
    if app:
        section, key = name.split(".")
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


mobile = platform in ("ios", "android")
desktop = platform not in ("ios", "android")
