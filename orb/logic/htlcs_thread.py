# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-15 07:15:28
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-08-06 10:29:54

import threading
from time import sleep
from threading import Lock
from traceback import print_exc

from kivy.app import App
from kivy.clock import mainthread

from orb.lnd import Lnd
from orb.logic.thread_manager import thread_manager


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

        app = App.get_running_app()

        while not self.stopped():
            try:
                lnd = Lnd()
                for e in lnd.get_htlc_events():
                    self.count += 1
                    if self.count % 20 == 0:
                        app.channels.get()
                    if self.stopped():
                        return
                    htlc = Htlc.init(e)
                    if False:
                        htlc.save()

                    for plugin in app.plugin_registry.values():
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
