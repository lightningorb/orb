# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-15 07:15:28
# @Last Modified by:   lnorb.com
# @Last Modified time: 2021-12-30 07:24:00

import os
from kivy.uix.screenmanager import Screen
from kivy.uix.videoplayer import VideoPlayer


class PlayerScreen(Screen):
    built = False

    def on_enter(self):
        if not self.built:
            path = os.path.expanduser(
                "~/Movies/Monosnap/screencast 2021-12-29 17-28-56.mp4"
            )
            player = VideoPlayer(source=path)
            self.ids.bl.add_widget(player)
            self.built = True
