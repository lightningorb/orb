# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-15 07:15:28
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-02-11 14:03:35

import os
from time import sleep
from threading import Lock, Thread
from copy import copy
from random import shuffle
from pathlib import Path
from functools import cmp_to_key

import yaml

from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
from kivy.properties import NumericProperty
from kivy.uix.boxlayout import BoxLayout

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


def get_dumper():
    safe_dumper = yaml.SafeDumper
    safe_dumper.add_representer(
        Ignore,
        lambda dumper, inst: dumper.represent_mapping(
            "!Ignore",
            {
                "all": inst.all,
                "any": inst.any,
                "alias": inst.alias,
            },
        ),
    )
    safe_dumper.add_representer(
        FromTo,
        lambda dumper, inst: dumper.represent_mapping(
            "!FromTo",
            {
                "fee_rate": inst.fee_rate,
                "num_sats": inst.num_sats,
                "from_all": inst.from_all if hasattr(inst, "from_all") else [],
                "to_all": inst.to_all if hasattr(inst, "to_all") else [],
                "from_any": inst.from_any if hasattr(inst, "from_any") else [],
                "to_any": inst.to_any if hasattr(inst, "to_any") else [],
                "alias": inst.alias,
            },
        ),
    )
    return safe_dumper


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
        super(Rebalance, self).stop()

    def run(self, *_):
        self.ratio = 0.5
        self.lock = Lock()
        self.setters = set([])

        self.schedule()
        while not self.stopped():
            sleep(1)

    def do_rebalancing(self, *args):
        """
        This is the 'heart' of the rebalancer.
        """
        with self.lock:
            path = (pref_path("yaml") / "autobalance.yaml").as_posix()
            if not os.path.exists(path):
                return
            obj = yaml.load(open(path, "r"), Loader=get_loader())
            if not obj:
                return
            num_threads = obj["threads"]
            chans = [*data_manager.data_man.channels.channels.values()]
            pk_ignore = set([])
            setters = {}
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


class ABView(Popup):
    def open(self, *args, **kwargs):
        """
        This gets called when the popup is first opened.
        """
        super(ABView, self).open(*args, **kwargs)
        self.path = (pref_path("yaml") / "autobalance.yaml").as_posix()
        if not os.path.exists(self.path):
            default = """
rules:
- !Ignore
  alias: LOOP
  all:
  - channel.remote_pubkey == '021c97a90a411ff2b10dc2a8e32de2f29d2fa49d41bfbb52bd416e460db0747d0d'
  any: null
- !FromTo
  alias: From high outbound to low outbound
  fee_rate: 500
  from_all:
  - channel.ratio > 0.5
  from_any: []
  num_sats: 100000
  to_all:
  - channel.ratio_include_pending < 0.1
  to_any: []
threads: 10
"""
            with open(self.path, "w") as f:
                f.write(default)
        self.obj = yaml.load(open(self.path, "r"), Loader=get_loader())
        if not self.obj:
            return
        self.populate_rules()

    def add_from_to_rule(self):
        self.obj["rules"].append(
            FromTo(
                "New",
                100,
                num_sats=100_000,
                priority=0,
                from_all=["False"],
                to_all=["False"],
            )
        )
        self.ids.rules.clear_widgets()
        self.populate_rules()
        self.save()

    def add_ignore_rule(self):
        self.obj["rules"].append(
            Ignore(
                alias="New",
                all=["False"],
                any=[],
            )
        )
        self.obj["rules"].sort(key=lambda x: type(x) is not Ignore)
        self.ids.rules.clear_widgets()
        self.populate_rules()
        self.save()

    def populate_rules(self):
        self.ids.rules.clear_widgets()
        mapping = {FromTo: FromToView, Ignore: IgnoreView}
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
        autobalance = Rebalance()
        autobalance.daemon = True
        autobalance.start()


class BaseView(BoxLayout):
    rule = ObjectProperty()
    parent_view = ObjectProperty()
    index = NumericProperty()

    def update_rule(self, attr, value):
        setattr(self.rule, attr, value)
        self.parent_view.save()


class FromToView(BaseView):
    pass


class IgnoreView(BaseView):
    pass


class AutoBalance(Plugin):
    def main(self):
        kv_path = (Path(__file__).parent / "autobalance.kv").as_posix()
        Builder.unload_file(kv_path)
        Builder.load_file(kv_path)
        ABView().open()
