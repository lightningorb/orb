# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-15 07:15:28
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-08-24 09:34:07

import threading
from time import sleep
from traceback import print_exc

from kivy.app import App
from kivy.clock import mainthread

from orb.ln import Ln
from orb.core.stoppable_thread import StoppableThreadHidden


class InvoicesThread(StoppableThreadHidden):
    def __init__(self, inst, name, *args, **kwargs):
        super(InvoicesThread, self).__init__(*args, **kwargs)
        self.inst = inst

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
                for e in Ln().get_invoice_events():
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
