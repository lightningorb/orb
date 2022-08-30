# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-08-23 04:36:36
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-08-30 13:28:12

from invoke import task
from .chalk import chalk
from orb.ln import factory
from typing import Optional
from orb.cli.utils import get_default_id
from datetime import datetime
from orb.app import App
from rich.pretty import pprint
import arrow
import typer

app = typer.Typer()


# @task(
#     help=dict(
#         pubkey="The Pubkey to use as the default pubkey for all Orb commands.",
#         peer_pubkey="The Pubkey of the peer you wish to open to",
#         amount_sats="The size of the channel in sats",
#         sat_per_vbyte="The fee to use in sats per vbytes",
#     )
# )
@app.command()
def open(
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


@app.command()
def list_forwards(
    pubkey: Optional[str] = typer.Argument(
        None, help="The pubkey of the node. If not provided, use the default node."
    ),
    # start_time: Optional[datetime] = typer.Argument(
    #     None,
    #     formats=["%Y-%m-%d", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S", "%m/%d/%Y"],
    #     help="Starting from this time",
    # ),
    # end_time: Optional[datetime] = typer.Argument(
    #     None,
    #     formats=["%Y-%m-%d", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S", "%m/%d/%Y"],
    #     help="Ending at this time",
    # ),
    index_offset: int = typer.Option(0, help="Start index."),
    num_max_events: int = typer.Option(100, help="Max number of events to return."),
):
    """
    List forwards for the node.
    """
    if not pubkey:
        pubkey = get_default_id()

    ln = factory(pubkey)
    for e in ln.get_forwarding_history(
        start_time=None,
        end_time=None,
        index_offset=index_offset,
        num_max_events=num_max_events,
    ).forwarding_events:
        pprint(e.todict())
