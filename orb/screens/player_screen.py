# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-15 07:15:28
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-01-02 07:07:15

import os
from kivy.uix.screenmanager import Screen
from kivy.uix.videoplayer import VideoPlayer


class PlayerScreen(Screen):
    built = False

    def on_enter(self):
        if not self.built:
            player = VideoPlayer(
                source=os.path.expanduser("~/Desktop/vids/batch_open.mp4")
            )
            self.ids.bl.add_widget(player)
            self.built = True
