# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-26 09:55:12
# @Last Modified by:   lnorb.com
# @Last Modified time: 2021-12-26 10:11:58
"""
Get the total balance for the node.
"""

from kivy.uix.popup import Popup
from kivy.uix.label import Label
from data_manager import data_man


def main():
    lnd = data_man.lnd
    remote, local, pending_in, pending_out, commit = 0, 0, 0, 0, 0

    # For each channel (including inactive channels)
    for c in lnd.get_channels():
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
    pending_channels = lnd.get_pending_channels()
    print(pending_channels)

    # Tally the liquidity trapped in pending open channels.
    pending_open = sum(
        channel.channel.local_balance
        for channel in pending_channels.pending_open_channels
    )

    # Tally the liquidity trapped in pending force close channels.
    pending_close = sum(
        channel.limbo_balance
        for channel in pending_channels.pending_force_closing_channels
    )

    # Query confirmed and unconfirmed chain balance.
    chain_total = lnd.get_balance().total_balance

    # Tally everything up.
    grand_total = (
        local
        + chain_total
        + commit
        + pending_in
        + pending_out
        + pending_open
        + pending_close
    )

    popup = Popup(
        title="Balance",
        content=Label(text=f"{grand_total:_}"),
        size_hint=(None, None),
        size=(300, 300),
    )
    popup.open()
