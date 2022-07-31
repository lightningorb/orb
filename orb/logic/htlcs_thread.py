# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-15 07:15:28
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-07-31 15:38:06
import json
import threading
from time import sleep
from traceback import print_exc
from threading import Lock
from kivy.clock import mainthread

from orb.lnd import Lnd
from orb.misc.prefs import is_rest
from orb.logic.thread_manager import thread_manager
from orb.misc.auto_obj import dict2obj
from orb.misc import data_manager

from orb.logic.htlc import Htlc

db_lock = Lock()


class HTLCsThread(threading.Thread):
    def __init__(self, inst, name, *args, **kwargs):
        super(HTLCsThread, self).__init__(*args, **kwargs)
        self._stop_event = threading.Event()
        self.inst = inst
        self.name = name
        self.count = 0
        thread_manager.add_thread(self)

    def run(self):
        try:
            self.__run()
        except:
            self.stop()

    def __run(self):
        @mainthread
        def mainthread_anim(cid, htlc):
            self.inst.cn[cid].l.anim_htlc(htlc)
            self.inst.ids.relative_layout.do_layout()

        @mainthread
        def mainthread_update():
            self.inst.update()

        rest = is_rest()
        while not self.stopped():
            try:
                lnd = Lnd()
                for e in lnd.get_htlc_events():
                    self.count += 1
                    if self.count % 20 == 0:
                        data_manager.data_man.channels.get()

                    if self.stopped():
                        return
                    if rest:
                        e = dict2obj(json.loads(e)["result"])

                    with db_lock:
                        htlc = Htlc.init(e)
                        # htlc.save()

                    # prevent routing from a low outbound channel to
                    # a channel with zero fees. or for example prevent
                    # routing from a low local channel to LOOP
                    # data_manager.data_man.lnd.htlc_interceptor(self, chan_id, htlc_id, action=1)

                    for plugin in data_manager.data_man.plugin_registry.values():
                        try:
                            plugin.htlc_event(htlc)
                        except:
                            print(f"HTLCs error in plugin: {plugin}")

                    for cid in [
                        x for x in [e.outgoing_channel_id, e.incoming_channel_id] if x
                    ]:
                        # this "should" update the balances
                        # on the channel object
                        mainthread_anim(cid, htlc)

            except:
                print("Exception getting HTLCs - let's sleep")
                print_exc()
                sleep(10)

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()
