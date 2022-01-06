# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-30 07:25:42
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-01-06 13:44:08

from kivy.app import App
from kivy.clock import Clock
from kivy.clock import mainthread
from kivymd.uix.screen import MDScreen

from orb.channels.channels_widget import ChannelsWidget
from orb.misc.decorators import guarded


class ChannelsScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super(ChannelsScreen, self).__init__(*args, **kwargs)
        self.channels_widget = None
        self.menu_built = False

    def on_enter(self, *args):
        @mainthread
        def delayed():
            app = App.get_running_app()
            app.root.ids.app_menu.add_channels_menu()
            self.menu_built = True

        if not self.menu_built:
            delayed()

        if not self.channels_widget:
            Clock.schedule_once(self.build, 2)

    @guarded
    def build(self, *_):
        @mainthread
        def delayed():
            self.channels_widget = ChannelsWidget(
                attribute_editor=self.ids.content_drawer
            )
            self.ids.cw_layout.add_widget(self.channels_widget)
            self.ids.content_drawer.bind(
                channel=lambda *_: self.ids.nav_drawer.set_state(
                    "open" if self.ids.content_drawer.channel else "close"
                )
            )

        delayed()

    @guarded
    def refresh(self, *_, **__):
        if self.channels_widget:
            self.channels_widget.htlcs_thread.stop()
            self.channels_widget.channels_thread.stop()
            self.ids.cw_layout.clear_widgets()
            self.build()
            app = App.get_running_app()
            app.root.ids.app_menu.close_all()
