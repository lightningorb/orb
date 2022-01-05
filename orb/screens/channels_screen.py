# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-30 07:25:42
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-01-05 17:38:55

from kivy.app import App
from kivy.clock import Clock
from kivy.clock import mainthread
from kivy.uix.screenmanager import Screen
from kivymd.uix.screen import MDScreen
from kivy.properties import ObjectProperty

from orb.channels.channels_widget import ChannelsWidget
from orb.misc.decorators import guarded

from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivymd.theming import ThemableBehavior
from kivymd.uix.list import MDList
from kivymd.uix.list import OneLineIconListItem
from kivy.properties import StringProperty
from kivymd.uix.textfield import MDTextField
from orb.attribute_editor.AE_channel import AEChannel


class DrawerList(MDList):
    pass


class ContentNavigationDrawer(BoxLayout):

    #: The currently selected channel object.
    channel = ObjectProperty(None, allownone=True)

    def __init__(self, *args, **kwargs):
        """
        Class constructor.
        """
        super(ContentNavigationDrawer, self).__init__(*args, **kwargs)
        self.bind(channel=self.on_selection_changed)

    def on_selection_changed(self, *_):
        """
        Invoked whenever a peer is selected.
        """
        if self.channel:
            self.ids.md_list.add_widget(AEChannel(channel=self.channel))

    def clear(self):
        """
        Clear the selection.
        """
        self.ids.md_list.clear_widgets()
        self.channel = None


class ItemDrawer(OneLineIconListItem):
    icon = StringProperty()


class ChannelsScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super(ChannelsScreen, self).__init__(*args, **kwargs)
        self.channels_widget = None

    def on_enter(self, *args):
        @mainthread
        def delayed():
            app = App.get_running_app()
            app.root.ids.app_menu.add_channels_menu()
            self.ids.nav_drawer.set_state("open")
            icons_item = {
                "folder": "My files",
                "account-multiple": "Shared with me",
                "star": "Starred",
                "history": "Recent",
                "checkbox-marked": "Shared with me",
                "upload": "Upload",
            }
            for icon_name in icons_item.keys():
                self.ids.content_drawer.ids.md_list.add_widget(
                    ItemDrawer(icon=icon_name, text=icons_item[icon_name])
                )

            widget = MDTextField(
                helper_text="this",
                helper_text_mode="persistent",
                text="that",
            )
            self.ids.content_drawer.ids.md_list.add_widget(widget)

        delayed()
        if not self.channels_widget:
            Clock.schedule_once(self.build, 2)

    @guarded
    def build(self, *args):
        @mainthread
        def delayed():
            self.channels_widget = ChannelsWidget(
                attribute_editor=self.ids.content_drawer
            )
            self.ids.cw_layout.add_widget(self.channels_widget)
            self.ids.content_drawer.bind(
                channel=lambda *_: self.ids.nav_drawer.set_state("open")
            )

        delayed()

    @guarded
    def refresh(self, *args, **kwargs):
        if self.channels_widget:
            self.channels_widget.htlcs_thread.stop()
            self.channels_widget.channels_thread.stop()
            self.ids.cw_layout.clear_widgets()
            self.build()
            app = App.get_running_app()
            app.root.ids.app_menu.close_all()
