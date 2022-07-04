# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-01-26 18:25:08
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-07-01 17:25:40

from kivy.properties import StringProperty
from kivy.uix.textinput import TextInput

from orb.misc.utils import mobile
from orb.misc import data_manager


class ConsoleOutput(TextInput):
    output = StringProperty("", rebind=True)

    def on_touch_down(self, touch):

        if self.collide_point(*touch.pos):
            if mobile and not touch.is_mouse_scrolling:
                return False
            if data_manager.data_man and data_manager.data_man.menu_visible:
                return False
        return super(ConsoleOutput, self).on_touch_down(touch)
