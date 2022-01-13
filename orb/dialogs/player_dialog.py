# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-15 07:15:28
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-01-12 20:35:42

import os
from functools import partial
from kivy.clock import mainthread

from kivy.properties import (
    StringProperty,
    ListProperty,
    NumericProperty,
)
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.videoplayer import VideoPlayer
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.tab import MDTabsBase
from kivy.app import App

from orb.components.popup_drop_shadow import PopupDropShadow
from orb.store.video_library import load_video_library
from orb.logic.download_thread import DownloadThread, CheckComplete


class Tab(MDFloatLayout, MDTabsBase):
    """Class implementing content for a tab."""


class VideoWidget(BoxLayout):
    name = StringProperty("")
    title = StringProperty("")
    is_complete = NumericProperty(0)

    def __init__(self, *args, **kwargs):
        super(VideoWidget, self).__init__(*args, **kwargs)
        self.ids.button.bind(on_press=self.video_clicked)
        self.download_thread = None
        self.url = f"https://lnorb.s3.us-east-2.amazonaws.com/vids/{self.name}"

    def video_clicked(self, *args):
        """
        Callback for when the video is clicked.
        First checks if it's downloaded, if it is
        then it opens it, else it downloads it.
        Warning, async fun ahead.
        """
        if not self.download_thread:

            def open_or_dl(widget, is_complete):
                print("open_or_dl")
                self.check_complete_thread.unbind(is_complete=open_or_dl)
                if is_complete == 1:
                    print("OPEN THE VIDEO")
                    self.check_complete_thread = None
                    self.is_complete += 1
                elif is_complete == 0:
                    print("START THE DOWNLOAD")
                    self.download_thread = DownloadThread(url=self.url)
                    self.download_thread.daemon = True
                    self.download_thread.start()

            self.check_complete_thread = CheckComplete(url=self.url)
            self.check_complete_thread.daemon = True
            self.check_complete_thread.bind(is_complete=open_or_dl)
            self.check_complete_thread.start()

        else:
            self.download_thread.stop()
            self.download_thread = None


class CollectionWidget(BoxLayout):
    name = StringProperty("")
    videos = ListProperty([])


class PlayerDialog(PopupDropShadow):
    def __init__(self, *args, **kwargs):
        super(PlayerDialog, self).__init__(*args, **kwargs)
        self.collection = None
        self.player = None

    def open(self):
        lib = load_video_library()
        for collection in lib.collections:
            collection_widget = CollectionWidget(**collection.__dict__)
            collection_widget.ids.button.bind(
                on_press=partial(self.collection_clicked, collection=collection)
            )
            self.ids.collections.add_widget(collection_widget)
        super(PlayerDialog, self).open()

    def collection_clicked(self, widget, collection):
        lib = load_video_library()
        self.ids.videos.clear_widgets()
        self.ids.tabs.switch_tab("Videos")
        for video in collection.videos:
            video_widget = VideoWidget(**video.__dict__)
            self.ids.videos.add_widget(video_widget)
            video_widget.bind(is_complete=self.open_video)

    @mainthread
    def open_video(self, widget, is_complete):
        print("open_video")
        user_data_dir = App.get_running_app().user_data_dir
        path = f"{user_data_dir}/{widget.name}"
        if self.player:
            self.player.state = "stop"
        self.ids.bl.clear_widgets()
        self.player = VideoPlayer(
            source=(path if os.path.exists(path) else None),
            options={"allow_stretch": True},
            state="play",
        )
        self.ids.bl.add_widget(self.player)
        self.ids.tabs.switch_tab("Player")

    def dismiss(self):
        print("Close")
        if self.player:
            self.player.state = "stop"
        super(PlayerDialog, self).dismiss()

    def on_tab_switch(self, instance_tabs, instance_tab, instance_tab_label, tab_text):
        pass
