# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-08-23 04:36:36
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-08-23 08:25:40

from invoke import task
from .chalk import chalk
from orb.ln import factory
from orb.cli.utils import get_default_id
from orb.app import App


@task(
    help=dict(
        pubkey="The Pubkey to use as the default pubkey for all Orb commands.",
        peer_pubkey="The Pubkey of the peer you wish to open to",
        amount_sats="The size of the channel in sats",
        sat_per_vbyte="The fee to use in sats per vbytes",
    )
)
def open(
    c,
    peer_pubkey: str,
    amount_sats: int,
    sat_per_vbyte: int,
    pubkey: str = "",
):
    """
    Open a channel.
    """
    if not pubkey:
        pubkey = get_default_id()

    ln = factory(pubkey)
    try:
        res = ln.open_channel(
            node_pubkey_string=peer_pubkey,
            sat_per_vbyte=float(sat_per_vbyte),
            amount_sat=int(amount_sats),
        )
        print(res)
    except Exception as e:
        print(f"Exception: {e}")
