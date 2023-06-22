# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-15 07:15:28
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-08-24 09:33:45

import threading
from time import sleep
from traceback import format_exc

from kivy.app import App
from kivy.clock import mainthread

from orb.ln import Ln
from orb.core.stoppable_thread import StoppableThreadHidden


class HTLCsThread(StoppableThreadHidden):
    def __init__(self, inst, name, *args, **kwargs):
        super(HTLCsThread, self).__init__(*args, **kwargs)
        self._stop_event = threading.Event()
        self.inst = inst
        self.count = 0

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
                print(format_exc())

        @mainthread
        def mainthread_update():
            self.inst.update()

        app = App.get_running_app()

        while not self.stopped():
            try:
                for htlc in Ln().get_htlc_events():
                    self.count += 1
                    # if self.count % 20 == 0:
                    app.channels.get()
                    if self.stopped():
                        return

                    for plugin in app.plugin_registry.values():
                        try:
                            plugin.htlc_event(htlc)
                        except:
                            print(f"HTLCs error in plugin: {plugin}")

                    for cid in [
                        x
                        for x in [htlc.outgoing_channel_id, htlc.incoming_channel_id]
                        if x
                    ]:
                        mainthread_anim(str(cid), htlc)

            except:
                print("Exception getting HTLCs - let's sleep")
                print(format_exc())
                sleep(10)
