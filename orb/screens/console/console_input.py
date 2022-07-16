# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-01-17 03:11:15
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-07-13 15:05:23

import uuid
from traceback import format_exc

from pygments.lexers import CythonLexer

from kivy import platform
from kivy.app import App
from kivy.properties import StringProperty
from kivy.uix.button import Button
from kivy.uix.codeinput import CodeInput
from kivy.uix.popup import Popup

from orb.components.popup_drop_shadow import PopupDropShadow
from orb.misc import data_manager


class ConsoleFileChooser(PopupDropShadow):

    selected_path = StringProperty("")


class ConsoleInput(CodeInput):

    output = StringProperty("")

    def __init__(self, *args, **kwargs):
        super(ConsoleInput, self).__init__(
            style_name="monokai", lexer=CythonLexer(), *args, **kwargs
        )

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            if data_manager.data_man and data_manager.data_man.menu_visible:
                return False
        return super(ConsoleInput, self).on_touch_down(touch)

    def execute(self, text):
        try:
            exec(text)
        except:
            print(format_exc())

    def run(self, *_):
        self.execute(self.text)

    def open_file(self, *_):
        dialog = ConsoleFileChooser()
        dialog.open()

        def do_open(widget, path):
            print(f"opening {path}")
            self.text = open(path).read()

        dialog.bind(selected_path=do_open)

    def clear_input(self, *_):
        self.text = ""

    def clear_output(self, *_):
        self.output = ""

    def reset_split_size(self, *_):

        App.get_running_app().store.put(
            "console", input_height=None, output_height=None
        )

    def keyboard_on_key_up(self, window, keycode):
        App.get_running_app().store.put("console_input", text=self.text)
        if self.do_eval:
            self.execute(self.selection_text)
        super(ConsoleInput, self).keyboard_on_key_up(window, keycode)
        return True

    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        meta = "meta" in modifiers
        if meta and keycode[1] == "q":
            return False
        direction = (
            keycode[1]
            if keycode and keycode[1] in ("left", "right", "up", "down")
            else False
        )
        if meta and direction:
            if direction == "left":
                line = self.text.split("\n")[self.cursor_row]
                for i, c in enumerate(line, 1):
                    if c not in (" ", "\t"):
                        self._cursor = (i, self._cursor[1])
                        break
            elif direction == "right":
                line = self.text.split("\n")[self.cursor_row]
                self._cursor = (len(line) - 1, self._cursor[1])
        self.do_eval = keycode[1] == "enter" and self.selection_text
        if self.do_eval:
            return False
        return super(ConsoleInput, self).keyboard_on_key_down(
            window, keycode, text, modifiers
        )
