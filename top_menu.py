from traceback import format_exc
import sys
from io import StringIO
from ui_actions import console_output
from kivy_garden.contextmenu import AppMenu
from kivy.clock import mainthread
from kivy.uix.actionbar import ActionButton
from kivy.uix.actionbar import ActionGroup
from kivy.app import App
from kivy_garden.contextmenu import ContextMenuTextItem
from kivy_garden.contextmenu import ContextMenu
from kivy_garden.contextmenu import AppMenuTextItem
from decorators import guarded
import data_manager


class TopMenu(AppMenu):
    def populate_scripts(self):
        @mainthread
        def delayed():
            print(self.ids)

        delayed()

        scripts = data_manager.data_man.store.get("scripts", [])
        menu = [x for x in self.children if x.text.lower() == "scripts"][0]
        menu.clear_widgets()
        cm = ContextMenu()
        for script in scripts:
            tm = self
            def run(self, *args):
                tm.exec(scripts[self.text])
            cm.add_widget(ContextMenuTextItem(text=script, on_release=run))
        menu.add_widget(cm)
        cm._on_visible(False)

    def exec(self, text):
        lnd = data_manager.data_man.lnd
        old_stdout = sys.stdout
        sys.stdout = mystdout = StringIO()
        try:
            exec(text)
            sys.stdout = old_stdout
            message = mystdout.getvalue()
            console_output(message.strip() + "\n")
        except:
            exc = format_exc()
            if exc:
                console_output(exc)

    def add_channels_menu(self):
        app = App.get_running_app()
        menu = [x for x in self.children if x.text.lower() == "view"][0]
        menu.clear_widgets()
        cm = ContextMenu()
        cm.add_widget(ContextMenuTextItem(text="Refresh", on_release=app.root.ids.sm.get_screen("channels").refresh))
        menu.add_widget(cm)
        cm._on_visible(False)

    def add_console_menu(self, cbs):
        menu = [x for x in self.children if x.text.lower() == "view"][0]
        menu.clear_widgets()
        cm = ContextMenu()
        cm.add_widget(ContextMenuTextItem(text="Load", on_release=cbs.load))
        cm.add_widget(ContextMenuTextItem(text="Run", on_release=cbs.run))
        cm.add_widget(ContextMenuTextItem(text="Install", on_release=cbs.install))
        cm.add_widget(ContextMenuTextItem(text="Delete", on_release=cbs.delete))
        menu.add_widget(cm)
        cm._on_visible(False)
