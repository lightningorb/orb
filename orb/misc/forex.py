# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-15 07:15:28
# @Last Modified by:   lnorb.com
# @Last Modified time: 2021-12-30 08:05:53

from forex_python.bitcoin import BtcConverter
from orb.misc.utils import pref
from currency_symbols import CurrencySymbols

b = BtcConverter()


def forex(sats):
    currency = pref("display.currency")
    if currency == "SAT":
        return f"S{int(sats):,}"
    symbol = CurrencySymbols.get_symbol(currency)
    return f"{symbol}{round(b.get_latest_price(currency) * int(sats) / 1e8, 2):,}"
