# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-15 07:15:28
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-08-16 15:00:16

import threading

from kivy.app import App

from kivy.clock import mainthread
from kivy.metrics import dp
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.datatables import MDDataTable

from orb.components.popup_drop_shadow import PopupDropShadow
from orb.misc.decorators import guarded
from orb.misc import mempool
from orb.ln import Ln


class Tab(MDFloatLayout, MDTabsBase):
    """Class implementing content for a tab."""


class BatchOpenScreen(PopupDropShadow):
    @guarded
    def open(self, *args):
        self.ids.pubkeys.text = (
            App.get_running_app().store.get("batch_open", {}).get("text", "")
        )
        super(BatchOpenScreen, self).open(*args)

    @guarded
    def calculate(self, text, amount):

        pks, amounts = [], []
        for line in text.split("\n"):
            if "," in line:
                pk, a = [x.strip() for x in line.split(",")]
                pks.append(pk)
                amounts.append(a)
            else:
                pk = line.strip()
                if pk:
                    pks.append(pk)
        amounts = [int(int(amount) / len(pks)) for _ in range(len(pks))]
        self.ids.pubkeys.text = "\n".join([f"{p},{a}" for p, a in zip(pks, amounts)])

    def ingest(self, text):
        App.get_running_app().store.put("batch_open", text=text)

    @guarded
    def get_pks_amounts(self):
        pks, amounts = [], []
        for line in self.ids.pubkeys.text.split("\n"):
            if "," in line:
                pk, a = [x.strip() for x in line.split(",")]
                pks.append(pk)
                amounts.append(a)
        return pks, amounts

    @guarded
    def on_tab_switch(self, instance_tabs, instance_tab, instance_tab_label, tab_text):
        if tab_text == "confirm":
            pks, amounts = self.get_pks_amounts()
            aliases = [Ln().get_node_alias(pk) for pk in pks]
            self.ids.table_layout.clear_widgets()
            self.ids.table_layout.add_widget(
                MDDataTable(
                    use_pagination=True,
                    rows_num=25,
                    check=False,
                    column_data=[("Alias", dp(60)), ("Amount", dp(30))],
                    row_data=[(al, f"{int(am):,}") for al, am in zip(aliases, amounts)],
                    elevation=2,
                )
            )

    @guarded
    def batch_open(self):
        pks, amounts = self.get_pks_amounts()
        try:
            response = Ln().batch_open(
                pubkeys=pks,
                amounts=amounts,
                sat_per_vbyte=mempool.get_fees("fastestFee") + 1,
            )
            self.ids.open_status.text = str(response)
            print(str(response))
        except Exception as e:
            self.ids.open_status.text = e.args[0].details
            print(e.args[0].details)

    @guarded
    def batch_connect(self):
        pks, amounts = self.get_pks_amounts()
        self.ids.connect.text = ""

        @mainthread
        def display(x):
            print(x)
            self.ids.connect.text += str(x) + "\n"

        def func(*args):
            for pk, amount in zip(pks, amounts):
                try:
                    info = Ln().get_node_info(pk)
                    display("-" * 50)
                    display(Ln().get_node_alias(pk))
                    display("-" * 50)
                    for address in info.addresses:
                        display(f"Connecting to: {pk}@{address.addr}")
                        try:
                            Ln().connect(f"{pk}@{address.addr}")
                            display("Attempted.")
                        except Exception as e:
                            display(e.args[0].details)
                except Exception as e:
                    display(e)

        threading.Thread(target=func).start()
