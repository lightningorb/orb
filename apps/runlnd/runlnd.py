# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-01-06 17:51:07
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-01-21 11:11:02

from functools import lru_cache
import os
from pathlib import Path

from peewee import Model, SqliteDatabase, CharField, BooleanField

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty

from orb.misc.plugin import Plugin
from orb.store.db_meta import get_db
from fabric import Connection


class RunLndDialog(Popup):
    pass


class RunLndPlugin(Plugin):
    def main(self):
        kv_path = (Path(__file__).parent / "runlnd.kv").as_posix()
        Builder.unload_file(kv_path)
        Builder.load_file(kv_path)
        RunLndDialog().open()
