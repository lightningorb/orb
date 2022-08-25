# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-08-08 19:17:43
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-08-12 10:36:14


from invoke import task
from simple_chalk import chalk
from orb.ln import factory
from orb.cli.utils import get_default_id
from orb.app import App


@task(help=dict(node="The Pubkey to use as the default pubkey for all Orb commands"))
def get_route(
    c,
    pubkey: str,
    amount: int = 10_000,
    node: str = get_default_id(),
):
    """
    Print route.
    """
    App().run(pubkey=node)
    ln = factory(node)
    print(ln.get_route(pub_key=pubkey, amount=amount))
