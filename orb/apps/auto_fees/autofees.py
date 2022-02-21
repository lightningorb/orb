# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-17 06:12:06
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-02-21 05:44:20

"""
Set of classes to set fees via a convenient yaml file.
"""

import os
import yaml
from copy import copy
from time import sleep
from pathlib import Path

import arrow

from kivy.clock import Clock
from threading import Thread
from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.properties import NumericProperty
from kivy.lang import Builder

from orb.store import model
from orb.math.lerp import lerp
from orb.misc.plugin import Plugin
from orb.logic.normalized_events import get_best_fee
from orb.core.stoppable_thread import StoppableThread
from orb.misc.utils import pref_path
from orb.lnd import Lnd
from orb.misc import data_manager

version = "0.0.4"
yaml_name = f"autofees_v{version}.yaml"
meta_yaml_name = f"autofees_meta_v{version}.yaml"


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
    def __init__(self, fee_rate, alias, all=None, any=None, priority=0):
        self.all = all
        self.any = any
        self.fee_rate = fee_rate
        self.alias = alias
        self.priority = priority

    def set_meta(self, meta):
        self.meta = meta
        ev = (
            model.ForwardEvent()
            .select()
            .order_by(model.ForwardEvent.timestamp.desc())
            .where(model.ForwardEvent.chan_id_out == str(self.channel.chan_id))
        )
        try:
            if ev:
                ev = ev.first()
        except:
            ev = None
        if ev:
            self.meta.last_routed = arrow.get(ev.timestamp).humanize()

    @property
    def routed_in(self):
        return sum(
            [
                x.amt_in
                for x in model.ForwardEvent()
                .select()
                .where(model.ForwardEvent.chan_id_in == str(self.channel.chan_id))
            ]
        )

    @property
    def routed_out(self):
        return sum(
            [
                x.amt_in
                for x in model.ForwardEvent()
                .select()
                .where(model.ForwardEvent.chan_id_out == str(self.channel.chan_id))
            ]
        )

    @property
    def max_fee(self):
        return max(
            [
                ((x.fee / x.amt_in) * 1_000_000 if x.fee else 0)
                for x in model.ForwardEvent()
                .select()
                .where(model.ForwardEvent.chan_id_out == str(self.channel.chan_id))
            ]
            + [0]
        )

    @property
    def min_fee(self):
        found_min = [
            ((x.fee / x.amt_in) * 1_000_000 if x.fee else 0)
            for x in model.ForwardEvent()
            .select()
            .where(model.ForwardEvent.chan_id_out == str(self.channel.chan_id))
        ]
        return min(found_min) if found_min else 0

    @property
    def best_fee(self):
        """
        Calculate the optimal routing fee based on history,
        and current channel liquidity.
        """
        most_frequent = get_best_fee(self.channel, include_zero=False) or 100
        ratio = self.channel.local_balance_include_pending / self.channel.capacity
        global_ratio = data_manager.data_man.channels.global_ratio
        if ratio < global_ratio:
            best = lerp(0, 100, min(ratio / global_ratio, 1))
        else:
            best = lerp(
                most_frequent,
                most_frequent + 10,
                (ratio - global_ratio) / (1 - global_ratio),
            )
        return max(best, 100)

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

    def eval_fee_rate(self):
        channel = self.channel
        best_fee = self.best_fee
        return int(eval(str(self.fee_rate)))


class Setter(Base):
    def __init__(self, channel, fee_rate, meta, obj, priority):
        self.channel = channel
        self.obj = obj
        self.fee_rate = fee_rate
        self.meta = meta
        self.priority = priority

    def set(self):
        self.meta.capacity = self.channel.capacity
        self.meta.ratio = self.channel.local_balance / self.channel.capacity
        if (
            self.obj["spam_prevention"] != 0
            and self.meta.last_changed
            and arrow.get(self.meta.last_changed)
            > arrow.utcnow().shift(minutes=-eval(self.obj["spam_prevention"]))
        ):
            print(f"{self.channel.alias}: last updated updated recently, ignoring")
            return
        alias = Lnd().get_node_alias(self.channel.remote_pubkey)
        self.meta.fee_rate = self.fee_rate
        current_fee_rate = int(self.channel.fee_rate_milli_msat)
        print(
            f"current fee rate: {current_fee_rate}, desired fee rate: {self.fee_rate}"
        )
        if current_fee_rate != self.fee_rate:
            self.meta.last_fee_rate = current_fee_rate
            self.meta.last_changed = int(arrow.utcnow().timestamp())
            if self.fee_rate < current_fee_rate:
                drop_rate_fee = current_fee_rate * (1 - self.obj["fee_drop_factor"])
                new_fee = max(drop_rate_fee, self.fee_rate)
            else:
                new_fee = min(
                    current_fee_rate + self.fee_rate * (self.obj["fee_bump_factor"]),
                    self.fee_rate,
                )
            print(f"setting fee rate to {new_fee} on {alias}")
            self.channel.fee_rate_milli_msat = new_fee
            self.channel.update_lnd_with_policies()


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
                "all": inst.all,
                "any": inst.any,
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


