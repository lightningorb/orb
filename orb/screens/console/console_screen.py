# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-01-15 13:22:44
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-08-08 09:47:45

from collections import deque
import sys
from kivy.app import App
from kivy.clock import (
    Clock,
    _default_time as time,
)  # ok, no better way to use the same clock as kivy, hmm
from kivy.clock import mainthread
from kivy.uix.screenmanager import Screen

from orb.screens.console.console_input import ConsoleInput
from orb.screens.console.console_output import ConsoleOutput

keep = lambda _: _
keep(ConsoleInput)
keep(ConsoleOutput)

MAX_TIME = 1 / 5.0


class ConsoleScreen(Screen):
    def __init__(self, *args, **kwargs):
        super(ConsoleScreen, self).__init__(*args, **kwargs)

        self.lines = deque()
        self.is_showing = False

        #: text to display in output when the user enters the output screen
        self.output_text = ""

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

            self.ids.console_input.text = (
                App.get_running_app().store.get("console_input", {}).get("text", "")
            )
            app = App.get_running_app()
            if app.root.ids.get("app_menu"):
                app.root.ids.app_menu.add_console_menu(cbs=self.ids.console_input)

        delayed()
        self.is_showing = True
        self.ids.console_output.output = self.output_text

    def on_pre_leave(self):
        self.ids.console_input.unbind(output=self.ids.console_output.setter("output"))
        self.is_showing = False

    def update_output(self, text, last_line):
        if text and text != "\n":
            self.output_text = text
            if self.is_showing:
                self.ids.console_output.output = text
        if last_line and last_line != "\n":
            app = App.get_running_app()
            if app.root and "status_line" in app.root.ids:
                app.root.ids.status_line.ids.line_output.output = last_line

    def consume(self, *args):
        """
        Print to the console's output section.
        Print the last line on the status line.
        """
        _print = lambda x: (sys.stdout.orig_write(str(x) + "\n"), sys.stdout.flush())
        app = App.get_running_app()
        if hasattr(app, "consumables"):
            while app.consumables and time() < (Clock.get_time() + MAX_TIME):
                text = app.consumables.popleft()
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
                        for _ in range(max(0, len(self.lines) - 500)):
                            self.lines.popleft()
                        last_line = next(
                            (x for x in reversed(text_lines) if x != ""), ""
                        )
                    self.update_output("\n".join(self.lines), last_line)
