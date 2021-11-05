from collections import defaultdict
import json

from kivy.clock import mainthread
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.metrics import dp
from kivy.lang import Builder
from kivymd.uix.datatables import MDDataTable
from kivy.properties import ListProperty
from threading import Thread
from decorators import guarded
from kivy.properties import NumericProperty


class FeeSpy(Popup):

    data = ListProperty([])
    num_nodes = NumericProperty(0)
    num_channels = NumericProperty(0)

    def __init__(self, *args, **kwargs):
        super(FeeSpy, self).__init__(*args, **kwargs)

        self.bind(data=self.set_table)
        self.data_tables = None
        self.data = []

    @mainthread
    def set_table(self, *args):
        if self.data_tables:
            self.ids.box_layout.remove_widget(self.data_tables)
        self.data_tables = MDDataTable(
            use_pagination=False,
            rows_num=5,
            check=False,
            column_data=[
                ("Alias", dp(50)),
                ("Fee Changes", dp(50), self.sort_on_signal),
                ("Updates", dp(50)),
            ],
            row_data=self.data,
            sorted_on="Fee Changes",
            sorted_order="ASC",
            elevation=2,
            height=self.ids.box_layout.height,
        )
        self.ids.box_layout.add_widget(self.data_tables)

    @guarded
    def sort_on_signal(self, data):
        return zip(*sorted(enumerate(data), key=lambda l: l[1][1]))

    def get_data(self):
        from data_manager import data_man

        lnd = data_man.lnd

        updates = {}
        node_updates = {}

        @mainthread
        def update_ui():
            self.ids.num_nodes_tracking.text = (
                f"tracking {len(node_updates)} nodes, {len(updates)} channels"
            )

        def func():

            for r in lnd.subscribe_channel_graph():
                for u in r.channel_updates:
                    cid = u.chan_id
                    last = u.routing_policy.fee_rate_milli_msat / 1000
                    pk = u.advertising_node
                    if cid in updates:
                        updates[cid] = dict(
                            total=updates[cid]['total']
                            + (abs(updates[cid]['last'] - last)),
                            last=last,
                            updates=updates[cid]['updates'] + 1,
                            pk=pk,
                        )
                    else:
                        updates[cid] = dict(total=last, last=last, updates=1, pk=pk)

                    if pk not in node_updates:
                        node_updates[pk] = updates[cid]
                    else:
                        node_updates[pk]['total'] += updates[cid]['total']
                        node_updates[pk]['updates'] += 1
                    node_updates[pk]['total'] = round(node_updates[pk]['total'], 2)

                to_print = [
                    [
                        lnd.get_node_alias(k),
                        node_updates[k]['total'],
                        node_updates[k]['updates'],
                    ]
                    for k in sorted(
                        node_updates,
                        key=lambda x: node_updates[x]['total'],
                        reverse=True,
                    )[:5]
                ]
                if to_print != self.data:
                    self.data = to_print

                self.num_nodes = len(node_updates)
                self.num_channels = len(updates)
                # update_ui()

        t = Thread(target=func)
        t.start()

    def dismiss(self, *args):
        super(FeeSpy, self).dismiss(*args)

    def open(self, *args):
        super(FeeSpy, self).open(*args)
        self.get_data()
