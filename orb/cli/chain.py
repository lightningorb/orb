# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-08-08 19:04:21
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-09-05 11:50:30

from typing import Optional, Union
from .chalk import chalk
from orb.cli.utils import get_default_id
from orb.ln import factory

from orb.cli.utils import pprint
from orb.cli.utils import pprint_from_ansi

import typer

app = typer.Typer(help="Commands relating to on-chain activities")


@app.command()
def fees():
    """
    Get mempool chain fees. Currently these are the fees from
    mempool.space

    .. asciinema:: /_static/orb-chain-fees.cast
    """
    from orb.misc.mempool import get_fees

    fees = get_fees(use_prefs=False, network="mainnet")
    for k, v in fees.items():
        print(f"{chalk().green(k):<25}: {chalk().blueBright(v):<3} sat/vbyte")


@app.command()
def deposit(
    pubkey: Optional[str] = typer.Argument(
        None, help="The pubkey of the node. If not provided, use the default node."
    ),
):
    """
    Get an on-chain address to deposit BTC.

    .. asciinema:: /_static/orb-chain-deposit.cast

    """

    import io
    import qrcode

    if not pubkey:
        pubkey = get_default_id()

    ad = factory(pubkey).new_address()
    print(f"{chalk().green('deposit_address')} {ad.address}")
    print(chalk().green(f"deposit_qr:"))
    qr = qrcode.QRCode()
    qr.add_data(ad.address)
    f = io.StringIO()
    qr.print_ascii(out=f)
    f.seek(0)
    print(f.read())


@app.command()
def send(
    address: str = typer.Argument(..., help="Destination address."),
    satoshi: str = typer.Argument(
        ..., help="Amount to send, expressed in satoshis, or 'all'."
    ),
    sat_per_vbyte: int = typer.Argument(
        ..., help="Sat per vbyte to use for the transaction."
    ),
    pubkey: Optional[str] = typer.Argument(
        None, help="The pubkey of the node. If not provided, use the default node."
    ),
):
    """
    Send coins on-chain.

    .. asciinema:: /_static/orb-chain-send.cast
    """
    if not pubkey:
        pubkey = get_default_id()

    send_all = False
    if satoshi == "all":
        send_all = True
        satoshi = 0
    else:
        satoshi = int(satoshi)
    node = factory(pubkey)
    try:
        ret = node.send_coins(
            addr=address,
            satoshi=satoshi,
            sat_per_vbyte=sat_per_vbyte,
            send_all=send_all,
        )
        for k, v in ret.__dict__.items():
            pprint_from_ansi(f"{chalk().greenBright(k)}: {chalk().blueBright(v)}")

    except Exception as e:
        print(f"exception occured: {e}")


@app.command()
def balance(
    pubkey: Optional[str] = typer.Argument(
        None, help="The pubkey of the node. If not provided, use the default node."
    ),
):
    """
    Get on-chain balance.

    .. asciinema:: /_static/orb-chain-balance.cast

    """

    if not pubkey:
        pubkey = get_default_id()
    node = factory(pubkey)
    for k, v in factory(pubkey).get_balance().__dict__.items():
        val = f"{v:_}"
        pprint_from_ansi(f"{chalk().greenBright(k)}: {chalk().blueBright(val)}")
