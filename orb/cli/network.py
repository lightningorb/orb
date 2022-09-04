# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-08-10 06:37:37
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-09-04 15:50:42

from typing import Optional
from invoke import task

from orb.cli.utils import get_default_id
from orb.ln import factory
from orb.app import App

import typer

app = typer.Typer()


@app.command()
def get_route(
    fee_limit_msat: str = typer.Option(
        500, help="the fee limit in millisatoshis. This is ignored by CLN."
    ),
    destination: str = typer.Option(
        ..., help="the pub_key of the node to which to find a route."
    ),
    source_pub_key: str = typer.Option(
        None, help="the pub_key of the node from which to find a route."
    ),
    outgoing_chan_id: str = typer.Option(
        ..., help="the channel id the first hop o the route."
    ),
    ignored_nodes: str = typer.Option([], help="list of nodes to ignore."),
    ignored_pairs: str = typer.Option([], help="list of pairs to ignore (LND only)."),
    last_hop_pubkey: str = typer.Option(
        [], help="the last node before pub_key (LND only)."
    ),
    satoshis: int = typer.Option(
        ..., help="the amount in satoshis the route should accomodate."
    ),
    time_pref: str = typer.Option(
        0, help="the time preference of the route, from 0 to 1. (LND only)."
    ),
    cltv: str = typer.Option(0, help="absolute lock time. (CLN only)."),
    pubkey: Optional[str] = typer.Option(
        None, help="The pubkey of the node. If not provided, use the default node."
    ),
):
    """
    Get a route.
    """
    if not pubkey:
        pubkey = get_default_id()
    ln = factory(pubkey)
    res = ln.get_route(
        fee_limit_msat=fee_limit_msat,
        pub_key=destination,
        source_pub_key=source_pub_key,
        outgoing_chan_id=outgoing_chan_id,
        ignored_nodes=ignored_nodes,
        ignored_pairs=ignored_pairs,
        last_hop_pubkey=last_hop_pubkey,
        amount_sat=satoshis,
        time_pref=time_pref,
        cltv=cltv,
    )
    print(res)
