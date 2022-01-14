# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-15 07:15:28
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-01-14 09:26:57

from traceback import format_exc

from kivy.app import App
from kivy_garden.contextmenu import AppMenu
from kivy_garden.contextmenu import ContextMenuTextItem
from kivy_garden.contextmenu import ContextMenuDivider
from kivy_garden.contextmenu import ContextMenu
from kivy.properties import ObjectProperty

from orb.store.scripts import load_scripts
from orb.misc import data_manager


class TopMenu(AppMenu):

    hovered_menu_item = ObjectProperty()

    script_widgets = []
    view_widgets = []

    def __init__(self, *args, **kwargs):
        super(TopMenu, self).__init__(*args, **kwargs)

    def populate_scripts(self):
        scripts = load_scripts()
        scripts = {
            ">".join([x.strip() for x in v.menu.split(">")]): v
            for v in scripts.values()
            if v.menu
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

                def run(self, *_):
                    app = App.get_running_app()
                    app.root.ids.app_menu.close_all()
                    tm.exec(scripts[self.full_name].code)
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

    def on_hovered_menu_item(self, *_, **__):
        """
        When the menu is hovered, tell data_manager.
        Sadly this doesn't seem to work as expected.
        :param _: args
        :param __: kwargs
        :return: None
        """
        data_manager.data_man.menu_visible = True

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
            ContextMenuTextItem(text="Run", on_release=cbs.run),
            ContextMenuTextItem(text="Install", on_release=cbs.install),
            ContextMenuTextItem(text="Delete", on_release=cbs.delete),
            ContextMenuDivider(),
            ContextMenuTextItem(text="Load", on_release=cbs.open_file),
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
