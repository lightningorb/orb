# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-15 07:15:28
# @Last Modified by:   lnorb.com
# @Last Modified time: 2021-12-29 05:32:00

import os
import math
from time import sleep
from threading import Lock, Thread
from copy import copy

import yaml

from kivy.clock import Clock

from orb.misc.utils import pref
from orb.logic.pay_logic import pay_thread, PaymentStatus
from orb.logic.channel_selector import *
from orb.logic.rebalance_thread import RebalanceThread
import data_manager

chan_ignore = set([])

"""

FIRST PHASE:

The first phase is reading the YAML file, this gives us rules that ultimately end up
in a set of 'to's and 'from's

From:            To:
  None            Chan_1
  None            Chan_2
  None            Chan_3

SECOND PHASE:

The second phase involves turning these "loose" requests into concrete requests,
i.e if no channel is selected in the 'From' column then it needs to be selected.

From:            To:
  Chan_a           Chan_1
  Chan_b           Chan_2
  Chan_c           Chan_3

THIRD PHASE:

The third phase involves actually carrying out those rebalances. It's important
for there to be at least 3 rebalances being carried out at all times.


"""


class EvalMixin:
    def eval(self):
        channel = self.channel
        if self.all:
            for a in self.all:
                if not eval(a):
                    return False
            return True
        if self.any:
            for a in self.any:
                if eval(a):
                    return True
            return False
        return False


class Ignore(EvalMixin):
    def __init__(self, alias, all=None, any=None):
        self.all = all
        self.any = any
        self.alias = alias


class To(EvalMixin):
    def __init__(
        self, alias, fee_rate, num_sats=100_000, priority=0, all=None, any=None
    ):
        self.all = all
        self.any = any
        self.alias = alias
        self.fee_rate = fee_rate
        self.num_sats = num_sats
        self.priority = priority


def get_loader():
    loader = yaml.SafeLoader
    loader.add_constructor("!Ignore", lambda l, n: Ignore(**l.construct_mapping(n)))
    loader.add_constructor("!To", lambda l, n: To(**l.construct_mapping(n)))
    return loader


class Setter:
    def __init__(self, _from, _to, fee_rate, num_sats, pk_ignore, priority=0):
        self._from = _from
        self._to = _to
        self.fee_rate = fee_rate
        self.priority = priority
        self.num_sats = num_sats
        self.pk_ignore = pk_ignore

    def set(self):
        outbound_channel = get_low_inbound_channel(
            lnd=data_manager.data_man.lnd,
            pk_ignore=self.pk_ignore,
            chan_ignore=chan_ignore,
            num_sats=self.num_sats,
        )
        t = RebalanceThread(
            amount=self.num_sats,
            fee_rate=self.fee_rate,
            chan_id=outbound_channel,
            last_hop_pubkey=self._to.remote_pubkey,
            max_paths=1000,
            name="AR",
            thread_n=0,
        )

        return t


class Autobalance(Thread):
    def schedule(self):
        Clock.schedule_interval(
            lambda _: Thread(target=self.do_rebalancing).start(), 15
        )

    def run(self, *_):
        import data_manager

        self.ratio = 0.5
        self.lock = Lock()
        self.threads = set([])

        self.schedule()
        while True:
            sleep(5)

    def do_rebalancing(self, *args):
        if self.lock.locked():
            return
        self.lock.acquire()
        from data_manager import data_man

        lnd = data_man.lnd
        if not os.path.exists("autobalance.yaml"):
            return
        obj = yaml.load(open("autobalance.yaml", "r"), Loader=get_loader())
        chans = lnd.get_channels()
        pk_ignore = set([])
        setters = {}

        for c in chans:
            if c.chan_id in pk_ignore:
                continue
            alias = lnd.get_node_alias(c.remote_pubkey)
            for rule in obj["rules"]:
                rule_copy = copy(rule)
                rule_copy.channel = c
                if type(rule) is Ignore:
                    if rule_copy.eval():
                        pk_ignore.add(rule_copy.channel.remote_pubkey)
                elif type(rule) is To:
                    key = (None, c.chan_id)
                    if key not in setters and rule_copy.eval():
                        setters[key] = Setter(
                            _from=None,
                            _to=rule_copy.channel,
                            pk_ignore=pk_ignore,
                            fee_rate=rule_copy.fee_rate,
                            num_sats=rule_copy.num_sats,
                            priority=rule_copy.priority,
                        )

        threads = [s.set() for s in setters.values()]

        for t in threads:
            t.start()

        for t in threads:
            t.join()

        print("Autorebalance - done")
        self.lock.release()


def main():
    autobalance = Autobalance()
    autobalance.daemon = True
    autobalance.start()
