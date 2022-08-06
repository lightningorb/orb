# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-15 07:15:28
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-08-06 10:22:38

from functools import lru_cache

from kivy.clock import mainthread
from kivy.app import App

from orb.components.popup_drop_shadow import PopupDropShadow
from orb.logic.rebalance_thread import RebalanceThread
from orb.lnd import Lnd


@lru_cache(maxsize=None)
def alias(lnd, pk):
    return lnd.get_node_alias(pk)


class Rebalance(PopupDropShadow):
    def __init__(self, **kwargs):
        PopupDropShadow.__init__(self, **kwargs)
        self.lnd = Lnd()
        self.chan_id = None
        self.last_hop_pubkey = None
        self.alias_to_pk = {}

        @mainthread
        def delayed(chans_pk, alias_to_pk):
            self.ids.spinner_out_id.values = chans_pk
            self.ids.spinner_in_id.values = alias_to_pk

        app = App.get_running_app()
        channels = app.channels
        self.alias_to_pk = {
            alias(self.lnd, c.remote_pubkey): c.remote_pubkey for c in channels
        }
        chans_pk = [
            f"{c.chan_id}: {alias(self.lnd, c.remote_pubkey)}" for c in channels
        ]
        delayed(chans_pk, self.alias_to_pk)

    def first_hop_spinner_click(self, chan):
        self.chan_id = int(chan.split(":")[0])
        print(f"Setting chan_id to: {self.chan_id}")

    def last_hop_spinner_click(self, alias):
        self.last_hop_pubkey = self.alias_to_pk[alias]
        print(f"Setting last hop pubkey to: {self.last_hop_pubkey}")

    def rebalance(self):
        self.thread = RebalanceThread(
            amount=int(self.ids.amount.text),
            chan_id=self.chan_id,
            last_hop_pubkey=self.last_hop_pubkey,
            fee_rate=int(self.ids.fee_rate.text),
            time_pref=self.ids.time_pref.value,
            max_paths=int(self.ids.max_paths.text),
            name="RebalanceThread",
            thread_n=0,
        )
        self.thread.daemon = True
        self.thread.start()

    def kill(self):
        self.thread.stop()
