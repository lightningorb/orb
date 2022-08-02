# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-15 07:15:28
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-08-01 17:33:58

import threading
from time import sleep
from traceback import print_exc

from kivy.app import App
from kivy.clock import mainthread

from orb.lnd import Lnd
from orb.logic.thread_manager import thread_manager


class InvoicesThread(threading.Thread):
    def __init__(self, inst, name, *args, **kwargs):
        super(InvoicesThread, self).__init__(*args, **kwargs)
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
        @mainthread
        def mainthread_anim(cid, htlc):
            self.inst.cn[cid].l.anim_htlc(htlc)
            self.inst.ids.relative_layout.do_layout()

        @mainthread
        def mainthread_update():
            self.inst.update()

        while not self.stopped():
            try:
                lnd = Lnd()
                for e in lnd.get_invoice_events():
                    if self.stopped():
                        return
                    if e.state == "SETTLED":
                        chan_id = e.htlcs[0].chan_id
                        self.inst.channels.channels[chan_id].local_balance += int(
                            e.amt_paid_msat / 1000
                        )
                        self.inst.channels.channels[chan_id].remote_balance -= int(
                            e.amt_paid_msat / 1000
                        )
                        App.get_running_app().main_layout.ids.sm.get_screen(
                            "channels"
                        ).channels_widget.update()

            except:
                print("Exception getting Invoices - let's sleep")
                print_exc()
                sleep(10)

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()
