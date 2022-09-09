# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-08-10 06:37:37
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-09-09 11:55:25

from invoke import task

from orb.logic.pay_invoices import PayInvoices
from orb.cli.utils import get_default_id
from orb.ln import factory
from orb.app import App

import typer

app = typer.Typer()


@app.command()
def invoices(
    chan_id: str = None,
    max_paths: int = 10_000,
    fee_rate: int = 500,
    time_pref: float = 0,
    num_threads: int = 5,
    pubkey: str = "",
):
    """
    Pay Ingested Invoices
    """
    if not pubkey:
        pubkey = get_default_id()

    App().run(pubkey=node)
    ln = factory(node)
    App().build(ln)

    pay_invoices = PayInvoices(
        chan_id=chan_id,
        max_paths=max_paths,
        fee_rate=fee_rate,
        time_pref=time_pref,
        num_threads=num_threads,
        ln=ln,
    )
    pay_invoices.start()


# @task(
#     help=dict(
#         pubkey="The Pubkey to use as the default pubkey for all Orb commands.",
#         total_amount_sat="The sum of the amount of all paid invoices should add up to total-amount-sat.",
#         url="The LNURL in the form LNURL....",
#         chunks="The number of chunks total-amount-sat is broken up into.",
#         num_threads="Make sure there are num-threads invoices available at any given time.",
#         rate_limit="Wait rate-limit seconds between each call to the LNURL generation endpoint.",
#         wait="Wait for payments to complete (setting this to False is only used for testing purposes).",
#     )
# )
@app.command()
def lnurl(
    url: str,
    total_amount_sat: int = 100_000_000,
    chunks: int = 100,
    num_threads: int = 5,
    rate_limit: int = 5,
    pubkey: str = "",
    wait: bool = True,
    chan_id: str = None,
    max_paths: int = 10_000,
    fee_rate: int = 500,
    time_pref: float = 0,
):
    """
    Generate bolt11 invoices from LNURL, and pay them.

    .. asciinema:: /_static/orb-pay-lnurl.cast
    """
    if not pubkey:
        pubkey = get_default_id()
    App().run(pubkey=pubkey)
    ln = factory(pubkey)
    App().build(ln)

    from orb.logic.lnurl_invoice_generator import LNUrlInvoiceGenerator

    iv = LNUrlInvoiceGenerator(
        url=url,
        total_amount_sat=total_amount_sat,
        chunks=chunks,
        num_threads=num_threads,
        rate_limit=rate_limit,
        ln=ln,
        wait=wait,
    )

    iv.daemon = True
    iv.start()

    pay_invoices = PayInvoices(
        chan_id=chan_id,
        max_paths=max_paths,
        fee_rate=fee_rate,
        time_pref=time_pref,
        num_threads=num_threads,
        ln=ln,
    )
    pay_invoices.start()
    iv.join()
    pay_invoices.join()
    App.get_running_app().stop()
