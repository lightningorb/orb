# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-15 07:15:28
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-01-04 05:59:56

import os
import sys
from traceback import format_exc
from io import StringIO
from collections import deque

from pygments.lexers import CythonLexer

from kivy.app import App
from kivy.clock import mainthread
from kivy.properties import StringProperty
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput
from kivy.uix.codeinput import CodeInput
from kivy.uix.videoplayer import VideoPlayer

from orb.screens.console.console_splitter import *

import data_manager

from kivy.utils import platform

ios = platform == "ios"


class ConsoleScreen(Screen):

    lines = deque()
    player_showing = False
    show_player = False

    def on_enter(self):
        """
        We have entered the console screen
        """

        @mainthread
        def delayed():
            # when 'output' changes on the console_input
            # then update 'output' on the console_output
            self.ids.console_input.bind(output=self.ids.console_output.setter("output"))
            # retrieve the code stored in the prefs, and set it
            # in the console input
            self.ids.console_input.text = data_manager.data_man.store.get(
                "console_input"
            ).get("text", "")
            app = App.get_running_app()
            app.root.ids.app_menu.add_console_menu(cbs=self.ids.console_input)
            if self.show_player and not self.player_showing:
                self.ids.vid_box.add_widget(
                    VideoPlayer(
                        source=os.path.expanduser(
                            "~/Movies/Monosnap/screencast 2021-12-29 17-28-56.mp4"
                        )
                    )
                )

        delayed()

    @mainthread
    def update_output(self, text, last_line):
        if not ios:
            self.ids.console_output.output = text
        if last_line:
            app = App.get_running_app()
            app.root.ids.status_line.ids.line_output.output = last_line
            app.root.ids.status_line.ids.line_output.cursor = (0, 0)

    def print(self, text):
        """
        Print to the console's output section.
        Print the last line on the status line.
        """
        # make sure we have something to print
        if text:
            # make sure it's a string
            text = str(text)
            # split up the output into lines
            text_lines = text.split("\n")
            if text_lines:
                for line in text_lines:
                    if line:
                        self.lines.append(line)
                for _ in range(max(0, len(self.lines) - 30)):
                    self.lines.popleft()
                last_line = text_lines[-1]
                self.update_output("\n".join(self.lines), last_line)


class InstallScript(Popup):
    pass


class DeleteScript(Popup):
    pass


class LoadScript(Popup):
    pass


class ConsoleInput(CodeInput):

    output = StringProperty("")

    def __init__(self, *args, **kwargs):
        super(ConsoleInput, self).__init__(
            style_name="monokai", lexer=CythonLexer(), *args, **kwargs
        )

    def on_touch_down(self, touch):
        import data_manager

        if self.collide_point(*touch.pos):
            if data_manager.menu_visible:
                return False
        return super(ConsoleInput, self).on_touch_down(touch)

    def exec(self, text):
        old_stdout = sys.stdout
        sys.stdout = mystdout = StringIO()
        try:
            exec(text)
            sys.stdout = old_stdout
            self.output += "\n" + mystdout.getvalue().strip() + "\n"
        except:
            exc = format_exc()
            if exc:
                self.output += exc

    def run(self, *_):
        self.exec(self.text)

    def load(self, *_):
        inst = LoadScript()

        def do_load(button, *_):
            sc = data_manager.data_man.store.get("scripts", {})
            self.text = sc.get(button.text, "")
            inst.dismiss()

        sc = data_manager.data_man.store.get("scripts", {})

        for name in sc:
            button = Button(text=name, size_hint=(None, None), size=(480, 40))
            button.bind(on_release=do_load)
            inst.ids.grid.add_widget(button)

        inst.open()
        app = App.get_running_app()
        app.root.ids.app_menu.close_all()

    def install(self, *_):
        inst = InstallScript()
        inst.open()

        def do_install(_, *__):
            sc = data_manager.data_man.store.get("scripts", {})
            script_name = ">".join(
                x.strip() for x in inst.ids.script_name.text.split(">")
            )
            sc[script_name] = self.text
            data_manager.data_man.store.put("scripts", **sc)
            app = App.get_running_app()
            app.root.ids.app_menu.populate_scripts()
            inst.dismiss()

        inst.ids.install.bind(on_release=do_install)
        app = App.get_running_app()
        app.root.ids.app_menu.close_all()

    def delete(self, *_):
        inst = LoadScript()
        try:
            sc = data_manager.data_man.store.get("scripts")
        except:
            pass

        def do_delete(button, *args):
            sc = data_manager.data_man.store.get("scripts", {})
            del sc[button.text]
            data_manager.data_man.store.put("scripts", **sc)
            app = App.get_running_app()
            app.root.ids.app_menu.populate_scripts()
            inst.dismiss()

        for name in sc:
            button = Button(text=name, size_hint=(None, None), size=(480, 40))
            button.bind(on_release=do_delete)
            inst.ids.grid.add_widget(button)

        inst.open()
        app = App.get_running_app()
        app.root.ids.app_menu.close_all()

    def clear_input(self, *args):
        self.text = ""

    def clear_output(self, *args):
        self.output = ""

    def reset_split_size(self, *args):
        import data_manager

        data_manager.data_man.store.put(
            "console", input_height=None, output_height=None
        )

    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        meta = "meta" in modifiers
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

        if text != "\u0135":
            to_save = self.text + (text or "")
            do_eval = keycode[1] == "enter" and self.selection_text
            data_manager.data_man.store.put("console_input", text=to_save)
            if do_eval:
                self.exec(self.selection_text)
                return True
        return super(ConsoleInput, self).keyboard_on_key_down(
            window, keycode, text, modifiers
        )


class ConsoleOutput(TextInput):
    output = StringProperty("")

    def on_touch_down(self, touch):
        import data_manager

        if self.collide_point(*touch.pos):
            if data_manager.menu_visible:
                return False
        return super(ConsoleOutput, self).on_touch_down(touch)
