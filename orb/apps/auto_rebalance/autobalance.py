# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-15 07:15:28
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-02-09 07:48:57

import os
from time import sleep
from threading import Lock, Thread
from copy import copy
from random import shuffle

import yaml

from kivy.clock import Clock

from orb.misc.utils import pref_path
from orb.core.stoppable_thread import StoppableThread
from orb.logic.rebalance_thread import RebalanceThread
from orb.misc.plugin import Plugin
from orb.misc import data_manager

chan_ignore = set([])


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

    def __str__(self):
        return """
        channel: {}
        all: {}
        any: {}
        """.format(
            self.channel.chan_id if hasattr(self, "channel") else None,
            "\n".join(x for x in self.all or []),
            "\n".join(x for x in self.any or []),
        )


class Ignore(EvalMixin):
    def __init__(self, alias, all=None, any=None):
        self.all = all
        self.any = any
        self.alias = alias


class From(EvalMixin):
    def __init__(self, all=None, any=None):
        self.all = all
        self.any = any


class To(EvalMixin):
    def __init__(self, all=None, any=None):
        self.all = all
        self.any = any


class FromTo:
    def __init__(
        self,
        alias,
        fee_rate,
        num_sats=100_000,
        priority=0,
        from_all=[],
        from_any=[],
        to_all=[],
        to_any=[],
    ):
        self.from_all = from_all
        self.to_all = to_all
        self._from = From(all=from_all, any=from_any)
        self._to = To(all=to_all, any=to_any)
        self.alias = alias
        self.fee_rate = fee_rate
        self.num_sats = num_sats
        self.priority = priority

    def eval(self):
        self._from.channel
        self._to.channel
        return self._from.eval() and self._from.eval()

    def __str__(self):
        return f"{self._from} {self._to}"


def get_loader():
    loader = yaml.SafeLoader
    loader.add_constructor(
        "!Ignore", lambda l, n: Ignore(**l.construct_mapping(n, deep=True))
    )
    loader.add_constructor(
        "!FromTo", lambda l, n: FromTo(**l.construct_mapping(n, deep=True))
    )
    return loader


class RuleBase:
    def __init__(self, fee_rate, priority, num_sats):
        self.fee_rate = fee_rate
        self.priority = priority
        self.num_sats = num_sats


class Setter(RuleBase):
    def __init__(self, _from, _to, fee_rate, num_sats, pk_ignore, priority=0):
        super(Setter, self).__init__(fee_rate, priority, num_sats)
        self._from = _from
        self._to = _to
        self.pk_ignore = pk_ignore
        self.thread = None

    def set(self):
        self.thread = RebalanceThread(
            amount=self.num_sats,
            fee_rate=self.fee_rate,
            chan_id=self._from.chan_id,
            last_hop_pubkey=self._to.remote_pubkey,
            max_paths=1000,
            name="AR",
            thread_n=0,
        )
        return self

    def __eq__(self, other):
        return (
            self._from.chan_id if self._from else None,
            self._to.chan_id if self._to else None,
        ) == (
            other._from.chan_id if other._from else None,
            other._to.chan_id if other._to else None,
        )

    def __hash__(self):
        return hash(
            str(
                (
                    self._from.chan_id if self._from else None,
                    self._to.chan_id if self._to else None,
                )
            )
        )


class Rebalance(StoppableThread):
    def schedule(self):
        Clock.schedule_once(lambda _: Thread(target=self.do_rebalancing).start(), 0)
        self.schedule = Clock.schedule_interval(
            lambda _: Thread(target=self.do_rebalancing).start(), 30
        )

    def stop(self):
        Clock.unschedule(self.schedule)

    def run(self, *_):
        self.ratio = 0.5
        self.lock = Lock()
        self.setters = set([])

        self.schedule()
        while True:
            sleep(5)

    def do_rebalancing(self, *args):
        """
        This is the 'heart' of the rebalancer.
        """
        # make sure we're only running of these at a time (why the lock?)
        with self.lock:
            # path to the user yaml file
            path = (pref_path("yaml") / "autobalance.yaml").as_posix()
            # return if it doesn't exist
            if not os.path.exists(path):
                return
            # load it
            obj = yaml.load(open(path, "r"), Loader=get_loader())
            # bail if it's empty
            if not obj:
                return

            num_threads = obj["threads"]

            # get our channels
            chans = [*data_manager.data_man.channels.channels.values()]

            # these are the pubkeys the user explicitely wants
            # to ignore
            pk_ignore = set([])

            # the 'setters' to the actual rebalancing work
            # our job now is to populate 'setters'
            setters = {}

            # for each of our channels
            for from_channel in chans:
                if from_channel.chan_id in pk_ignore:
                    continue
                for to_channel in chans:
                    if from_channel.chan_id == to_channel.chan_id:
                        continue
                    if to_channel.chan_id in pk_ignore:
                        continue
                    for rule in obj.get("rules", []):
                        rule_copy = copy(rule)
                        if type(rule) is Ignore:
                            for chan in [from_channel, to_channel]:
                                rule_copy.channel = chan
                                if rule_copy.eval():
                                    pk_ignore.add(rule_copy.channel.remote_pubkey)
                        elif type(rule) is FromTo:
                            _from = From(
                                all=rule_copy.from_all
                                if hasattr(rule_copy, "from_all")
                                else None,
                                any=rule_copy.from_any
                                if hasattr(rule_copy, "from_any")
                                else None,
                            )
                            _from.channel = from_channel
                            _to = To(
                                all=rule_copy.to_all
                                if hasattr(rule_copy, "to_all")
                                else None,
                                any=rule_copy.to_any
                                if hasattr(rule_copy, "to_any")
                                else None,
                            )
                            _to.channel = to_channel
                            if _from.eval() and _to.eval():
                                key = (from_channel.chan_id, to_channel.chan_id)
                                setters[key] = Setter(
                                    _from=from_channel,
                                    _to=to_channel,
                                    pk_ignore=pk_ignore,
                                    fee_rate=rule_copy.fee_rate,
                                    num_sats=rule_copy.num_sats,
                                    priority=rule_copy.priority,
                                )


            setters = [*setters.values()]
            shuffle(setters)

            for s in set([s for s in self.setters if s.thread.stopped()]):
                self.setters.remove(s)

            for setter in setters:
                if setter not in self.setters and len(self.setters) < num_threads:
                    self.setters.add(setter.set())
                    setter.thread.start()

            print("Autorebalance - done")


class AutoBalance(Plugin):
    def main(self):
        autobalance = Rebalance()
        autobalance.daemon = True
        autobalance.start()
