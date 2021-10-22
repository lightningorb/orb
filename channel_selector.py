from random import choice

def get_low_inbound_channel(lnd, avoid, pk_ignore, chan_ignore, num_sats):
    chans = []
    channels = lnd.get_channels(active_only=True)
    for chan in channels:
        if chan.remote_pubkey in pk_ignore:
            continue
        if chan.chan_id in chan_ignore:
            continue
        pending_out = sum(
            int(p.amount) for p in chan.pending_htlcs if not p.incoming
        )
        actual_available_outbound = chan.local_balance - pending_out
        enough_available_outbound = (num_sats < actual_available_outbound)
        more_than_half_outbound = (actual_available_outbound / chan.capacity) > 0.5
        good_candidate = enough_available_outbound and more_than_half_outbound
        if good_candidate:
            if chan.chan_id in [*avoid.keys()]:
                avoid[chan.chan_id] += 1
                if avoid[chan.chan_id] > 15:
                    del avoid[chan.chan_id]
                else:
                    continue
            chans.append(chan)
    if chans:
        return choice(chans).chan_id
