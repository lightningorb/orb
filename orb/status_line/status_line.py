# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-15 07:15:28
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-07-01 11:45:55

import sys
from io import StringIO

from kivy.app import App
from kivy.uix.label import Label
from kivy.clock import mainthread
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.properties import StringProperty


class StatusLine(BoxLayout):
    def __init__(self, *args, **kwargs):
        super(StatusLine, self).__init__(*args, **kwargs)

    def se_release(self):
        app = App.get_running_app()
        if app.root.ids.sm.current != "console":
            self.prev = app.root.ids.sm.current
            app.root.ids.sm.current = "console"
            app.root.ids.sm.transition.direction = "left"
        else:
            app.root.ids.sm.current = self.prev
            app.root.ids.sm.transition.direction = "right"


class StatusLineOutput(Label):
    output = StringProperty("")
