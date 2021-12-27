# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-15 07:15:28
# @Last Modified by:   lnorb.com
# @Last Modified time: 2021-12-27 05:12:57
from orb.logic.normalized_events import ChanRoutingData, Event
from orb.misc.decorators import guarded

from orb.components.popup_drop_shadow import PopupDropShadow
from orb.math.normal_distribution import NormalDistribution
from kivy_garden.graph import Graph, SmoothLinePlot
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
from orb.logic.normalized_events import get_descritized_routing_events


class FeeDistribution(PopupDropShadow):
    """
    This dialog displays normal distributions of routing event fees.
    """

    def open(self, *args):
        """
        Invoked when the dialog opens. Fetches the rourting events and
        prepares the data for normal distribution analysis.
        """
        from data_manager import data_man
        from orb.store import model

        self.chan_routing_data = {}
        self.channel_n = 0
        i = 0

        for c in data_man.lnd.get_channels():
            routing_events = get_descritized_routing_events(c)
            if routing_events:
                self.chan_routing_data[i] = routing_events
                i += 1

        self.next_channel()
        super(FeeDistribution, self).open(*args)

    @guarded
    def next_channel(self):
        """
        Callback, when the 'Next' button is clicked.
        """
        self.graph_channel(self.channel_n % len(self.chan_routing_data))
        self.channel_n += 1

    @guarded
    def graph_channel(self, i):
        """
        Performs the normal distribution calculations, and graphs the
        result in the dialog.
        """

        chan_routing_data = self.chan_routing_data[i]
        nd = NormalDistribution()
        nd.data = [x.ppm for x in chan_routing_data.vals]
        nd.calculate_prob_dist()
        self.ids.table.clear_widgets()
        self.ids.table.add_widget(
            MDDataTable(
                use_pagination=False,
                check=False,
                column_data=[
                    ("Value", dp(10)),
                    ("Prob.", dp(20)),
                    ("Norm Prob.", dp(20)),
                    ("Freq.", dp(10)),
                    ("Norm Freq.", dp(20)),
                ],
                row_data=nd.table,
                elevation=2,
            )
        )

        self.ids.alias.text = chan_routing_data.alias
        values = [int(item["value"]) for item in nd.probability_distribution]
        probs = [int(item["probability"] * 100) for item in nd.probability_distribution]

        graph = Graph(
            size_hint=[1, 1],
            xlabel="PPM",
            ylabel="Probability %",
            x_ticks_major=int((max(values) - min(values)) / 10),
            y_ticks_major=int((max(probs) - min(probs)) / 10),
            y_grid_label=True,
            x_grid_label=True,
            padding=5,
            x_grid=True,
            y_grid=True,
            xmin=min(values) - 1,
            xmax=max(values) + 1,
            ymin=min(probs) - 1,
            ymax=max(probs) + 1,
        )
        plot = SmoothLinePlot(color=[1, 0, 0, 1])
        plot.points = [*zip(values, probs)]
        graph.add_plot(plot)
        self.ids.bl.clear_widgets()
        self.ids.bl.add_widget(graph)