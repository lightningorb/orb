from traceback import format_exc
import sys
from io import StringIO
from ui_actions import console_output
from kivy_garden.contextmenu import AppMenu
from kivy.clock import mainthread
from kivy.app import App
from kivy_garden.contextmenu import ContextMenuTextItem
from kivy_garden.contextmenu import ContextMenuDivider
from kivy_garden.contextmenu import ContextMenu
import data_manager


class TopMenu(AppMenu):

    script_widgets = []
    view_widgets = []

    def populate_scripts(self):
        scripts = data_manager.data_man.store.get("scripts", [])
        menu = [x for x in self.children if x.text.lower() == "scripts"][0]

        for widget in self.script_widgets:
            menu.submenu.remove_widget(widget)

        for script in scripts:
            tm = self

            def run(self, *args):
                app = App.get_running_app()
                app.root.ids.app_menu.close_all()
                tm.exec(scripts[self.text])
                return True

            widget = ContextMenuTextItem(text=script, on_release=run)
            self.script_widgets.append(widget)
            menu.submenu.add_widget(widget)
        menu.submenu._on_visible(False)

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

        for widget in self.view_widgets:
            menu.submenu.remove_widget(widget)

        widget = ContextMenuTextItem(
            text="Refresh", on_release=app.root.ids.sm.get_screen("channels").refresh
        )
        menu.submenu.add_widget(widget)
        self.view_widgets.append(widget)
        menu.submenu._on_visible(False)

    def add_console_menu(self, cbs):
        menu = [x for x in self.children if x.text.lower() == "view"][0]

        for widget in self.view_widgets:
            menu.submenu.remove_widget(widget)

        self.view_widgets = [
            ContextMenuTextItem(text="Load", on_release=cbs.load),
            ContextMenuTextItem(text="Run", on_release=cbs.run),
            ContextMenuTextItem(text="Install", on_release=cbs.install),
            ContextMenuTextItem(text="Delete", on_release=cbs.delete),
            ContextMenuDivider(),
            ContextMenuTextItem(text="Clear Input", on_release=cbs.clear_input),
            ContextMenuTextItem(text="Clear Output", on_release=cbs.clear_output),
        ]
        for w in self.view_widgets:
            menu.submenu.add_widget(w)
        menu.submenu._on_visible(False)
