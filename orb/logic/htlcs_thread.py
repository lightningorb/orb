# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-15 07:15:28
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-01-02 17:00:05
import json
import threading
from time import sleep
from traceback import print_exc
from threading import Lock, Thread

from munch import Munch

from orb.lnd import Lnd
from orb.misc.prefs import is_rest
from orb.logic.thread_manager import thread_manager

db_lock = Lock()


class HTLCsThread(threading.Thread):
    def __init__(self, inst, name, *args, **kwargs):
        super(HTLCsThread, self).__init__(*args, **kwargs)
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
        from orb.logic.htlc import Htlc

        rest = is_rest()
        while not self.stopped():
            try:
                lnd = Lnd()
                for e in lnd.get_htlc_events():
                    if self.stopped():
                        return
                    self.inst.update_rect()
                    if rest:
                        e = Munch.fromDict(json.loads(e)["result"])
                    htlc = Htlc(lnd, e)

                    # prevent routing from a low outbound channel to
                    # a channel with zero fees. or for example prevent
                    # routing from a low local channel to LOOP
                    # data_manager.data_man.lnd.htlc_interceptor(self, chan_id, htlc_id, action=1)

                    with db_lock:
                        htlc.save()
                    for cid in self.inst.cn:
                        chans = [
                            e.outgoing_channel_id
                            if hasattr(e, "outgoing_channel_id")
                            else None,
                            e.incoming_channel_id
                            if hasattr(e, "incoming_channel_id")
                            else None,
                        ]
                        if self.inst.cn[cid].l.channel.chan_id in chans:
                            Thread(
                                target=lambda *_: self.inst.cn[cid].l.anim_htlc(htlc)
                            ).start()
                            self.inst.ids.relative_layout.do_layout()

            except:
                print("Exception getting HTLCs - let's sleep")
                print_exc()
                sleep(10)

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()
