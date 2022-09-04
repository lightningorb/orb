# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-08-08 19:04:21
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-09-04 17:02:01

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
    """
    from orb.misc.mempool import get_fees

    fees = get_fees(use_prefs=False, network="mainnet")
    for k, v in fees.items():
        print(f"{chalk().green(k):<25}: {chalk().blueBright(v):<3} sat/vbyte")


@app.command()
def deposit(pubkey: str = ""):
    """
    Get an on-chain address to deposit BTC.
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

    # help=dict(
    #     address="The destination address",
    #     pubkey="The node pubkey from which to send coins",
    #     amount="The amount to send in satoshis (for CLN this can be 'all')",
    #     sat_per_vbyte="Sats per vB (for CLN this can be slow, normal, urgent, or None)",
    # )


@app.command()
def send(
    address: str,
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
    """

    if not pubkey:
        pubkey = get_default_id()
    node = factory(pubkey)
    for k, v in factory(pubkey).get_balance().__dict__.items():
        val = f"{v:_}"
        pprint_from_ansi(f"{chalk().greenBright(k)}: {chalk().blueBright(val)}")
