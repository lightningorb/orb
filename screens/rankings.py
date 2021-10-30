from kivy.metrics import dp
from popup_drop_shadow import PopupDropShadow
from kivy.uix.screenmanager import Screen
from decorators import guarded
from kivymd.uix.datatables import MDDataTable


class Rankings(PopupDropShadow):
    @guarded
    def __init__(self, *args):
        super(Rankings, self).__init__(*args)
        from store.node_rank import count_successes_failures

        self.data_tables = MDDataTable(
            use_pagination=True,
            rows_num=25,
            check=False,
            column_data=[
                ("Alias", dp(60)),
                ("Successes", dp(30), self.sort_on_signal),
                ("Failures", dp(30)),
            ],
            row_data=[x for x in count_successes_failures()],
            sorted_on="Successes",
            sorted_order="ASC",
            elevation=2,
        )
        self.add_widget(self.data_tables)

    # [Indexes, Sorted_Row_Data]
    def sort_on_signal(self, data):
        return zip(*sorted(enumerate(data), key=lambda l: l[1][1]))
