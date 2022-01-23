# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-15 07:15:28
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-01-22 11:18:42

from threading import Thread

from kivymd.uix.tab import MDTabsBase
from kivymd.uix.floatlayout import MDFloatLayout
from kivy.app import App as KivyApp
from kivy.clock import mainthread

from orb.components.popup_drop_shadow import PopupDropShadow
from orb.dialogs.app_store.app_details.app_detais import AppDetails
from orb.dialogs.app_store.app_summary.app_summary import AppSummary
from orb.misc.decorators import guarded


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
        self.available = []

        def get_remote_apps(*_):
            self.available = KivyApp.get_running_app().apps.get_remote_apps()
            self.load_available()

        Thread(target=get_remote_apps).start()
        self.load_installed()

    def load_installed(self):
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
            self.load_available()

    @mainthread
    def load_available(self):
        self.ids.available.clear_widgets()
        for app in self.available:
            app_summary = AppSummary(app)
            app_summary.bind(selected=self.on_selected)
            self.ids.available.add_widget(app_summary)
