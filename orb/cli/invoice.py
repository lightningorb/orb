# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-08-08 19:17:43
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-08-22 11:42:26


from invoke import task
from .chalk import chalk
from orb.ln import factory
from orb.cli.utils import get_default_id
from orb.app import App


@task(
    help=dict(
        pubkey="The Pubkey to use as the default pubkey for all Orb commands.",
        total_amount_sat="The sum of the amount of all paid invoices should add up to total-amount-sat.",
        url="The LNURL in the form LNURL....",
        chunks="The number of chunks total-amount-sat is broken up into.",
        num_threads="Make sure there are num-threads invoices available at any given time.",
        rate_limit="Wait rate-limit seconds between each call to the LNURL generation endpoint.",
        wait="Wait for payments to complete (setting this to False is only used for testing purposes).",
    )
)
def lnurl_generate(
    c,
    url: str,
    total_amount_sat: int = 100_000_000,
    chunks: int = 100,
    num_threads: int = 5,
    rate_limit: int = 5,
    pubkey: str = "",
    wait: bool = True,
):
    """
    Generate bolt11 invoices from LNURL.
    """
    if not pubkey:
        pubkey = get_default_id()

    App().run(pubkey=pubkey)
    ln = factory(pubkey)
    App().build(ln)

    from orb.logic.lnurl_invoice_generator import LNUrlInvoiceGenerator

    try:
        iv = LNUrlInvoiceGenerator(
            url=url,
            total_amount_sat=total_amount_sat,
            chunks=chunks,
            num_threads=num_threads,
            rate_limit=rate_limit,
            ln=ln,
            wait=wait,
        )

        iv.start()
    except Exception as e:
        print(f"exception occured: {e}")


@task(help=dict(pubkey="The Pubkey to use as the default pubkey for all Orb commands"))
def generate(
    c,
    satoshis: int = 10_000,
    pubkey: str = "",
):
    """
    Generate bolt11 invoices.
    """
    import io
    import qrcode

    if not pubkey:
        pubkey = get_default_id()

    App().run(pubkey=pubkey)
    ln = factory(pubkey)
    invoice = ln.generate_invoice(amount=satoshis, memo="Orb CLI invoice")
    ad = factory(pubkey).new_address()
    print(f"{chalk().green('Invoice:')} {invoice[0]}")
    print(chalk().green(f"deposit_qr:"))
    qr = qrcode.QRCode()
    qr.add_data(invoice[0])
    f = io.StringIO()
    qr.print_ascii(out=f)
    f.seek(0)
    print(f.read())


@task(help=dict(pubkey="The Pubkey to use as the default pubkey for all Orb commands"))
def ingest(
    c,
    bolt11_invoice: str,
    pubkey: str = "",
):
    """
    Ingest invoice into invoices DB.
    """
    from orb.store import model

    if not pubkey:
        pubkey = get_default_id()

    App().run(pubkey=pubkey)
    ln = factory(pubkey)
    req = ln.decode_payment_request(bolt11_invoice)
    print(req)
    # if model.Invoice().select().where(model.Invoice.raw == bolt11_invoice):
    # raise Exception("Already ingested")
    # invoice = model.Invoice(
    #     raw=bolt11_invoice,
    #     destination=req.destination,
    #     num_satoshis=req.num_satoshis,
    #     timestamp=req.timestamp,
    #     expiry=req.expiry,
    #     description=req.description,
    # )
    # invoice.save()
