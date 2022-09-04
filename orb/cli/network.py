# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-08-10 06:37:37
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-09-04 22:04:11

from typing import Optional
from invoke import task

from orb.cli.utils import get_default_id
from orb.ln import factory
from orb.app import App

import typer

app = typer.Typer()


@app.command()
def get_route(
    destination: str = typer.Argument(
        ..., help="the pub_key of the node to which to find a route."
    ),
    fee_limit_msat: str = typer.Option(500, help="the fee limit in millisatoshis."),
    source_pub_key: str = typer.Option(
        None, help="the pub_key of the node from which to find a route."
    ),
    outgoing_chan_id: str = typer.Option(
        None, help="the channel id the first hop o the route."
    ),
    ignored_nodes: str = typer.Option([], help="list of nodes to ignore."),
    ignored_pairs: str = typer.Option([], help="list of pairs to ignore (LND only)."),
    last_hop_pubkey: str = typer.Option(
        [], help="the last node before pub_key (LND only)."
    ),
    satoshis: int = typer.Option(
        1_000, help="the amount in satoshis the route should accomodate."
    ),
    time_pref: str = typer.Option(
        0, help="the time preference of the route, from 0 to 1. (LND only)."
    ),
    cltv: str = typer.Option(0, help="absolute lock time. (CLN only)."),
    pubkey: Optional[str] = typer.Option(
        None, help="The pubkey of the node. If not provided, use the default node."
    ),
):
    """

    This is a hard command to get right so that it looks and behaves similarly in CLN and LND, and messing up a route could be a bad idea, for this reason the returned object contains the *original*, as it was returned by lnd / cln.

    Sample result for LND
    ---------------------

    .. code:: json

        {
            "hops": [
                {
                    "amp_record": null,
                    "amt_to_forward": 1000,
                    "amt_to_forward_msat": 1000000,
                    "chan_capacity": 100000000,
                    "chan_id": 68345642782621696,
                    "custom_records": {},
                    "expiry": 63990,
                    "fee": 0,
                    "fee_msat": 0,
                    "metadata": "",
                    "mpp_record": null,
                    "pub_key": "031ce6d59ad4fe4158949dcd87ea49158dc6923f4457ec69bae9b0b04c13973213",
                    "tlv_payload": true
                }
            ],
            "original": {
                "hops": [
                    {
                        "amp_record": null,
                        "amt_to_forward": 1000,
                        "amt_to_forward_msat": 1000000,
                        "chan_capacity": 100000000,
                        "chan_id": 68345642782621696,
                        "custom_records": {},
                        "expiry": 63990,
                        "fee": 0,
                        "fee_msat": 0,
                        "metadata": "",
                        "mpp_record": null,
                        "pub_key": "031ce6d59ad4fe4158949dcd87ea49158dc6923f4457ec69bae9b0b04c13973213",
                        "tlv_payload": true
                    }
                ],
                "total_amt": 1000,
                "total_amt_msat": 1000000,
                "total_fees": 0,
                "total_fees_msat": 0,
                "total_time_lock": 63990
            },
            "total_amt": 1000,
            "total_amt_msat": 1000000,
            "total_fees": 0,
            "total_fees_msat": 0
        }


    Sample result for CLN
    ---------------------

    .. code:: json

        {
            "hops": [
                {
                    "amp_record": null,
                    "amt_to_forward": 1000,
                    "amt_to_forward_msat": 1000000,
                    "chan_capacity": 0,
                    "chan_id": "162x1x1",
                    "custom_records": {},
                    "direction": 0,
                    "expiry": 0,
                    "fee": 0.0,
                    "fee_msat": 0,
                    "metadata": "",
                    "mpp_record": null,
                    "pub_key": "0280dc76984a81124699b2a8b96b3167443b9dfad03c3c98c85bb2d020e6924283",
                    "tlv_payload": true
                }
            ],
            "original": {
                "api_version": "0.8.0",
                "route": [
                    {
                        "amount_msat": "1000000msat",
                        "channel": "162x1x1",
                        "delay": 0,
                        "direction": 0,
                        "id": "0280dc76984a81124699b2a8b96b3167443b9dfad03c3c98c85bb2d020e6924283",
                        "msatoshi": 1000000,
                        "style": "tlv"
                    }
                ]
            },
            "total_amt": 1000,
            "total_amt_msat": 1000000,
            "total_fees": 0,
            "total_fees_msat": 0
        }

    --cltv
    ~~~~~~

    The CLTV flag is required by CLN, but not LND.

    --time-pref
    ~~~~~~~~~~~

    This is also an awkward flag, as LND >= 0.15 can take a time-preference flag ranging from -1 and 1, however this flag is meaningless to CLN. So we keep the flag exposed, even though it does nothing with CLN.

    """
    if not pubkey:
        pubkey = get_default_id()
    ln = factory(pubkey)
    res = ln.get_route(
        fee_limit_msat=fee_limit_msat,
        pub_key=destination,
        source_pub_key=source_pub_key,
        outgoing_chan_id=outgoing_chan_id,
        ignored_nodes=ignored_nodes,
        ignored_pairs=ignored_pairs,
        last_hop_pubkey=last_hop_pubkey,
        amount_sat=satoshis,
        time_pref=time_pref,
        cltv=cltv,
    )
    print(res)
