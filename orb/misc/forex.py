from forex_python.bitcoin import BtcConverter
from orb.misc.utils import pref
from currency_symbols import CurrencySymbols

b = BtcConverter()


def forex(sats):
    currency = pref('display.currency')
    if currency == 'SAT':
        return f'S{sats:,}'
    symbol = CurrencySymbols.get_symbol(currency)
    return f'{symbol}{round(b.get_latest_price(currency) * sats / 1e8, 2):,}'
