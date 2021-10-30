from random import choice


def get_low_inbound_channel(lnd, avoid, pk_ignore, chan_ignore, num_sats, ratio=0.5):
    chans = []
    channels = lnd.get_channels(active_only=True)
    for chan in channels:
        if chan.remote_pubkey in pk_ignore:
            continue
        if chan.chan_id in chan_ignore:
            continue
        pending_out = sum(int(p.amount) for p in chan.pending_htlcs if not p.incoming)
        actual_available_outbound = chan.local_balance - pending_out
        enough_available_outbound = num_sats < actual_available_outbound
        more_than_half_outbound = (actual_available_outbound / chan.capacity) > ratio
        good_candidate = enough_available_outbound and more_than_half_outbound
        if good_candidate:
            chans.append(chan)
    if chans:
        return choice(chans).chan_id


def get_low_outbound_channel(lnd, avoid, pk_ignore, chan_ignore, num_sats, ratio=0.5):
    chans = []
    channels = lnd.get_channels(active_only=True)
    for chan in channels:
        if chan.remote_pubkey in pk_ignore:
            continue
        if chan.chan_id in chan_ignore:
            continue
        pending_in = sum(int(p.amount) for p in chan.pending_htlcs if p.incoming)
        actual_available_inbound = chan.remote_balance - pending_in
        enough_available_inbound = num_sats < actual_available_inbound
        more_than_half_inbound = (actual_available_inbound / chan.capacity) > ratio
        good_candidate = enough_available_inbound and more_than_half_inbound
        if good_candidate:
            chans.append(chan)
    if chans:
        chan = choice(chans)
        return chan.chan_id, chan.remote_pubkey
