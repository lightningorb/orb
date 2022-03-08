# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-02-01 12:59:05
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-02-01 13:56:44

from pathlib import Path
from threading import Thread
from traceback import format_exc

from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog

from orb.misc.plugin import Plugin
from orb.misc.decorators import guarded
from orb.misc.forex import forex

from forex_python.bitcoin import BtcConverter
from forex_python.converter import CurrencyRates

c = CurrencyRates()
b = BtcConverter()


class Content(BoxLayout):
    def convert(self):
        def func():
            try:
                self.ids._result.text = "Getting rates..."
                _from = self.ids._from.text
                _to = self.ids._to.text
                _amount = float(self.ids._amount.text)
                if len(_from) == len(_to) == 3:
                    if _from == "BTC":
                        rate = float(b.get_latest_price(_to))
                        self.ids._result.text = f"{round(rate * _amount, 2):_}"
                    elif _to == "BTC":
                        rate = float(b.get_latest_price(_from))
                        self.ids._result.text = f"{round(_amount / rate, 8):_}"
                    elif _from == "SAT":
                        rate = float(b.get_latest_price(_to))
                        self.ids._result.text = f"{round(rate * _amount / 1e8, 2):_}"
                    elif _to == "SAT":
                        rate = float(b.get_latest_price(_from))
                        self.ids._result.text = f"{int(_amount / rate * 1e8):_}"
                    else:
                        self.ids._result.text = (
                            f"{round(c.convert(_from, _to, _amount), 2):_}"
                        )
            except:
                self.ids._result.text = "..."
                print(format_exc())

        Thread(target=func).start()


class CurrencyConverter(Plugin):
    def main(self):
        kv_path = (Path(__file__).parent / "currency_converter.kv").as_posix()
        Builder.unload_file(kv_path)
        Builder.load_file(kv_path)

        self.dialog = MDDialog(
            title="Currency Converter", type="custom", content_cls=Content()
        )
        self.dialog.open()
