import sys
import data_manager

from io import StringIO

from kivy.uix.actionbar import ContextualActionView
from kivy.uix.button import Button
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.clock import mainthread
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput
from kivy.app import App

import ui_actions
from traceback import format_exc


class Project(ContextualActionView):
    pass


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
            try:
                # retrieve the code stored in the prefs, and set it
                # in the console input
                code = data_manager.data_man.store.get("console_input").get("text", "")
                self.ids.console_input.text = code
            except:
                pass
            app = App.get_running_app()
            project = Project()
            # add the contextual menu for the console to the menu bar
            app.root.ids.ActionBar.add_widget(project)

            # bind run and install buttons
            project.ids.run.bind(on_release=self.ids.console_input.run)
            project.ids.load.bind(on_release=self.ids.console_input.load)
            project.ids.install.bind(on_release=self.ids.console_input.install)

        delayed()


class InstallScript(Popup):
    pass


class LoadScript(Popup):
    pass


class ConsoleInput(TextInput):

    output = StringProperty("")

    def exec(self, text):
        lnd = data_manager.data_man.lnd
        old_stdout = sys.stdout
        sys.stdout = mystdout = StringIO()
        try:
            exec(text)
            sys.stdout = old_stdout
            message = mystdout.getvalue()
            self.output += message.strip() + "\n"
        except:
            exc = format_exc()
            if exc:
                self.output += exc

    def run(self, *args):
        self.exec(self.text)

    def load(self, *args):
        inst = LoadScript()
        try:
            sc = data_manager.data_man.store.get("scripts")
        except:
            pass

        def do_load(button, *args):
            sc = {}
            try:
                sc = data_manager.data_man.store.get("scripts")
            except:
                pass
            script = sc.get(button.text, None)
            self.text = script
            inst.dismiss()

        for name in sc:
            button = Button(text=name, size_hint=(None, None), size=(480, 40))
            button.bind(on_release=do_load)
            inst.ids.grid.add_widget(button)

        inst.open()

    def install(self, *args):
        inst = InstallScript()
        inst.open()

        def do_install(_, *args):
            sc = {}
            try:
                sc = data_manager.data_man.store.get("scripts")
            except:
                pass
            sc[inst.ids.script_name.text] = self.text
            data_manager.data_man.store.put("scripts", **sc)
            ui_actions.populate_scripts()
            inst.dismiss()

        inst.ids.install.bind(on_release=do_install)

    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        do_eval = keycode[1] == "enter" and self.selection_text
        data_manager.data_man.store.put("console_input", text=self.text)
        if do_eval:
            self.output += str(self.selection_text)
            self.exec(self.selection_text)
        else:
            super(ConsoleInput, self).keyboard_on_key_down(
                window, keycode, text, modifiers
            )


class ConsoleOutput(TextInput):
    output = StringProperty("")
