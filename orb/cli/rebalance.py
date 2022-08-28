# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-08-10 08:03:08
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-08-28 04:32:46


from .chalk import chalk

from invoke import task

from orb.logic.rebalance_thread import RebalanceThread
from orb.cli.utils import get_default_id
from orb.ln import factory
from orb.app import App


import typer

app = typer.Typer()


@app.command()
def rebalance(
    c,
    amount: int = 1_000,
    chan_id: str = None,
    last_hop_pubkey: str = None,
    max_paths: int = 10_000,
    fee_rate: int = 500,
    time_pref: float = 0,
    node: str = get_default_id(),
):
    """
    Rebalance the node
    """
    App().run(pubkey=node)
    ln = factory(node)
    App().build(ln)

    rebalance = RebalanceThread(
        amount=amount,
        chan_id=chan_id,
        last_hop_pubkey=last_hop_pubkey,
        fee_rate=fee_rate,
        time_pref=time_pref,
        max_paths=max_paths,
        name="RebalanceThread",
        thread_n=0,
        ln=ln,
    )
    rebalance.start()
