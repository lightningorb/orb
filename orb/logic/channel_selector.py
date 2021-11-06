from random import choice

LNBIG = [
    '777338228286160896',
    '772393724494086144',
    '772380530381488129',
    '777338228285833217',
]


def get_low_inbound_channel(lnd, avoid, pk_ignore, chan_ignore, num_sats, ratio=0.5):
    """
    Pick a channel for sending out sats.
    """
    chans = []
    channels = lnd.get_channels(active_only=True)
    for chan in channels:
        if chan.remote_pubkey in pk_ignore:
            continue
        if chan.chan_id in chan_ignore:
            continue
        # get the amount of sats that are locked on our side of the channel
        pending_out = sum(int(p.amount) for p in chan.pending_htlcs if not p.incoming)
        # deduct those from the local balance available
        actual_available_outbound = chan.local_balance - pending_out
        # check whether the amount of sats remaining is enough for the payment
        enough_available_outbound = num_sats < actual_available_outbound

        if chan.chan_id in LNBIG:
            ratio = 0.1

        # check whether the available balance is above a certain ratio, e.g
        # a ratio of 1 would hardly ever pick the channel while a ratio
        # of 0 would always pick the channel
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
