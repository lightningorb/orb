# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-26 09:55:12
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-08-07 12:31:15

"""
Get the total balance for the node.
"""

from kivy.uix.popup import Popup
from kivy.uix.label import Label

from orb.ln import Ln
from orb.misc.plugin import Plugin


class Balance(Plugin):
    def main(self):
        ln = Ln()
        if ln.node_type != "lnd":
            print("This app currently only works for LND")
            return
        remote, local, pending_in, pending_out, commit = 0, 0, 0, 0, 0

        cbal = Ln().local_remote_bal()

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
        print(pending_channels)

        limbo = pending_channels.total_limbo_balance

        # Query confirmed and unconfirmed chain balance.
        chain_total = ln.get_balance().total_balance

        # Tally everything up.
        grand_total = local + chain_total + commit + pending_out + limbo

        tot = f"{grand_total:_}"
        print(tot)

        popup = Popup(
            title="Balance",
            content=Label(text=tot),
            size_hint=(None, None),
            size=(300, 300),
        )
        popup.open()
