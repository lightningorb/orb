# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-01-12 16:23:08
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-01-14 14:44:12

import os
from pathlib import Path
from functools import lru_cache
from time import time
import requests
from collections import defaultdict

from kivy.app import App
from kivy.properties import NumericProperty
from kivy.event import EventDispatcher

from orb.misc.stoppable_thread import StoppableThread
from orb.misc.utils import pref


class Base(EventDispatcher, StoppableThread):

    progress = NumericProperty(0)
    is_complete = NumericProperty(-1)

    def __init__(self, url, *args, **kwargs):
        super(Base, self).__init__(*args, **kwargs)
        self.url = url
        self.DOWNLOAD_FOLDER = Path(App.get_running_app().user_data_dir) / pref(
            "path.video"
        )
        if not self.DOWNLOAD_FOLDER.is_dir():
            self.DOWNLOAD_FOLDER.mkdir()
        self.file = self.DOWNLOAD_FOLDER / url.split("/")[-1]
        self.bps = defaultdict(int)
        self.i = 0
        self.av_mbps_cache = 0
        self.max_mbps_cache = 0

    @property
    @lru_cache(maxsize=None)
    def file_size_online(self):
        r = requests.head(self.url)
        return int(r.headers.get("content-length", 0))

    @property
    def file_size_offline(self):
        return self.file.stat().st_size if self.file.exists() else 0

    @property
    def av_mbps(self):
        if self.i % 100 == 0:
            self.av_mbps_cache = sum(self.bps.values()) / len(self.bps)
        return self.av_mbps_cache

    @property
    def max_mbps(self):
        if self.i % 100 == 0:
            self.max_mbps_cache = max(self.bps.values())
        return self.max_mbps_cache

    @property
    def check_is_complete(self):
        self.progress = self.file_size_offline / self.file_size_online
        return self.progress == 1.0


class CheckComplete(Base):
    def __init__(self, url):
        super(CheckComplete, self).__init__(url)

    def run(self):
        self.check_is_complete
        self.is_complete = int(self.progress == 1.0)
        self.stop()


class DownloadThread(Base):
    def __init__(self, url):
        super(DownloadThread, self).__init__(url)

    def run(self):
        print("Starting the download")
        if self.file.exists():
            if not self.check_is_complete:
                print(f"File {self.file} is incomplete. Resume download.")
                self.downloader(resume_byte_pos=self.file_size_offline)
            else:
                print(f"File {self.file} is complete. Skip download.")
        else:
            print(f"File {self.file} does not exist. Start download.")
            self.downloader()
        self.stop()

    def downloader(self, resume_byte_pos=0):
        print(f"Requesting {self.file} for download")
        r = requests.get(
            self.url,
            stream=True,
            headers=({"Range": f"bytes={resume_byte_pos}-"}),
        )
        print(f"Got {self.file} with status code: {r.status_code}")
        block_size, total = 2 ** 15, resume_byte_pos

        with open(self.file, "ab" if resume_byte_pos else "wb") as f:
            for chunk in r.iter_content(chunk_size=block_size):
                if chunk and not self.stopped():
                    total += block_size
                    self.i += 1
                    self.bps[int(time())] += block_size
                    self.progress = total / self.file_size_online
                    f.write(chunk)
                    print(
                        f"Downloaded {round((total/(2**20)), 2):,} Mib ({round(self.progress*100, 2)}% @ an av. of {round(self.av_mbps/2**20, 2)} Mib/s and max {round(self.max_mbps/2**20, 2)} Mib/s)"
                    )
                else:
                    break
        if self.check_is_complete:
            print(f"Finished Downloading {self.file}")
