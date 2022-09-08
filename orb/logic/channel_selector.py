# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-15 07:15:28
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-09-08 12:15:09

from time import time
from random import choice, seed
from orb.app import App


def get_low_inbound_channel(pk_ignore, chan_ignore, num_sats):
    """
    Pick a channel for sending out sats.
    """
    seed(time())
    chans = []
    app = App.get_running_app()
    channels = app.channels
    for chan in channels:
        if chan.remote_pubkey in pk_ignore:
            continue
        if chan.chan_id in chan_ignore:
            continue
        enough_available_outbound = int(num_sats) < chan.local_balance

        ratio = (
            (chan.local_balance - num_sats) / int(chan.capacity)
        )

        more_than_half_outbound = ratio - 0.1 > chan.balanced_ratio
        good_candidate = enough_available_outbound and more_than_half_outbound
        if good_candidate:
            chans.append(chan)
    if chans:
        return choice(chans).chan_id


def get_low_outbound_channel(pk_ignore, chan_ignore, num_sats, ratio=0.5):
    seed(time())
    chans = []
    app = App.get_running_app()
    channels = app.channels
    for chan in channels:
        if chan.remote_pubkey in pk_ignore:
            continue
        if chan.chan_id in chan_ignore:
            continue
        enough_available_inbound = int(num_sats) < chan.local_balance
        low_outbound = (
            (chan.local_balance - num_sats) / int(chan.capacity)
        ) + 0.1 < chan.balanced_ratio
        good_candidate = enough_available_inbound and low_outbound
        if good_candidate:
            chans.append(chan)
    if chans:
        chan = choice(chans)
        return chan.chan_id, chan.remote_pubkey
