# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-17 06:12:06
# @Last Modified by:   lnorb.com
# @Last Modified time: 2021-12-27 04:04:35

"""
Set of classes to set fees via a convenient yaml file.
"""

import os
import yaml
from copy import copy
from time import sleep

import arrow

import data_manager
from kivy.clock import Clock
from threading import Thread
from orb.store import model
from orb.math.lerp import lerp

lnd = data_manager.data_man.lnd


class Base:
    def __str__(self):
        return str(self.__dict__)


class FeeMeta(Base):
    def __init__(
        self,
        last_changed=None,
        chan_id=None,
        alias=None,
        last_routed=None,
        fee_rate=None,
        last_fee_rate=None,
        capacity=None,
        ratio=None,
    ):
        self.last_changed = last_changed
        self.chan_id = chan_id
        self.alias = alias
        self.last_routed = last_routed
        self.fee_rate = fee_rate
        self.last_fee_rate = last_fee_rate
        self.capacity = capacity
        self.ratio = ratio

    def __cmp__(self, other):
        return self.chan_id == other.chan_id


class Match(Base):
    def __init__(self, rule, fee_rate, alias, priority=0):
        self.rule = rule
        self.fee_rate = fee_rate
        self.alias = alias
        self.priority = priority

    def set_meta(self, meta):
        self.meta = meta
        ev = (
            model.FowardEvent()
            .select()
            .order_by(model.FowardEvent.timestamp.desc())
            .where(model.FowardEvent.chan_id_out == str(self.channel.chan_id))
            .first()
        )
        if ev:
            self.meta.last_routed = arrow.get(ev.timestamp).humanize()

    @property
    def routed_in(self):
        return sum(
            [
                x.amt_in
                for x in model.FowardEvent()
                .select()
                .where(model.FowardEvent.chan_id_in == str(self.channel.chan_id))
            ]
        )

    @property
    def routed_out(self):
        return sum(
            [
                x.amt_in
                for x in model.FowardEvent()
                .select()
                .where(model.FowardEvent.chan_id_out == str(self.channel.chan_id))
            ]
        )

    @property
    def max_fee(self):
        return max(
            [
                ((x.fee / x.amt_in) * 1_000_000 if x.fee else 0)
                for x in model.FowardEvent()
                .select()
                .where(model.FowardEvent.chan_id_out == str(self.channel.chan_id))
            ]
            + [0]
        )

    @property
    def policy_to(self):
        return lnd.get_policy_to(self.channel.chan_id)

    def eval(self):
        channel = self.channel
        return eval(self.rule)

    def eval_fee_rate(self):
        channel = self.channel
        return int(eval(str(self.fee_rate)))


class Setter(Base):
    def __init__(self, channel, fee_rate, meta, priority=0):
        self.channel = channel
        self.fee_rate = fee_rate
        self.meta = meta
        self.priority = priority

    def set(self):
        self.meta.capacity = self.channel.capacity
        self.meta.ratio = self.channel.local_balance / self.channel.capacity
        if self.meta.last_changed and arrow.get(
            self.meta.last_changed
        ) > arrow.utcnow().dehumanize("10 minutes ago"):
            return
        policy = lnd.get_policy_to(self.channel.chan_id)
        alias = lnd.get_node_alias(self.channel.remote_pubkey)
        self.meta.fee_rate = self.fee_rate
        current_fee_rate = int(policy.fee_rate_milli_msat)
        if current_fee_rate != self.fee_rate:
            self.meta.last_fee_rate = current_fee_rate
            self.meta.last_changed = int(arrow.utcnow().timestamp())
            print(f"setting fee rate to {self.fee_rate} on {alias}")
            lnd.update_channel_policy(
                channel=self.channel, fee_rate=self.fee_rate / 1e6, time_lock_delta=44
            )


def get_loader():
    loader = yaml.SafeLoader
    loader.add_constructor("!FeeMeta", lambda l, n: FeeMeta(**l.construct_mapping(n)))
    loader.add_constructor("!Match", lambda l, n: Match(**l.construct_mapping(n)))
    return loader


def get_dumper():
    safe_dumper = yaml.SafeDumper
    safe_dumper.add_representer(
        Match,
        lambda dumper, inst: dumper.represent_mapping(
            "!Match",
            {
                "rule": inst.rule,
                "fee_rate": inst.fee_rate,
                "priority": inst.priority,
                "alias": inst.alias,
            },
        ),
    )
    safe_dumper.add_representer(
        FeeMeta,
        lambda dumper, inst: dumper.represent_mapping("!FeeMeta", inst.__dict__),
    )
    return safe_dumper


class Fees(Thread):
    def schedule(self):
        Clock.schedule_once(lambda _: Thread(target=self.main).start(), 1)
        Clock.schedule_interval(lambda _: Thread(target=self.main).start(), 5 * 60)

    def main(self, *_):
        if not os.path.exists("fees.yaml"):
            return
        obj = yaml.load(open("fees.yaml", "r"), Loader=get_loader())
        meta = {x.chan_id: x for x in obj.get("meta", [])}
        chans = lnd.get_channels()
        setters = {}
        for c in chans:
            alias = lnd.get_node_alias(c.remote_pubkey)
            if c.chan_id not in meta:
                meta[c.chan_id] = FeeMeta(chan_id=c.chan_id, alias=alias)
            for rule in obj["rules"]:
                match = copy(rule)
                match.channel = c
                match.set_meta(meta[c.chan_id])
                if match.eval():
                    if c not in setters or match.priority > setters[c].priority:
                        setters[c] = Setter(
                            channel=c,
                            fee_rate=match.eval_fee_rate(),
                            meta=meta[c.chan_id],
                            priority=match.priority,
                        )
        for s in setters:
            setters[s].set()
        print("Writing output")
        obj["meta"] = sorted(
            [*set([*meta.values()])], key=lambda x: (x.ratio or 0), reverse=True
        )
        with open("fees.yaml", "w") as stream:
            stream.write(yaml.dump(obj, Dumper=get_dumper()))

    def run(self, *_):
        self.schedule()
        while True:
            sleep(5)


def main():
    auto_fee = Fees()
    auto_fee.daemon = True
    auto_fee.start()
