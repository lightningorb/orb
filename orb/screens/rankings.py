from kivy.properties import StringProperty
from kivy.uix.label import Label
from kivy.metrics import dp
from orb.components.popup_drop_shadow import PopupDropShadow
from orb.misc.decorators import guarded
from kivymd.uix.datatables import MDDataTable


class RankingsFileChooser(PopupDropShadow):

    selected_path = StringProperty('')


class RankingsExportPath(PopupDropShadow):

    selected_path = StringProperty('')


class Rankings(PopupDropShadow):
    @guarded
    def __init__(self, *args):
        super(Rankings, self).__init__(*args)

    def open(self, *args):
        super(Rankings, self).open(*args)
        from orb.store.node_rank import count_successes_failures

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
            self.ids.box_layout.add_widget(self.data_tables)
        else:
            self.ids.box_layout.add_widget(
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

    @guarded
    def ingest(self):
        dialog = RankingsFileChooser()
        dialog.open()

        def do_ingest(widget, path):
            from orb.store import node_rank

            node_rank.ingest(path)

        dialog.bind(selected_path=do_ingest)

    @guarded
    def export(self):
        dialog = RankingsExportPath()
        dialog.open()

        def do_export(widget, path):
            from orb.store import node_rank

            node_rank.export(path)

        dialog.bind(selected_path=do_export)
