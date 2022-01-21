# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-15 07:15:28
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-01-21 06:55:10

from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.floatlayout import MDFloatLayout
from kivy.properties import ObjectProperty
from kivy.properties import NumericProperty
from kivy.event import EventDispatcher
from kivy.app import App as KivyApp

from orb.components.popup_drop_shadow import PopupDropShadow
from orb.misc.decorators import guarded
from orb.logic.app_store_authenticate import authenticate


class AppSummary(BoxLayout):
    """
    The AppSummary is the card that shows in both the installed
    and available apps.
    """

    app = ObjectProperty()
    selected = NumericProperty(0)

    def __init__(self, app, *args, **kwargs):
        self.app = app
        super(AppSummary, self).__init__(*args, **kwargs)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.selected += 1
        return super(AppSummary, self).on_touch_down(touch)


class AppDetails(BoxLayout):
    """
    The AppDetails contain further information on the app
    such as ratings, and provides the ability to install or
    uninstall the app.
    """

    app = ObjectProperty(rebind=True)

    def __init__(self, app, *args, **kwargs):
        self.app = app
        super(AppDetails, self).__init__(*args, **kwargs)

    def install_uninstall(self):
        kivy_app = KivyApp.get_running_app()
        if self.app.installed:
            kivy_app.apps.uninstall(self.app)
            self.ids.install_button.disabled = True
        else:
            app = kivy_app.apps.install(self.app)
            self.ids.tip_button.disabled = False
            self.app = app
        kivy_app.root.ids.app_menu.close_all()
        kivy_app.root.ids.app_menu.populate_scripts()


class Tab(MDFloatLayout, MDTabsBase):
    """Class implementing content for a tab."""


class AppStoreDialog(PopupDropShadow):
    """
    The AppStore displays apps, and allows installing and uninstalling
    apps in Orb.

    The installed apps are loaded from the file-system, while the available
    apps are loaded from a remote data source.
    """

    def open(self, *args):
        """
        Open the AppStore.
        """
        super(AppStoreDialog, self).open(self, *args)
        authenticate()
        self.load_installed()

    def load_installed(self):
        # phew!
        apps = KivyApp.get_running_app().apps.apps
        for app in apps.values():
            app_summary = AppSummary(app)
            app_summary.bind(selected=self.on_selected)
            self.ids.installed.add_widget(app_summary)

    def on_selected(self, widget, val):
        self.ids.tabs.switch_tab("Details")
        self.ids.details.clear_widgets()
        self.ids.details.add_widget(AppDetails(app=widget.app))

    @guarded
    def on_tab_switch(self, instance_tabs, instance_tab, instance_tab_label, tab_text):
        if tab_text == "Installed":
            self.ids.installed.clear_widgets()
            self.load_installed()
        elif tab_text == "Available":
            self.ids.available.clear_widgets()
            self.load_available()

    def load_available(self):
        for app in KivyApp.get_running_app().apps.get_remote_apps():
            app_summary = AppSummary(app)
            app_summary.bind(selected=self.on_selected)
            self.ids.available.add_widget(app_summary)
