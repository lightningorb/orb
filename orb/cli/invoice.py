# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-08-08 19:17:43
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-08-28 06:26:48

from .chalk import chalk
from orb.ln import factory
from typing import Optional
from orb.cli.utils import get_default_id
from orb.app import App

import typer

app = typer.Typer()


@app.command()
def generate(
    satoshis: Optional[int] = typer.Argument(
        1_000, help="The amount of Satoshis for this invoice."
    ),
    pubkey: Optional[str] = typer.Argument(
        None, help="The pubkey of the node. If not provided, use the default node."
    ),
):
    """
    Generate a bolt11 invoice.
    """
    import io
    import qrcode

    if not pubkey:
        pubkey = get_default_id()

    App().run(pubkey=pubkey)
    ln = factory(pubkey)
    invoice = ln.generate_invoice(amount=satoshis, memo="Orb CLI invoice")
    print(f"{chalk().green('Invoice:')} {invoice[0]}")
    print(chalk().green(f"deposit_qr:"))
    qr = qrcode.QRCode()
    qr.add_data(invoice[0])
    f = io.StringIO()
    qr.print_ascii(out=f)
    f.seek(0)
    print(f.read())
