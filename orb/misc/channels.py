# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-01-01 10:03:46
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-03-28 15:30:09

from traceback import print_exc
import concurrent.futures
import urllib.request
from threading import Thread

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
        Clock.schedule_interval(self.compute_balanced_ratios, 30)
        Clock.schedule_once(lambda *_: Thread(target=self.get_chan_policies).start(), 5)
        Clock.schedule_interval(
            lambda *_: Thread(target=self.get_chan_policies).start(), 5 * 60
        )

    def get_chan_policies(self, *_):
        def get_policies(channel):
            channel.get_policies()

        with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:
            future_to_channel = {
                executor.submit(get_policies, c): c for c in self.channels.values()
            }
            for future in concurrent.futures.as_completed(future_to_channel):
                channel = future_to_channel[future]
                try:
                    data = future.result()
                except Exception as exc:
                    print("%r generated an exception: %s" % (channel, exc))

    def remove(self, channel):
        del self.channels[channel.chan_id]
        self.sorted_chan_ids.remove(channel.chan_id)

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
        local = self.local_balance_include_pending
        return local / self.capacity if self.capacity else 0

    @property
    def local_balance(self):
        return sum(x.local_balance for x in self.channels.values())

    @property
    def local_balance_include_pending(self):
        return sum(x.local_balance_include_pending for x in self.channels.values())

    @property
    def remote_balance(self):
        return sum(x.remote_balance for x in self.channels.values())

    @property
    def remote_balance_include_pending(self):
        return sum(x.remote_balance_include_pending for x in self.channels.values())

    @property
    def capacity(self):
        local = self.local_balance_include_pending
        remote = self.remote_balance_include_pending
        return local + remote

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
        capacity = self.capacity
        if capacity == 0:
            return

        def search(solution, indices, global_ratio):
            low, mid, high, n = 0, 0, 1, 0
            while low <= high:
                mid = (high + low) / 2
                for i in indices:
                    solution[i] = mid
                ratio = (
                    sum(
                        [
                            x.capacity * y
                            for x, y in zip([*self.channels.values()], solution)
                        ]
                    )
                    / capacity
                )
                abs_diff = abs(ratio - global_ratio)
                n += 1
                if abs_diff < 1 / 1e5 or n > 100:
                    return ratio
                low, high = (mid, high) if ratio < global_ratio else (low, mid)
            return ratio

        search(solution, indices, gr)
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
