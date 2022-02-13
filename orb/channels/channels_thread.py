# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-15 07:15:28
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-02-13 11:49:38

import threading
from time import sleep

from orb.lnd import Lnd
from orb.logic.thread_manager import thread_manager
from traceback import format_exc


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
                        if e.inactive_channel:
                            print(dir(e.inactive_channel))
                            """
                            inactive_channel {
                              funding_txid_bytes: "\350\035\010\310\204WC}\341\301\r\345Fn\273>\326\366_\213\251E\334%\346$\2447\301\032\267,"
                              output_index: 1
                            }
                            """
                        if e.active_channel:
                            print(dir(e.active_channel))
                            """
                            active_channel {
                              funding_txid_bytes: "\230&\303o\r\\m\204G\322?N\241\243\336j\333(\333\t\203\']\363\320Y\370\361\005\216\302\313"
                              output_index: 5
                            }
                            type: ACTIVE_CHANNEL
                            """
                        if e.open_channel.chan_id:
                            self.inst.channels.channels.append(e.open_channel)
                            self.inst.add_channel(e.open_channel)
                        if e.closed_channel.chan_id:
                            to_remove = next(
                                iter(
                                    x
                                    for x in self.inst.channels.channels.values()
                                    if x.chan_id == e.closed_channel.chan_id
                                ),
                                None,
                            )
                            if to_remove:
                                print(f"removing channel {to_remove.chan_id}")
                                self.inst.channels.remove(to_remove)
                                self.inst.remove_channel(to_remove)
            except:
                print("Exception getting Channels - let's sleep")
                print(format_exc())
                sleep(10)
            sleep(10)

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()
