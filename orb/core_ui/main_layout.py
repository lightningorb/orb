# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-15 07:15:28
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-01-10 10:17:25

import os

from kivy.properties import ObjectProperty
from kivy.clock import mainthread
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.core.window import Window, Keyboard
from kivy.uix.videoplayer import VideoPlayer
import data_manager
from kivy.utils import platform

ios = platform == "ios"


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
        if not ios:
            keyboard = Window.request_keyboard(self._keyboard_released, self)
            keyboard.bind(
                on_key_down=self._keyboard_on_key_down,
                on_key_up=self._keyboard_released,
            )
        self.super = []
        self.shift = False

        @mainthread
        def delayed():
            app = App.get_running_app()
            app.root.ids.app_menu.populate_scripts()
            show_player = False
            # to test out the video player, change the parent to a RelativeLayout
            # and uncomment the Scatter in the .kv file.
            if show_player:
                self.ids.scatter.add_widget(
                    VideoPlayer(
                        size=[800, 500],
                        source=os.path.expanduser("~/Desktop/vids/rankings.mp4"),
                    )
                )

        delayed()

    def on_menu_visible(self, *args):
        """
        This callback is because Kivy has trouble handling focus
        with the submenu system. Thus we track when the menu is visible,
        and all Widgets in the application need to ensure not recieving
        clicks when the menu is showing.
        """
        data_manager.data_man.menu_visible = self.menu_visible

    def _keyboard_released(self, window=None, key=None):
        if data_manager.data_man.disable_shortcuts:
            return
        if key:
            code, key = key
            if key == "shift":
                self.shift = False

    def _keyboard_on_key_down(self, window, key, text, super):
        data_man = data_manager.data_man
        if data_man.disable_shortcuts:
            return
        code, key = key
        if key == "shift":
            self.shift = True
            return False
        if self.shift and key == "c":
            data_man.show_chords = not data_man.show_chords
            return False
        if key == "j":
            data_man.show_chord += 1
        if key == "k":
            data_man.show_chord -= 1
        if key == "i":
            data_man.chords_direction = 0
        if key == "o":
            data_man.chords_direction = 1
        return False
