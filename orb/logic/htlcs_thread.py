# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-15 07:15:28
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-08-01 10:10:32
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
            try:
                self.inst.cn[cid].l.anim_htlc(htlc)
                self.inst.ids.relative_layout.do_layout()
            except:
                pass

        @mainthread
        def mainthread_update():
            self.inst.update()

        while not self.stopped():
            try:
                lnd = Lnd()
                # events = []
                for e in lnd.get_htlc_events():
                    self.count += 1
                    # events.append(e.todict())
                    if self.count % 20 == 0:
                        data_manager.data_man.channels.get()
                    # with open("events.json", "w") as f:
                    #     f.write(json.dumps(events, indent=4))
                    if self.stopped():
                        return
                    htlc = Htlc.init(e)
                    # htlc.save()

                    for plugin in data_manager.data_man.plugin_registry.values():
                        try:
                            plugin.htlc_event(htlc)
                        except:
                            print(f"HTLCs error in plugin: {plugin}")

                    for cid in [
                        x for x in [e.outgoing_channel_id, e.incoming_channel_id] if x
                    ]:
                        mainthread_anim(cid, htlc)

            except:
                print("Exception getting HTLCs - let's sleep")
                print_exc()
                sleep(10)

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()
