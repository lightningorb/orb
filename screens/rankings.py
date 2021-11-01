from kivy.uix.label import Label
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

        row_data = count_successes_failures()

        if row_data:
            self.data_tables = MDDataTable(
                use_pagination=True,
                rows_num=25,
                check=False,
                column_data=[
                    ("Alias", dp(60)),
                    ("Successes", dp(30), self.sort_on_signal),
                    ("Failures", dp(30)),
                ],
                row_data=row_data,
                sorted_on="Successes",
                sorted_order="ASC",
                elevation=2,
            )
            self.add_widget(self.data_tables)
        else:
            self.add_widget(
                Label(
                    text=(
                        'This feature ranks nodes by how predictable\n'
                        'they are at routing payments.\n'
                        'No path-finding data available.\n'
                        'Make payments, or circular rebalances.'
                    )
                )
            )

    @guarded
    def sort_on_signal(self, data):
        return zip(*sorted(enumerate(data), key=lambda l: l[1][1]))
