# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-01-16 06:56:19
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-01-16 06:59:39

from orb.misc.plugin import Plugin
from orb.misc import data_manager


class UpdateChannels(Plugin):
    def main(self):
        print("Getting channels")
        data_manager.data_man.channels.get()
        print("Channels updated")

    @property
    def menu(self):
        return "wip > UpdateChannels"

    @property
    def uuid(self):
        return "dcdd9858-e65a-460c-a0c1-4d81b84ffce8"
