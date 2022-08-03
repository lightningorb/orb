# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-30 07:25:42
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-08-03 11:31:47

from kivy.app import App
from kivy.clock import Clock
from kivy.clock import mainthread
from kivymd.uix.screen import MDScreen
from kivy.app import App

from orb.channels.channels_widget import ChannelsWidget
from orb.misc.decorators import guarded
from orb.logic.gestures_delegate import GesturesDelegate


class ChannelsScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super(ChannelsScreen, self).__init__(*args, **kwargs)
        self.channels_widget = None
        self.menu_built = False

    def on_enter(self, *args):
        @mainthread
        def delayed():
            app = App.get_running_app()
            try:
                app.root.ids.app_menu.add_channels_menu()
            except:
                print("FAILED TO ADD CHANNELS MENU")

        delayed()

        if not self.channels_widget:
            Clock.schedule_once(self.build, 2)

    @guarded
    def build(self, *_):
        @guarded
        @mainthread
        def delayed():
            self.gestures_delegate = GesturesDelegate(overlay=self.ids.gestures_overlay)
            self.channels_widget = ChannelsWidget(
                gestures_delegate=self.gestures_delegate,
            )
            self.ids.cw_layout.add_widget(self.channels_widget)
            App.get_running_app().bind(
                selection=lambda w, s: self.ids.nav_drawer.set_state("open")
                if s
                else None
            )

            def state_change(w, s):
                if s == "close":
                    App.get_running_app().selection = None

            self.ids.nav_drawer.bind(state=state_change)

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
