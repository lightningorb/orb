# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-15 07:15:28
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-01-05 17:16:42

from random import choice
import data_manager


def get_low_inbound_channel(lnd, pk_ignore, chan_ignore, num_sats):
    """
    Pick a channel for sending out sats.
    """
    chans = []
    # TODO: switch this to data_manager.data_man.channels
    # but make sure they can be filtered for active channels only
    channels = lnd.get_channels(active_only=True)
    for chan in channels:
        if chan.remote_pubkey in pk_ignore:
            continue
        if chan.chan_id in chan_ignore:
            continue
        # get the amount of sats that are locked on our side of the channel
        pending_out = sum(int(p.amount) for p in chan.pending_htlcs if not p.incoming)
        # add those from the local balance available, to get the correct reading
        # of the local balance
        actual_available_outbound = int(chan.local_balance) + pending_out
        # check whether the amount of sats remaining is enough for the payment
        enough_available_outbound = int(num_sats) < actual_available_outbound

        threshold_ratio = float(
            data_manager.data_man.store.get("balanced_ratio", {}).get(
                str(chan.chan_id), "0.5"
            )
        )

        # check whether the available balance is above a certain ratio, e.g
        # a ratio of 1 would hardly ever pick the channel while a ratio
        # of 0 would always pick the channel
        more_than_half_outbound = (
            (actual_available_outbound - num_sats) / int(chan.capacity)
        ) > threshold_ratio
        good_candidate = enough_available_outbound and more_than_half_outbound
        if good_candidate:
            chans.append(chan)
    if chans:
        return choice(chans).chan_id


def get_low_outbound_channel(lnd, pk_ignore, chan_ignore, num_sats, ratio=0.5):
    chans = []
    # TODO: switch this to data_manager.data_man.channels
    # but make sure they can be filtered for active channels only
    channels = lnd.get_channels(active_only=True)
    for chan in channels:
        if chan.remote_pubkey in pk_ignore:
            continue
        if chan.chan_id in chan_ignore:
            continue
        pending_in = sum(int(p.amount) for p in chan.pending_htlcs if p.incoming)
        actual_available_inbound = int(chan.remote_balance) + pending_in
        enough_available_inbound = int(num_sats) < actual_available_inbound
        threshold_ratio = float(
            data_manager.data_man.store.get("balanced_ratio", {}).get(
                str(chan.chan_id), "0.5"
            )
        )
        more_than_half_inbound = (
            (actual_available_inbound - num_sats) / int(chan.capacity)
        ) > threshold_ratio
        good_candidate = enough_available_inbound and more_than_half_inbound
        if good_candidate:
            chans.append(chan)
    if chans:
        chan = choice(chans)
        return chan.chan_id, chan.remote_pubkey
