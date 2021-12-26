# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-15 07:15:28
# @Last Modified by:   lnorb.com
# @Last Modified time: 2021-12-27 03:16:07

from orb.misc.decorators import guarded

from orb.components.popup_drop_shadow import PopupDropShadow
from orb.math.normal_distribution import NormalDistribution
from kivy_garden.graph import Graph, SmoothLinePlot
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp


from dataclasses import dataclass


@dataclass
class ChanRoutingData:
    """
    Simple dataclass that holds data for
    normal distribution calculation.
    """

    alias: str
    chan_id: str
    vals: float


@dataclass
class Event:
    """
    Simple dataclass that holds an Event for
    normal distribution calculation.
    """

    amt: int
    ppm: int

    def __lt__(self, other):
        return self.ppm < other.ppm

    def __hash__(self):
        return self.ppm


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
            fh = (
                model.FowardEvent()
                .select()
                .where(model.FowardEvent.chan_id_out == str(c.chan_id))
            )

            # compute the PPMs
            events = sorted(
                [
                    Event(
                        amt=f.amt_in,
                        ppm=int(((f.fee_msat / f.amt_in_msat) * 1_000_000_000) / 1_000),
                    )
                    for f in fh
                ]
            )

            alias = data_man.lnd.get_node_alias(c.remote_pubkey)

            norm_vals = []
            for e in events:
                for n in range(int(e.amt / 10_000)):
                    norm_vals.append(Event(ppm=e.ppm, amt=10_000))

            # make sure we have more than one event
            if len(set(norm_vals)) >= 2:
                self.chan_routing_data[i] = ChanRoutingData(
                    chan_id=str(c.chan_id),
                    vals=norm_vals,
                    alias=alias,
                )
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
