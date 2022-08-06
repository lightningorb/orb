# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-01-26 18:25:08
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-08-06 10:21:09

from kivy.properties import StringProperty
from kivy.uix.textinput import TextInput
from kivy.app import App

from orb.misc.utils import mobile


class ConsoleOutput(TextInput):
    output = StringProperty("", rebind=True)

    def on_touch_down(self, touch):
        app = App.get_running_app()
        if self.collide_point(*touch.pos):
            if mobile and not touch.is_mouse_scrolling:
                return False
            if app and app.menu_visible:
                return False
        return super(ConsoleOutput, self).on_touch_down(touch)
