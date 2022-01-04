# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-15 07:15:28
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-01-04 12:51:37

import requests
import os

from kivy.uix.screenmanager import Screen
from kivy.uix.videoplayer import VideoPlayer

from kivy.app import App


class PlayerScreen(Screen):
    built = False

    def download(self):
        user_data_dir = App.get_running_app().user_data_dir
        path = f"{user_data_dir}/small.mp4"
        if os.path.exists(path):
            return
        url = "http://techslides.com/demos/sample-videos/small.mp4"
        response = requests.get(url)
        totalbits = 0
        if response.status_code == 200:
            with open(path, "wb") as f:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        totalbits += 1024
                        print("Downloaded", totalbits * 1025, "KB...")
                        f.write(chunk)

    def on_enter(self):
        user_data_dir = App.get_running_app().user_data_dir
        path = f"{user_data_dir}/small.mp4"

        if not self.built:
            self.download()
            player = VideoPlayer(source=path)
            self.ids.bl.add_widget(player)
            self.built = True
