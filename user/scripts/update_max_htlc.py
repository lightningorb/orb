# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-15 07:27:21
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-01-04 14:53:29

from time import sleep
from kivy.clock import Clock
from threading import Thread
from orb.lnd import Lnd


class MaxPolicy:
    half_cap = 0
    local_balance = 1


max_policy = MaxPolicy.local_balance


class UpdateMaxHTLC(Thread):
    def schedule(self):
        Clock.schedule_once(lambda _: Thread(target=self.main).start(), 1)
        Clock.schedule_interval(lambda _: Thread(target=self.main).start(), 10 * 60)

    def main(self, *_):
        for i, c in enumerate(Lnd().get_channels()):
            policy = Lnd().get_policy_to(c.chan_id)
            max_htlc = int(int(policy.max_htlc_msat) / 1_000)
            if max_policy == MaxPolicy.half_cap:
                new_max_htlc = int(c.capacity * 0.5)
            elif max_policy == MaxPolicy.local_balance:
                new_max_htlc = int(c.local_balance)
            needs_update = max_htlc != new_max_htlc
            if needs_update:
                print(
                    f"Updating policy for: {c.chan_id}, max_htlc: {max_htlc}, new_max_htlc: {new_max_htlc}"
                )
                Lnd().update_channel_policy(
                    channel=c,
                    time_lock_delta=int(policy.time_lock_delta),
                    fee_rate=int(policy.fee_rate_milli_msat) / 1e6,
                    base_fee_msat=int(policy.fee_base_msat),
                    max_htlc_msat=int((new_max_htlc * 1_000)),
                )
        print(f"Max HTLC updated")

    def run(self, *_):
        self.schedule()
        while True:
            sleep(5)


def main():
    max_htlc = UpdateMaxHTLC()
    max_htlc.daemon = True
    max_htlc.start()
