# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-08-23 04:36:36
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-09-06 17:12:41

from datetime import datetime
from typing import Optional

from orb.logic.rebalance_thread import RebalanceThread
from orb.cli.utils import get_default_id
from orb.ln import factory
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

    .. asciinema:: /_static/orb-channel-open.cast
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
    index_offset: int = typer.Option(0, help="Start index."),
    num_max_events: int = typer.Option(100, help="Max number of events to return."),
):
    """
    List forwards for the node.

    .. asciinema:: /_static/orb-channel-list-forwards.cast
    """
    if not pubkey:
        pubkey = get_default_id()

    ln = factory(pubkey)
    for e in ln.get_forwarding_history(
        index_offset=index_offset,
        num_max_events=num_max_events,
    ).forwarding_events:
        pprint(e.todict())


@app.command()
def rebalance(
    satoshis: int = typer.Argument(1_000, help="Amount to rebalance."),
    outgoing_chan_id: str = typer.Option(None, help="Outgoing channel ID."),
    last_hop_pubkey: str = typer.Option(None, help="Pubkey of the last hop."),
    max_paths: int = typer.Option(
        10_000, help="Max number of paths to attempt before giving up."
    ),
    fee_rate: int = typer.Option(500, help="Fee rate PPM for circular payment."),
    time_pref: float = typer.Option(0, help="Time preference (LND only)."),
    pubkey: str = get_default_id(),
):
    """
    Rebalance the node
    """
    App().run(pubkey=pubkey)
    ln = factory(pubkey)
    App().build(ln)

    rt = RebalanceThread(
        amount=satoshis,
        chan_id=outgoing_chan_id,
        last_hop_pubkey=last_hop_pubkey,
        fee_rate=fee_rate,
        time_pref=time_pref,
        max_paths=max_paths,
        name="RebalanceThread",
        thread_n=0,
        ln=ln,
    )
    rt.start()