class FeesAuto(StoppableThread):
    def __init__(self, obj):
        self.obj = obj
        super(FeesAuto, self).__init__()

    def stop(self):
        Clock.unschedule(self.schedule)
        super(FeesAuto, self).stop()

    def schedule(self):
        Clock.schedule_once(lambda _: Thread(target=self.main).start(), 1)
        self.schedule = Clock.schedule_interval(
            lambda _: Thread(target=self.main).start(), eval(self.obj["frequency"])
        )

    def main(self, *_):
        def load(fn):
            path = (pref_path("yaml") / fn).as_posix()
            print(path)
            if os.path.exists(path):
                return yaml.load(open(path, "r"), Loader=get_loader())
            return {}

        obj_meta = load(meta_yaml_name)
        meta = {x.chan_id: x for x in obj_meta.get("meta", [])}
        chans = data_manager.data_man.channels
        setters = {}
        for c in chans:
            print(f"analyzing channel: {c.chan_id}")
            if c.chan_id not in meta:
                meta[c.chan_id] = FeeMeta(chan_id=c.chan_id, alias=c.alias)
            for rule in self.obj.get("rules", []):
                match = copy(rule)
                match.channel = c
                match.set_meta(meta[c.chan_id])
                if match.eval():
                    if c not in setters or match.priority > setters[c].priority:
                        setters[c] = Setter(
                            channel=c,
                            fee_rate=match.eval_fee_rate(),
                            meta=meta[c.chan_id],
                            obj=self.obj,
                            priority=match.priority,
                        )
        for s in setters:
            se = setters[s]
            print(f"Attempting to set: {se.fee_rate} on {se.channel.chan_id}")
            se.set()
        obj_meta["meta"] = sorted(
            [*set([*meta.values()])], key=lambda x: (x.ratio or 0), reverse=True
        )
        app = App.get_running_app()
        if app:
            path = (pref_path("yaml") / "fees_meta.yaml").as_posix()
            with open(path, "w") as stream:
                stream.write(yaml.dump(obj_meta, Dumper=get_dumper()))

    def run(self, *_):
        self.schedule()
        while True:
            sleep(5)


class AFView(Popup):
    def __init__(self, *args, **kwargs):
        self.path = (pref_path("yaml") / yaml_name).as_posix()
        if not os.path.exists(self.path):
            default = """
default_fee: 100
fee_bump_factor: 1
fee_drop_factor: 0.1
frequency: 300
rules:
- !Match
  alias: Low Outbound
  all:
  - channel.local_balance < 500_000 or channel.ratio < 0.1
  any: null
  fee_rate: '1000'
  priority: 2
- !Match
  alias: Low Inbound
  all:
  - channel.ratio_include_pending > 0.9
  any: null
  fee_rate: '0'
  priority: 0
- !Match
  alias: Best Fee
  all:
  - (channel.local_balance > 500_000 or channel.ratio > 0.1) and channel.ratio_include_pending
    <= 0.9
  any: null
  fee_rate: self.best_fee
  priority: 1
- !Match
  alias: LOOP
  all:
  - channel.alias == 'LOOP'
  any: null
  fee_rate: '1000'
  priority: 5
spam_prevention: 300
"""
            with open(self.path, "w") as f:
                f.write(default)
        self.obj = yaml.load(open(self.path, "r"), Loader=get_loader())
        if not self.obj:
            return
        super(AFView, self).__init__(*args, **kwargs)

    def open(self, *args, **kwargs):
        """
        This gets called when the popup is first opened.
        """
        super(AFView, self).open(*args, **kwargs)
        self.populate_rules()

    def add_match_rule(self):
        self.obj["rules"].append(
            Match(
                alias="New",
                priority=0,
                all=["False"],
                fee_rate="best_fee",
            )
        )
        self.ids.rules.clear_widgets()
        self.populate_rules()
        self.save()

    def populate_rules(self):
        self.ids.rules.clear_widgets()
        mapping = {Match: MatchView}
        for index, rule in enumerate(self.obj["rules"]):
            view = mapping[type(rule)](rule=rule, parent_view=self, index=index)
            self.ids.rules.add_widget(view)

    def delete_rule(self, index):
        self.obj["rules"] = self.obj["rules"][:index] + self.obj["rules"][index + 1 :]
        self.save()
        self.populate_rules()

    def update_obj(self, attr, value):
        self.obj[attr] = value
        self.save()

    def save(self, *_):
        with open(self.path, "w") as stream:
            stream.write(yaml.dump(self.obj, Dumper=get_dumper()))

    def start(self):
        autofees = FeesAuto(self.obj)
        autofees.daemon = True
        autofees.start()


class BaseView(BoxLayout):
    rule = ObjectProperty()
    parent_view = ObjectProperty()
    index = NumericProperty()

    def update_rule(self, attr, value):
        setattr(self.rule, attr, value)
        self.parent_view.save()


class MatchView(BaseView):
    pass


class AutoFeesPlugin(Plugin):
    def main(self):
        kv_path = (Path(__file__).parent / "autofees.kv").as_posix()
        Builder.unload_file(kv_path)
        Builder.load_file(kv_path)
        AFView().open()
