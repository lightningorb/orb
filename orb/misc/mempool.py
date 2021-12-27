# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-15 07:15:28
# @Last Modified by:   lnorb.com
# @Last Modified time: 2021-12-27 10:02:56

import requests


def get_fees(which=None):
    """
    Get Mempool fees from mempool.space.

    >>> fees = get_fees()

    >>> fees['fastestFee'] >= 1
    True

    >>> fees['halfHourFee'] >= 1
    True

    >>> fees['hourFee'] >= 1
    True

    >>> fees['minimumFee'] >= 1
    True

    >>> get_fees('fastestFee') >= 1
    True
    """
    # TODO: Should use an enum style class rather than strings.

    fees = requests.get("https://mempool.space/api/v1/fees/recommended").json()
    return fees[which] if which else fees


if __name__ == "__main__":
    import doctest

    doctest.testmod()
