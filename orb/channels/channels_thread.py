# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-15 07:15:28
# @Last Modified by:   lnorb.com
# @Last Modified time: 2021-12-31 05:26:50

import threading
from time import sleep

from orb.lnd import Lnd
from orb.logic.thread_manager import thread_manager


class ChannelsThread(threading.Thread):
    def __init__(self, inst, name, *args, **kwargs):
        super(ChannelsThread, self).__init__(*args, **kwargs)
        self._stop_event = threading.Event()
        self.inst = inst
        self.name = name
        thread_manager.add_thread(self)

    def run(self):
        try:
            self.__run()
        except:
            self.stop()

    def __run(self):
        while not self.stopped():
            try:
                it = Lnd().get_channel_events()
                if it:
                    for e in it:
                        if self.stopped():
                            return
                        print(e)
                        if e.open_channel.chan_id:
                            self.inst.channels.channels.append(e.open_channel)
                            self.inst.add_channel(e.open_channel)
                        if e.closed_channel.chan_id:
                            to_remove = next(
                                iter(
                                    x
                                    for x in self.inst.channels.channels
                                    if x.chan_id == e.closed_channel.chan_id
                                ),
                                None,
                            )
                            if to_remove:
                                self.inst.channels.channels.remove(to_remove)
                                self.inst.remove_channel(e.closed_channel)
            except:
                print("Exception getting Channels - let's sleep")
                # print_exc()
                sleep(10)
            sleep(10)

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()
