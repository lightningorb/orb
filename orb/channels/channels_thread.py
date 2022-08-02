# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-15 07:15:28
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-08-03 07:28:02

import base64
import codecs
import threading
from time import sleep
from traceback import format_exc

from orb.lnd import Lnd
from orb.misc.channel import Channel
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
                        if hasattr(e, "inactive_channel"):
                            c = e.inactive_channel
                            tb = c.funding_txid_bytes
                            funding_txid_bytes = (
                                tb if type(tb) is bytes else base64.b64decode(tb)
                            )
                            funding_txid_str = codecs.encode(
                                funding_txid_bytes, "hex"
                            ).decode()
                            cp = f"{funding_txid_str}:{c.output_index}"
                            chan = next(
                                iter(
                                    x
                                    for x in self.inst.channels.channels.values()
                                    if x.channel_point == cp
                                ),
                                None,
                            )
                            if chan:
                                chan.active = False
                            # else:
                            #     print(f"Channel point not found: {cp}")
                        if hasattr(e, "active_channel"):
                            c = e.active_channel
                            tb = c.funding_txid_bytes
                            funding_txid_bytes = (
                                tb if type(tb) is bytes else base64.b64decode(tb)
                            )
                            funding_txid_str = codecs.encode(
                                funding_txid_bytes, "hex"
                            ).decode()
                            cp = f"{funding_txid_str}:{c.output_index}"
                            chan = next(
                                iter(
                                    x
                                    for x in self.inst.channels.channels.values()
                                    if x.channel_point == cp
                                ),
                                None,
                            )
                            if chan:
                                chan.active = True
                            # else:
                            #     print(f"Channel point not found: {cp}")
                        if hasattr(e, "open_channel"):
                            o = e.open_channel
                            if o.chan_id:
                                self.inst.channels.get()
                                channel = self.inst.channels.channels[o.chan_id]
                                self.inst.add_channel(channel, update=True)
                                channel.get_policies()
                        if hasattr(e, "pending_open_channel"):
                            p = e.pending_open_channel
                            print(
                                f"PENDING OPEN: index: {p.output_index}, txid: {p.txid}"
                            )
                        if hasattr(e, "closed_channel"):
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
                                self.inst.update()
            except:
                print("Exception getting Channels - let's sleep")
                print(format_exc())
                sleep(10)
            sleep(10)

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()
