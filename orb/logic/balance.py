# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-26 09:55:12
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-08-08 15:21:06

"""
Get the total balance for the node.
"""


def balance(ln):
    remote, local, pending_in, pending_out, commit = 0, 0, 0, 0, 0
    cbal = ln.channel_balance()

    # For each channel (including inactive channels)
    for c in ln.get_channels():
        # Tally the local and remote balances
        local += c.local_balance
        remote += c.remote_balance
        # If we initiated the open, then including the commit fee
        if c.initiator:
            commit += c.commit_fee
        # Tally up the pending in, and pending out sats
        pi = sum(int(p.amount) for p in c.pending_htlcs if p.incoming)
        po = sum(int(p.amount) for p in c.pending_htlcs if not p.incoming)
        # These should match the channel's unsettled balance
        assert c.unsettled_balance == pi + po
        pending_in += pi
        pending_out += po

    # Get all pending channels.
    pending_channels = ln.get_pending_channels()

    limbo = pending_channels.total_limbo_balance

    # Query confirmed and unconfirmed chain balance.
    chain_total = ln.get_balance().total_balance

    # Tally everything up.
    grand_total = local + chain_total + commit + pending_out + limbo

    return grand_total
