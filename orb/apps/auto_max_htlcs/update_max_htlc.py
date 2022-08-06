# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-07-22 05:36:17
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-08-06 08:22:33

from time import sleep
from threading import Thread

from orb.core.stoppable_thread import StoppableThread
from orb.misc.plugin import Plugin

from orb.lnd import Lnd
from orb.misc.utils import pref_path

from kivy.properties import ObjectProperty
from kivy.event import EventDispatcher
from kivy.config import ConfigParser
from kivy.uix.popup import Popup
from kivy.utils import platform
from kivy.clock import Clock


class UpdateMaxHTLC(StoppableThread, EventDispatcher):
    config = ObjectProperty()

    def __init__(self, config):
        self.config = config
        super(UpdateMaxHTLC, self).__init__()

    def main(self, *_):
        app = App.get_running_app()
        for i, c in enumerate(app.channels.channels.values()):
            round = lambda x: int(int(x / 10_000) * 10_000)
            max_htlc = round(int(int(c.max_htlc_msat) / 1_000))
            if self.config["config"]["policy"] == "Half Capacity":
                new_max_htlc = round(int(c.capacity * 0.5))
            elif self.config["config"]["policy"] == "Local Balance":
                new_max_htlc = round(int(c.local_balance))
            elif self.config["config"]["policy"] == "Balanced Ratio":
                new_max_htlc = round(int(c.balanced_ratio * c.capacity))
            if self.config["config"]["disable_depleted"] == "True":
                if c.ratio_include_pending < float(
                    self.config["config"]["depletion_ratio"]
                ):
                    new_max_htlc = 1
            new_max_htlc = max(int(new_max_htlc), 0)
            needs_update = max_htlc != new_max_htlc
            if needs_update:
                print(
                    f"Updating policy for: {c.chan_id}, max_htlc: {max_htlc}, new_max_htlc: {new_max_htlc}"
                )
                c.min_htlc_msat = 0
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
        if hasattr(self, "schedule"):
            Clock.unschedule(self.schedule)
        super(UpdateMaxHTLC, self).stop()


class UpdateMaxHTLCView(Popup):
    config = ObjectProperty()

    def __init__(self, config):
        self.config = config
        super(UpdateMaxHTLCView, self).__init__()

    def start(self):
        self.max_htlc = UpdateMaxHTLC(config=self.config)
        self.max_htlc.daemon = True
        self.config.write()
        self.max_htlc.start()

    def stop(self):
        if hasattr(self, "max_htlc"):
            self.max_htlc.stop()


class UpdateMaxHTLCPlug(Plugin):
    def main(self):
        # kv_path = (Path(__file__).parent / "update_max_htlc.kv").as_posix()
        # Builder.unload_file(kv_path)
        # Builder.load_file(kv_path)
        path = pref_path("yaml") / "update_max_htlc_msat.conf"
        config = ConfigParser()
        config.filename = path.as_posix()
        if not path.exists():
            config.adddefaultsection("config")
            config.setdefaults(
                "config",
                dict(
                    policy="Balanced Ratio",
                    disable_depleted=True,
                    depletion_ratio="0.2",
                ),
            )
            config.write()
        else:
            config.read(path.as_posix())

        self.view = UpdateMaxHTLCView(config)
        self.view.open()

    def cleanup(self):
        self.view.stop()
