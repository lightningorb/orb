# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-24 07:44:57
# @Last Modified by:   lnorb.com
# @Last Modified time: 2021-12-31 05:52:22
"""
Get the total balance for the node.
"""

from orb.lnd import Lnd


def main():
    remote, local, pending_in, pending_out, commit = 0, 0, 0, 0, 0

    # For each channel (including inactive channels)
    for c in Lnd().get_channels():
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
    local += pending_out
    remote += pending_in
    print(f"Global Ratio: {local / (local + remote)}")
