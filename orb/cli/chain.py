# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-08-08 19:04:21
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-08-27 15:50:23

from .chalk import chalk
from invoke import task
from orb.cli.utils import get_default_id
from orb.ln import factory
from orb.misc.monkey_patch import fix_annotations

fix_annotations()


@task
def fees(c):
    """
    Get mempool chain fees. Currently these are the fees from
    mempool.space

    >>> orb chain.fees

    fastestFee      : 7 sat/vbyte
    halfHourFee     : 1 sat/vbyte
    hourFee         : 1 sat/vbyte
    economyFee      : 1 sat/vbyte
    minimumFee      : 1 sat/vbyte
    """
    from orb.misc.mempool import get_fees

    fees = get_fees(use_prefs=False, network="mainnet")
    for k, v in fees.items():
        print(f"{chalk().green(k):<25}: {chalk().blueBright(v):<3} sat/vbyte")


@task
def deposit(c, pubkey: str = ""):
    """
    Get an on-chain address to deposit BTC.

    >>> orb chain.deposit

    deposit_address tb1q0wfpxdeh8wyvfcaxdxfrxj7qp753s47vu683ax
    deposit_qr:

    █▀▀▀▀▀█ ▄█▄  ▄▄█  ██  █▀▀▀▀▀█
    ...
    ▀▀▀▀▀▀▀ ▀▀▀  ▀   ▀▀▀▀    ▀ ▀▀
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


@task(
    help=dict(
        address="The destination address",
        pubkey="The node pubkey from which to send coins",
        amount="The amount to send in satoshis (for CLN this can be 'all')",
        sat_per_vbyte="Sats per vB (for CLN this can be slow, normal, urgent, or None)",
    )
)
def send(c, address: str, amount: int, sat_per_vbyte: int, pubkey: str = ""):
    """
    Send coins on-chain.

    >>> orb chain.send --amount 10_000 --sat-per-vbyte 1 --address tb1q0wfpxdeh8wyvfcaxdxfrxj7qp753s47vu683ax

    {
        "txid": "41ffa0fa564db85e65515fb3c3e2fe95d6a403c0f3473575dcad2bbde962c052"
    }

    """

    if not pubkey:
        pubkey = get_default_id()

    try:
        sat_per_vbyte = int(sat_per_vbyte)
    except:
        pass
    try:
        amount = int(amount)
    except:
        pass
    node = factory(pubkey)
    try:
        ret = node.send_coins(
            addr=address,
            amount=amount,
            sat_per_vbyte=sat_per_vbyte,
        )
        print(ret)
    except Exception as e:
        print(f"exception occured: {e}")
