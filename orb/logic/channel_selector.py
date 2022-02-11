# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-15 07:15:28
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-01-15 19:39:06

from random import choice
from orb.misc import data_manager


def get_low_inbound_channel(lnd, pk_ignore, chan_ignore, num_sats):
    """
    Pick a channel for sending out sats.
    """
    chans = []
    channels = data_manager.data_man.channels
    for chan in channels:
        if chan.remote_pubkey in pk_ignore:
            continue
        if chan.chan_id in chan_ignore:
            continue
        enough_available_outbound = int(num_sats) < chan.local_balance

        threshold_ratio = float(
            data_manager.data_man.store.get("balanced_ratio", {}).get(
                str(chan.chan_id), "0.5"
            )
        )

        more_than_half_outbound = (
            (chan.local_balance - num_sats) / int(chan.capacity)
        ) > threshold_ratio
        good_candidate = enough_available_outbound and more_than_half_outbound
        if good_candidate:
            chans.append(chan)
    if chans:
        return choice(chans).chan_id


def get_low_outbound_channel(lnd, pk_ignore, chan_ignore, num_sats, ratio=0.5):
    chans = []
    channels = data_manager.data_man.channels
    for chan in channels:
        if chan.remote_pubkey in pk_ignore:
            continue
        if chan.chan_id in chan_ignore:
            continue
        enough_available_inbound = int(num_sats) < chan.local_balance
        threshold_ratio = float(
            data_manager.data_man.store.get("balanced_ratio", {}).get(
                str(chan.chan_id), "0.5"
            )
        )
        more_than_half_inbound = (
            (chan.local_balance - num_sats) / int(chan.capacity)
        ) > threshold_ratio
        good_candidate = enough_available_inbound and more_than_half_inbound
        if good_candidate:
            chans.append(chan)
    if chans:
        chan = choice(chans)
        return chan.chan_id, chan.remote_pubkey
