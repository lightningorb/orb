# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-15 07:15:28
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-02-13 07:51:41

"""
This module stores useful functions for foreign-exchange math.
"""

from forex_python.bitcoin import BtcConverter
from orb.misc.utils_no_kivy import pref
from currency_symbols import CurrencySymbols

b = BtcConverter()


def forex(sats: float):
    """
    Convert the given number of Satoshis to the prefered
    currency as specified in the user prefs.

    >>> usd_price = forex(1_000_000)
    >>> '$' in usd_price
    True
    >>> usd_price = float(usd_price[1:])
    >>> usd_price > 100
    True
    """
    currency = pref("display.currency") or "USD"
    if currency == "SAT":
        return f"S{int(sats):,}"
    return f"{CurrencySymbols.get_symbol(currency)}{round(b.get_latest_price(currency) * int(sats) / 1e8, 2):,}"


# if __name__ == "__main__":
#     import doctest

#     doctest.testmod()
