# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-01-06 17:51:07
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-01-21 11:42:45

from abc import ABC, abstractmethod
from kivy.app import App


class Plugin(ABC):
    def __init__(self, *args, **kwargs):
        self._app = None

    def set_app(self, app):
        self._app = app

    @property
    def app(self):
        print(f"{__file__}.app() deprecation warning")
        assert False
        return App.get_running_app()

    def get_screen(self, name):
        return App.get_running_app().root.ids.sm.get_screen(name)
