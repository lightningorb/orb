# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-01-15 13:22:44
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-01-17 03:07:45
# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-15 07:15:28
# @Last Modiconsumablesfied by:   lnorb.com
# @Last Modified time: 2022-01-15 13:07:26

from collections import deque

from kivy.app import App
from kivy.clock import (
    Clock,
    _default_time as time,
)  # ok, no better way to use the same clock as kivy, hmm
from kivy.clock import mainthread
from kivy.uix.screenmanager import Screen

from orb.misc import data_manager
from orb.screens.console.console_input import ConsoleInput
from orb.screens.console.console_output import ConsoleOutput

MAX_TIME = 1 / 5


class ConsoleScreen(Screen):

    lines = deque()
    player_showing = False
    show_player = False
    is_showing = False

    #: text to display in output when the user enters the output screen
    output_text = ""

    def __init__(self, *args, **kwargs):
        super(ConsoleScreen, self).__init__(*args, **kwargs)
        Clock.schedule_interval(self.consume, 0)

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
                "console_input", {}
            ).get("text", "")
            app = App.get_running_app()
            app.root.ids.app_menu.add_console_menu(cbs=self.ids.console_input)

        delayed()
        self.is_showing = True
        self.ids.console_output.output = self.output_text

    def on_pre_leave(self):
        self.is_showing = False

    def update_output(self, text, last_line):
        if text and text != "\n":
            if self.is_showing:
                self.ids.console_output.output = text
            else:
                self.output_text = text
        if last_line and last_line != "\n":
            app = App.get_running_app()
            app.root.ids.status_line.ids.line_output.output = last_line

    def consume(self, *args):
        """
        Print to the console's output section.
        Print the last line on the status line.
        """
        app = App.get_running_app()
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
                    last_line = text_lines[-1]
                self.update_output("\n".join(self.lines), last_line)
