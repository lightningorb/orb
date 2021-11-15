from kivy.metrics import dp
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.icon_definitions import md_icons
from kivy.core.clipboard import Clipboard
from kivymd.uix.datatables import MDDataTable
from kivy.uix.label import Label
from kivymd.uix.datatables import MDDataTable

from orb.components.popup_drop_shadow import PopupDropShadow
from orb.misc.ui_actions import console_output
from orb.misc.decorators import guarded
from orb.misc import mempool

import data_manager


class Tab(MDFloatLayout, MDTabsBase):
    '''Class implementing content for a tab.'''


class BatchOpenScreen(PopupDropShadow):
    @guarded
    def calculate(self, text, amount):
        pks, amounts = [], []
        for line in text.split('\n'):
            if ',' in line:
                pk, a = [x.strip() for x in line.split(',')]
                pks.append(pk)
                amounts.append(a)
            else:
                pk = line.strip()
                if pk:
                    pks.append(pk)
        amounts = [int(int(amount) / len(pks)) for _ in range(len(pks))]
        self.ids.pubkeys.text = '\n'.join([f'{p},{a}' for p, a in zip(pks, amounts)])

    @guarded
    def get_pks_amounts(self):
        pks, amounts = [], []
        for line in self.ids.pubkeys.text.split('\n'):
            if ',' in line:
                pk, a = [x.strip() for x in line.split(',')]
                pks.append(pk)
                amounts.append(a)
        return pks, amounts

    @guarded
    def on_tab_switch(self, instance_tabs, instance_tab, instance_tab_label, tab_text):
        if tab_text == 'open':
            from data_manager import data_man

            pks, amounts = self.get_pks_amounts()
            aliases = [data_man.lnd.get_node_alias(pk) for pk in pks]
            self.ids.table_layout.clear_widgets()
            self.ids.table_layout.add_widget(
                MDDataTable(
                    use_pagination=False,
                    check=False,
                    column_data=[("Alias", dp(60)), ("Amount", dp(30))],
                    row_data=[(al, f'{int(am):,}') for al, am in zip(aliases, amounts)],
                    elevation=2,
                )
            )

    @guarded
    def batch_open(self):
        pks, amounts = self.get_pks_amounts()
        from data_manager import data_man

        data_man.lnd.batch_open(
            pubkeys=pks, amounts=amounts, sat_per_vbyte=mempool.get_fees('halfHourFee')
        )
