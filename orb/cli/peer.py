# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-08-23 04:48:14
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-08-28 06:24:00

from invoke import task
from .chalk import chalk
from orb.ln import factory
from orb.cli.utils import get_default_id
from orb.app import App

import typer

app = typer.Typer()

# @task(
#     help=dict(
#         pubkey="The Pubkey to use as the default pubkey for all Orb commands.",
#         peer_pubkey="The Pubkey of the peer you wish to open to",
#     )
# )
@app.command()
def connect(
    peer_pubkey: str,
    pubkey: str = "",
):
    """
    Connect to a peer.
    """
    if not pubkey:
        pubkey = get_default_id()

    ln = factory(pubkey)
    info = ln.get_node_info(peer_pubkey)
    for address in info.addresses:
        fq = f"{peer_pubkey}@{address.addr}"
        print(f'{chalk().blueBright("Connecting to: ")} {chalk().greenBright(fq)}')
        res = ln.connect(fq)
        print(res)


# @task(
#     help=dict(
#         pubkey="The Pubkey to use as the default pubkey for all Orb commands.",
#     )
# )
@app.command()
def list(
    pubkey: str = "",
):
    """
    List peers.
    """
    if not pubkey:
        pubkey = get_default_id()

    ln = factory(pubkey)
    peers = ln.list_peers()
    for p in peers.peers:
        print(f"{chalk().blueBright(p.pub_key)}")
