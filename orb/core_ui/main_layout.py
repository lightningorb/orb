# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-15 07:15:28
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-08-08 11:28:28

import os

from kivy.properties import ObjectProperty
from kivy.clock import mainthread
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.uix.videoplayer import VideoPlayer

from orb.misc.utils import mobile, ios


class MainLayout(BoxLayout):
    """
    This is the main layout for the application. Edit with care!
    We inherit from BoxLayout vertically as the main UI elements are
    stacked, i.e the TopMenu, the main area, and the status line.
    """

    menu_visible = ObjectProperty()

    def __init__(self, *args, **kwargs):
        super(MainLayout, self).__init__(*args, **kwargs)
        # hack alert: the submenus are pretty buggy, and require
        # us to build them at the bottom off the screen then moving
        # them to the top. So we build this widget upside down and
        # then flip it.
        self.children = self.children[::-1]
        if False:
            keyboard = Window.request_keyboard(self._keyboard_released, self)
            keyboard.bind(
                on_key_down=self._keyboard_on_key_down,
                on_key_up=self._keyboard_released,
            )
        self.super = []
        self.shift = False

        #if ios:
            # self.ids.app_store_login.disabled = True
            # self.ids.app_store.disabled = True
        #    self.ids.upload_app.disabled = True

        @mainthread
        def delayed():
            app = App.get_running_app()
            try:
                app.root.ids.app_menu.populate_scripts()
            except:
                print("FAILED TO POPULATE SCRIPTS")

        delayed()

    def on_menu_visible(self, *args):
        """
        This callback is because Kivy has trouble handling focus
        with the submenu system. Thus we track when the menu is visible,
        and all Widgets in the application need to ensure not recieving
        clicks when the menu is showing.
        """
        app = App.get_running_app()
        app.menu_visible = self.menu_visible

    def _keyboard_released(self, window=None, key=None):
        app = App.get_running_app()
        if app.disable_shortcuts:
            return
        if key:
            code, key = key
            if key == "shift":
                self.shift = False

    def _keyboard_on_key_down(self, window, key, text, super):
        # TODO: Get rid of this
        app = App.get_running_app()
        if app.disable_shortcuts:
            return
        code, key = key
        if key == "shift":
            self.shift = True
            return False
        if self.shift and key == "c":
            app.show_chords = not app.show_chords
            return False
        if key == "j":
            app.show_chord += 1
        if key == "k":
            app.show_chord -= 1
        if key == "i":
            app.chords_direction = 0
        if key == "o":
            app.chords_direction = 1
        return False
