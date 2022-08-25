# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-15 07:15:28
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-08-10 10:59:25

import requests


def get_fees(which=None, use_prefs=True, network="mainnet"):
    """
    Get Mempool fees from mempool.space.

    >>> fees = get_fees()
    >>> fees['fastestFee'] >= 1
    True
    >>> fees["halfHourFee"] >= 1
    True
    >>> fees['hourFee'] >= 1
    True
    >>> fees['minimumFee'] >= 1
    True

    >>> get_fees('fastestFee') >= 1
    True
    """
    # TODO: Should use an enum style class rather than strings.
    lut = dict(testnet="testnet/", signet="signet/", mainnet="")
    if use_prefs:
        from orb.misc.utils_no_kivy import pref

        path = lut[pref("ln.network") or "mainnet"]
    else:
        path = lut[network]
    url = f"https://mempool.space/{path}api/v1/fees/recommended"
    fees = requests.get(url).json()
    return fees[which] if which else fees


if __name__ == "__main__":
    import doctest

    doctest.testmod()
