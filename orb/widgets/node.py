# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-15 07:15:28
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-08-06 08:26:25

from threading import Thread

from kivy.animation import Animation
from kivy.properties import ListProperty, ObjectProperty, BooleanProperty
from kivy.uix.button import Button
from kivy.app import App

from orb.misc.utils import prefs_col, pref
from orb.lnd import Lnd


class Node(Button):
    channel = ObjectProperty(None)
    touch_start = ListProperty([0, 0])
    touch_end = ListProperty([0, 0])
    round = BooleanProperty(False)
    selected = BooleanProperty(False)

    def __init__(self, *args, **kwargs):
        super(Node, self).__init__(*args, **kwargs)
        if self.channel:
            Thread(
                target=lambda: setattr(
                    self, "text", Lnd().get_node_alias(self.channel.remote_pubkey)
                )
            ).start()
        App.get_running_app().bind(selection=self.set_selected)
        if self.channel:
            self.channel.bind(active=self.set_active)
            self.anim_col()

    @property
    def colour(self):
        if self.channel.active:
            new_col_str = (
                "display.node_background_color",
                "display.node_selected_background_color",
            )[self.selected]
            return prefs_col(new_col_str)
        return (0.1, 0.1, 0.1, 1)

    def set_active(self, widget, active):
        self.anim_col()

    def set_selected(self, widget, channel):
        if self.channel:
            self.selected = channel == self.channel
            self.anim_col()

    def anim_col(self):
        col = self.canvas.before.get_group("b")[0]
        (
            Animation(
                rgba=self.colour,
                duration=0.2,
            )
        ).start(col)

    def anim_to_pos(self, pos):
        Animation(pos=pos, duration=1).start(self)

    def on_release(self):
        if self.channel:
            App.get_running_app().selection = self.channel

    def on_touch_down(self, touch):
        app = App.get_running_app()
        if self.collide_point(*touch.pos):
            if app.menu_visible:
                return False
        return super(Node, self).on_touch_down(touch)

    @property
    def width_pref(self):
        return pref("display.node_height") if self.round else pref("display.node_width")

    @property
    def height_pref(self):
        return pref("display.node_height")
