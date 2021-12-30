# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-15 07:15:28
# @Last Modified by:   lnorb.com
# @Last Modified time: 2021-12-30 11:37:57

from kivy.event import EventDispatcher
from kivy.properties import ListProperty
from orb.misc.channel import Channel


class Channels(EventDispatcher):

    """
    This class should hold all the currently existing Channels,
    as :py:mod:`orb.misc.channel.Channel` objects.

    The purpose is that it's expensive getting channels over
    and over from LND. This this class offers a way to read
    and effectively cache channel data.

    In addition to caching, it also uses Kivi's properties
    and event dispatcher mechanism so the application can observe
    channel attribute changes.

    Please note this class is iterable.
    """

    #: the channels as a ListProperty
    channels = ListProperty([])

    def __init__(self, lnd):
        """
        Class initializer. Takes the lnd object, and gets
        and sorts channel data.
        """
        self.lnd = lnd
        self.get()

    def get(self):
        """
        Get and sorts channel data.
        """
        self.channels = [Channel(c) for c in self.lnd.get_channels()]
        self.sort_channels()

    def sort_channels(self):
        """
        Sort channel data based on channel ratio.
        """
        self.channels.sort(
            key=lambda x: int(x.local_balance) / int(x.capacity),
            reverse=True,
        )

    @property
    def global_ratio(self):
        cb = self.lnd.channel_balance()
        return int(cb.local_balance.sat) / (
            int(cb.local_balance.sat) + int(cb.remote_balance.sat)
        )

    def __len__(self):
        return len(self.channels)

    def __iter__(self):
        self.it = 0
        return self

    def __next__(self):
        if self.it < len(self):
            ret = self.channels[self.it]
            self.it += 1
        else:
            raise StopIteration
        return ret
