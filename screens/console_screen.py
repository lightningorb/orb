import sys
import data_manager

from io import StringIO

from kivy.uix.actionbar import ContextualActionView
from kivy.uix.button import Button
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
from kivy.properties import BooleanProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.clock import mainthread
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput
from kivy.app import App
from time import time
from kivy.uix.codeinput import CodeInput
from pygments.lexers import CythonLexer
from kivy.uix.splitter import Splitter
from kivy.properties import ObjectProperty

import ui_actions
from traceback import format_exc


class ConsoleSplitter(Splitter):

    input = ObjectProperty(None)
    output = ObjectProperty(None)

    def __init__(self, *args, **kwargs):
        super(ConsoleSplitter, self).__init__(*args, **kwargs)
        self.pressed = False
        self.pressed_pos = (0, 0)
        self.input_pressed_height = 0
        self.output_pressed_height = 0

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.pressed = True
            self.pressed_pos = touch.pos
            self.input_pressed_height = self.input.height
            self.output_pressed_height = self.output.height
        return super(ConsoleSplitter, self).on_touch_down(touch)

    def on_touch_up(self, touch):
        if self.collide_point(*touch.pos):
            self.pressed = False
        return super(ConsoleSplitter, self).on_touch_down(touch)

    def on_touch_move(self, touch):
        if self.pressed:
            self.input.height = self.input_pressed_height + (
                self.pressed_pos[1] - touch.pos[1]
            )
            self.output.height = self.output_pressed_height - (
                self.pressed_pos[1] - touch.pos[1]
            )
            self.input.size_hint = (None, None)
            self.output.size_hint = (None, None)
            return True
        return super(ConsoleSplitter, self).on_touch_move(touch)


class ConsoleScreen(Screen):
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

        delayed()

    @mainthread
    def print(self, text):
        if text:
            text = str(text)
            app = App.get_running_app()
            console = app.root.ids.sm.get_screen("console")
            lines = console.ids.console_output.output.split("\n")
            if len(lines) > 100:
                lines = lines[1:]
            out = "\n".join(lines)
            console.ids.console_output.output = out + "\n" + str(text)
            last_line = next(iter([x for x in text.split("\n") if x][::-1]), None)
            if last_line:
                app.root.ids.status_line.ids.line_output.output = last_line


class InstallScript(Popup):
    pass


class DeleteScript(Popup):
    pass


class LoadScript(Popup):
    pass


class ConsoleInput(CodeInput):

    output = StringProperty("")

    def __init__(self, *args, **kwargs):
        super(ConsoleInput, self).__init__(lexer=CythonLexer(), *args, **kwargs)
        self.tapped = 0
        self.double_tapped = False

    def on_touch_down(self, touch):
        """
        Sadly, the context menu has focus issues with a TextInput underneath it,
        so to fix this issue, the console's TextInput needs to be enabled by
        double-tapping it.
        """
        if self.collide_point(*touch.pos):
            if time() - self.tapped < 0.3:
                self.double_tapped = True
            self.tapped = time()
            if self.double_tapped:
                return super(ConsoleInput, self).on_touch_down(touch)
            return False
        self.double_tapped = False
        return super(ConsoleInput, self).on_touch_down(touch)

    def exec(self, text):
        lnd = data_manager.data_man.lnd
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

    def run(self, *args):
        self.exec(self.text)

    def load(self, *args):
        inst = LoadScript()

        def do_load(button, *args):
            sc = data_manager.data_man.store.get("scripts", {})
            self.text = sc.get(button.text, '')
            inst.dismiss()

        sc = data_manager.data_man.store.get("scripts", {})

        for name in sc:
            button = Button(text=name, size_hint=(None, None), size=(480, 40))
            button.bind(on_release=do_load)
            inst.ids.grid.add_widget(button)

        inst.open()
        app = App.get_running_app()
        app.root.ids.app_menu.close_all()

    def install(self, *args):
        inst = InstallScript()
        inst.open()

        def do_install(_, *args):
            sc = data_manager.data_man.store.get("scripts", {})
            sc[inst.ids.script_name.text] = self.text
            data_manager.data_man.store.put("scripts", **sc)
            app = App.get_running_app()
            app.root.ids.app_menu.populate_scripts()
            inst.dismiss()

        inst.ids.install.bind(on_release=do_install)
        app = App.get_running_app()
        app.root.ids.app_menu.close_all()

    def delete(self, *args):
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
        self.text = ''

    def clear_output(self, *args):
        self.output = ''

    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        if text != '\u0135':
            print('self.text', self.text)
            print('text', text)
            to_save = self.text + (text or '')
            print('to_save', to_save)
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
