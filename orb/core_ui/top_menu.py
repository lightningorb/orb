# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-15 07:15:28
# @Last Modified by:   lnorb.com
# @Last Modified time: 2021-12-31 05:34:24
import sys
from traceback import format_exc
from io import StringIO

from kivy_garden.contextmenu import AppMenu
from kivy.app import App
from kivy_garden.contextmenu import ContextMenuTextItem
from kivy_garden.contextmenu import ContextMenuDivider
from kivy_garden.contextmenu import ContextMenu


import data_manager


class TopMenu(AppMenu):

    script_widgets = []
    view_widgets = []

    def populate_scripts(self):
        scripts = data_manager.data_man.store.get("scripts", {})
        scripts = {
            ">".join([x.strip() for x in k.split(">")]): v for k, v in scripts.items()
        }
        menu = [x for x in self.children if x.text.lower() == "scripts"][0]

        for widget in self.script_widgets:
            menu.submenu.remove_widget(widget)

        def add_to_tree(d, c, t, p):
            if len(c[d:]) > 1:
                if not t.get(c[d]):
                    widget = ContextMenuTextItem(text=c[d])
                    t[c[d]] = widget
                    widget.add_widget(ContextMenu())
                    p.add_widget(widget)
                    widget.submenu._on_visible(False)
                    if d == 0:
                        self.script_widgets.append(widget)
                else:
                    widget = t[c[d]]
                add_to_tree(d + 1, c, t[c[d]], widget.submenu)
            else:
                tm = self

                def run(self, *args):
                    app = App.get_running_app()
                    app.root.ids.app_menu.close_all()
                    tm.exec(scripts[self.full_name])
                    return True

                widget = ContextMenuTextItem(text=c[d], on_release=run)
                widget.full_name = ">".join(c)
                p.add_widget(widget)
                self.script_widgets.append(widget)

        tree = {}
        for script in scripts:
            components = [x.strip() for x in script.split(">")]
            add_to_tree(d=0, c=components, t=tree, p=menu.submenu)
        menu.submenu._on_visible(False)

    def exec(self, text):
        try:
            exec(text)
        except:
            exc = format_exc()
            if exc:
                print(exc)

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
            ContextMenuDivider(),
            ContextMenuTextItem(
                text="Reset Split Size", on_release=cbs.reset_split_size
            ),
        ]
        for w in self.view_widgets:
            menu.submenu.add_widget(w)
        menu.submenu._on_visible(False)
