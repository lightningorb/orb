# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-15 07:27:21
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-03-08 09:57:51

from time import sleep
from kivy.clock import Clock
from threading import Thread

from orb.core.stoppable_thread import StoppableThread
from orb.lnd import Lnd
from orb.misc.plugin import Plugin
from orb.misc import data_manager
from kivy.utils import platform

ios = platform == "ios"


class MaxPolicy:
    half_cap = 0
    local_balance = 1


max_policy = MaxPolicy.local_balance


class UpdateMaxHTLC(StoppableThread):
    def main(self, *_):
        for i, c in enumerate(data_manager.data_man.channels.channels.values()):
            round = lambda x: int(int(x / 10_000) * 10_000)
            max_htlc = round(int(int(c.max_htlc_msat) / 1_000))
            if max_policy == MaxPolicy.half_cap:
                new_max_htlc = round(int(c.capacity * 0.5))
            elif max_policy == MaxPolicy.local_balance:
                new_max_htlc = round(int(c.local_balance))
            needs_update = max_htlc != new_max_htlc
            if needs_update:
                print(
                    f"Updating policy for: {c.chan_id}, max_htlc: {max_htlc}, new_max_htlc: {new_max_htlc}"
                )
                c.max_htlc_msat = new_max_htlc * 1_000
        print(f"Max HTLC updated")

    def run(self, *_):
        Clock.schedule_once(lambda _: Thread(target=self.main).start(), 1)
        self.schedule = Clock.schedule_interval(
            lambda _: Thread(target=self.main).start(), 10 * 60
        )
        while not self.stopped():
            sleep(5)

    def stop(self, *_):
        Clock.unschedule(self.schedule)
        super(UpdateMaxHTLC, self).stop()


class UpdateMaxHTLCPlug(Plugin):
    def main(self):
        self.max_htlc = UpdateMaxHTLC(name="M")
        self.max_htlc.daemon = True
        self.max_htlc.start()

    def cleanup(self):
        self.max_htlc.stop()
