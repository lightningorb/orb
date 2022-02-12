# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-01-01 10:03:46
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-02-12 08:46:04

from traceback import print_exc

from kivy.event import EventDispatcher
from kivy.properties import ListProperty
from kivy.properties import DictProperty
from kivy.clock import Clock

from orb.misc.channel import Channel
from orb.misc.utils import pref
from orb.misc import data_manager


class Channels(EventDispatcher):

    """
    This class should hold all the currently existing Channels,
    as :py:mod:`orb.misc.channel.Channel` objects.

    The purpose is that it's expensive getting channels over
    and over from LND. This class offers a way to read
    and effectively cache channel data.

    In addition to caching, it also uses Kivi's properties
    and event dispatcher mechanism so the application can observe
    channel attribute changes.

    The object ids in self.channels should not change. Instead
    channels should be added and removed. This enables the
    rest of the application classes to bind data to these
    objects.

    Please note this class is iterable.
    """

    #: the channels as a DictProperty
    channels = DictProperty({})
    #: the sorted channels chan_ids
    sorted_chan_ids = ListProperty([])

    def __init__(self, lnd):
        """
        Class initializer. Takes the lnd object, and gets
        and sorts channel data.
        """
        self.lnd = lnd
        self.get()
        Clock.schedule_once(self.compute_balanced_ratios, 0)
        self.interval = Clock.schedule_interval(self.compute_balanced_ratios, 30)

    def get(self):
        """
        Get and sorts channel data.
        """
        try:
            for c in self.lnd.get_channels():
                chan_id = int(c.chan_id)
                if chan_id in self.channels:
                    self.channels[chan_id].update(c)
                else:
                    self.channels[chan_id] = Channel(c)
            self.sorted_chan_ids = [int(x) for x in self.channels]
            self.sort_channels()
        except:
            print_exc()
            print("Failed to get channels")

    def sort_channels(self):
        """
        Sort channel data based on channel ratio.
        """

        sorter = {
            "ratio": (
                lambda x: self.channels[x].local_balance_include_pending
                / self.channels[x].capacity
            ),
            "capacity": lambda x: self.channels[x].capacity,
            "total-sent": lambda x: self.channels[x].total_satoshis_sent,
            "total-received": lambda x: self.channels[x].total_satoshis_received,
            "out-ppm": lambda x: self.channels[x].fee_rate_milli_msat,
        }

        self.sorted_chan_ids.sort(
            key=sorter[pref("display.channel_sort_criteria")],
            reverse=True,
        )

    @property
    def global_ratio(self):
        """
        Compute the global ratio, i.e local / capacity.
        """
        cb = self.lnd.channel_balance()
        local = int(cb.unsettled_local_balance.sat) + int(cb.local_balance.sat)
        remote = int(cb.unsettled_remote_balance.sat) + int(cb.remote_balance.sat)
        return local / (local + remote)

    def compute_balanced_ratios(self, *_):
        solution = []
        channels = [x for x in self.channels.values()]
        for c in channels:
            solution.append(
                data_manager.data_man.store.get("balanced_ratio", {}).get(
                    str(c.chan_id), -1
                )
            )
        gr = self.global_ratio
        indices = [i for i, x in enumerate(solution) if x == -1]

        def binary_search(arr, gr):
            low, mid, high = 0, 0, 1
            while low <= high:
                mid = (high + low) / 2
                for i in indices:
                    arr[i] = mid
                ratio = sum(arr) / len(arr)
                abs_diff = abs(ratio - gr)
                if abs_diff < 0.0001:
                    return ratio
                if ratio < gr:
                    low += 0.00001
                elif ratio > gr:
                    high -= 0.00001
            return ratio

        binary_search(solution, 0.5)
        for i, c in enumerate(channels):
            channels[i].balanced_ratio = solution[i]

    def __len__(self):
        return len(self.sorted_chan_ids)

    def __iter__(self):
        self.it = 0
        return self

    def __next__(self):
        if self.it < len(self):
            ind = self.sorted_chan_ids[self.it]
            self.it += 1
        else:
            raise StopIteration
        return self.channels[ind]
