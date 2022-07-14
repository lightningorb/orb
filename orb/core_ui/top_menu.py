# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-15 07:15:28
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-07-13 15:04:56

from traceback import format_exc

from kivy.app import App as KivyApp
from kivy_garden.contextmenu import AppMenu
from kivy_garden.contextmenu import ContextMenuTextItem
from kivy_garden.contextmenu import ContextMenuDivider
from kivy_garden.contextmenu import ContextMenu
from kivy.properties import ObjectProperty

from orb.misc import data_manager
from orb.misc.plugin import Plugin


class TopMenu(AppMenu):

    hovered_menu_item = ObjectProperty()

    script_widgets = []
    view_widgets = []

    def __init__(self, *args, **kwargs):
        super(TopMenu, self).__init__(*args, **kwargs)

    def populate_scripts(self):
        apps = KivyApp.get_running_app().apps.apps.values()
        menu = [x for x in self.children if x.text.lower() == "apps"][0]

        for widget in self.script_widgets:
            menu.submenu.remove_widget(widget)

        def add_to_tree(d, c, t, p, app):
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
                add_to_tree(d + 1, c, t[c[d]], widget.submenu, app=app)
            else:

                def run(widget):
                    kivyApp = KivyApp.get_running_app()
                    kivyApp.root.ids.app_menu.close_all()
                    self.execute(widget.app.menu_run_code)
                    return True

                widget = ContextMenuTextItem(text=c[d], on_release=run)
                widget.app = app
                p.add_widget(widget)
                self.script_widgets.append(widget)

        tree = {}
        for app in apps:
            components = [x.strip() for x in app.menu.split(">")]
            add_to_tree(d=0, c=components, t=tree, p=menu.submenu, app=app)
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

    def execute(self, text):
        try:
            exec(text)
        except:
            exc = format_exc()
            if exc:
                print(exc)

    def add_channels_menu(self):
        app = KivyApp.get_running_app()
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
