# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-01-17 03:11:15
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-08-19 05:13:50

from traceback import format_exc
from string import *
from pygments.lexers import CythonLexer
import bisect

from kivy.app import App
from kivy.properties import StringProperty
from kivy.uix.codeinput import CodeInput

from orb.components.popup_drop_shadow import PopupDropShadow

ascii_dev_letters = ascii_letters + "_" + digits


class ConsoleFileChooser(PopupDropShadow):

    selected_path = StringProperty("")


class ConsoleInput(CodeInput):

    output = StringProperty("")

    def __init__(self, *args, **kwargs):
        super(ConsoleInput, self).__init__(
            style_name="monokai", lexer=CythonLexer(), *args, **kwargs
        )

    def on_touch_down(self, touch):
        app = App.get_running_app()
        if self.collide_point(*touch.pos):
            if app.menu_visible:
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
        alt = "alt" in modifiers
        if meta and keycode[1] == "q":
            return False
        direction = (
            keycode[1]
            if keycode and keycode[1] in ("left", "right", "up", "down")
            else False
        )
        if keycode[1] == "x" and meta:
            lines = self.text.split("\n")
            lines = lines[: self.cursor_row] + lines[self.cursor_row + 1 :]
            cursor = self.cursor[:]
            self._set_text("\n".join(lines))
            self.cursor = cursor[:]
        if direction in ("left", "right"):
            get_line = lambda n: self.text.split("\n")[n]
            line = get_line(self.cursor_row)
            if alt:
                if line:
                    label = lambda x: next(
                        iter(
                            i
                            for i, c in enumerate(
                                [ascii_dev_letters, whitespace, punctuation], 1
                            )
                            if x in c
                        ),
                        0,
                    )
                    labels = [(i, label(x)) for i, x in enumerate(line)]
                    ret = [
                        v[0]
                        for i, v in enumerate(labels, 1)
                        if v[1] != labels[i - 2][1]
                    ]
                    if direction == "left":
                        pos = ret[bisect.bisect_right(ret, self.cursor_col - 1) - 1]
                    else:
                        pos = ret[
                            min(
                                bisect.bisect_left(ret, self.cursor_col + 1) + 1,
                                len(ret) - 1,
                            )
                        ]
                    self.cursor = (pos + int(direction == "left"), self._cursor[1])
            if meta:
                if direction == "left":
                    first_non_space_like = next(
                        iter(i for i, c in enumerate(line) if c not in " \t"), 0
                    )
                    row = first_non_space_like * (
                        first_non_space_like != self._cursor[0]
                    )
                    self._cursor = (row + 1, self._cursor[1])
                elif direction == "right":
                    self._cursor = (len(line) + 1, self._cursor[1])
        self.do_eval = keycode[1] == "enter" and self.selection_text
        if self.do_eval:
            return False
        return super(ConsoleInput, self).keyboard_on_key_down(
            window, keycode, text, modifiers
        )
