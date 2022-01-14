# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-15 07:15:28
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-01-14 12:02:18

from io import StringIO
import sys

from kivy.clock import mainthread
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label


class StatusLine(BoxLayout):
    def __init__(self, *args, **kwargs):
        super(StatusLine, self).__init__(*args, **kwargs)


class StatusLineOutput(Label):
    output = StringProperty("")
