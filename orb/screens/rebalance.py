# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-15 07:15:28
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-01-08 07:28:18

from traceback import print_exc
import threading
from functools import lru_cache

from kivy.clock import mainthread

from orb.components.popup_drop_shadow import PopupDropShadow
from orb.logic.rebalance_thread import RebalanceThread
from orb.lnd import Lnd
import data_manager


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
        def delayed(chans_pk):
            self.ids.spinner_out_id.values = chans_pk
            self.ids.spinner_in_id.values = chans_pk

        channels = data_manager.data_man.channels
        self.alias_to_pk = {
            alias(self.lnd, c.remote_pubkey): c.remote_pubkey for c in channels
        }
        chans_pk = [
            f"{c.chan_id}: {alias(self.lnd, c.remote_pubkey)}" for c in channels
        ]
        delayed(chans_pk)

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
            max_paths=int(self.ids.max_paths.text),
            name="RebalanceThread",
            thread_n=0,
        )
        self.thread.daemon = True
        self.thread.start()

    def kill(self):
        self.thread.stop()
