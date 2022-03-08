# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-01-06 17:51:07
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-01-21 12:02:30

from kivy.uix.popup import Popup
from orb.misc.plugin import Plugin
from fabric import Connection
import os
from orb.misc.prefs import hostname
from orb.misc.utils import pref


class ChannelsDbSize(Plugin):
    def main(self):
        kwargs = {"key_filename": os.path.expanduser("~/.rln/lnd4/lnd4.pem")}
        with Connection(hostname(), connect_kwargs=kwargs, user="ubuntu") as c:
            cmd = f"ls -hs .lnd/data/graph/{pref('lnd.network')}/channel.db"
            out = c.run(cmd).stdout
            size = next(iter(out.split()), "could not get size")
            print(size)
