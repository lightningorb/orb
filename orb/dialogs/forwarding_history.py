# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-15 07:15:28
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-01-30 17:03:18

from collections import defaultdict
from threading import Thread
import arrow
from kivy.uix.popup import Popup
from kivy_garden.graph import Graph, SmoothLinePlot
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout

from orb.misc.forex import forex
from orb.lnd import Lnd


def get_forwarding_history():
    from orb.store import model

    return model.FowardEvent().select()


def view_forwarding_history():
    from kivy.uix.popup import Popup
    from kivy.uix.label import Label

    fh = get_forwarding_history()

    total_out = 0
    total_in = 0
    total_fee = 0
    last_event = 0

    for f in fh.iterator():
        total_out += f.amt_out
        total_in += f.amt_in
        total_fee += f.fee
        last_event = f.timestamp

    text = f"""
    total fees: {forex(total_fee)}
    total out: {forex(total_out)} 
    total in: {forex(total_in)}

    last event:
    {arrow.get(last_event).format('YYYY-MM-DD HH:mm:ss')}
    """

    popup = Popup(
        title="Total Routing",
        content=Label(text=text),
        size_hint=(None, None),
        size=(500, 500),
    )
    popup.open()


def sma(data, n=3):
    ret = []
    for i in range(len(data)):
        if i >= n:
            ret.append(sum(data[i - n : i]) / n)
        else:
            ret.append(float("nan"))
    return ret


def graph_fees_earned():

    fh = get_forwarding_history()
    buckets = defaultdict(int)
    for f in fh:
        buckets[
            int(arrow.get(f.timestamp).replace(hour=0, minute=0, second=0).timestamp())
        ] += f.fee
    if not buckets:
        return
    last = sorted(buckets.keys(), reverse=True)[0]
    del buckets[last]
    if not buckets:
        return

    graph = Graph(
        size_hint=[1, 0.9],
        xlabel="Day",
        ylabel="Sats",
        x_ticks_major=5,
        y_ticks_major=30_000,
        y_grid_label=True,
        x_grid_label=True,
        padding=5,
        x_grid=True,
        y_grid=True,
        xmin=0,
        xmax=len(buckets),
        ymin=0,
        ymax=max(buckets.values()),
    )
    graph.add_plot(
        SmoothLinePlot(
            color=[1, 0.5, 0.5, 1],
            points=[(k, v) for k, v in enumerate(buckets.values())],
        )
    )
    graph.add_plot(
        SmoothLinePlot(
            color=[0.5, 0.5, 1, 1],
            points=[(k, v) for k, v in enumerate(sma(list(buckets.values()), 7))],
        )
    )
    graph.add_plot(
        SmoothLinePlot(
            color=[0.5, 1, 0.5, 1],
            points=[(k, v) for k, v in enumerate(sma(list(buckets.values()), 30))],
        )
    )
    bl = BoxLayout(orientation="vertical")
    bl.add_widget(graph)
    bl.add_widget(
        Label(
            size_hint=(1, 0.1),
            text=(
                f"Total routing fees earned: {round((sum(buckets.values())/1e8), 8)}"
                f" BTC ({sum(buckets.values()):,} sats)"
            ),
        )
    )
    popup = Popup(
        title="fees earned",
        content=bl,
        size_hint=(0.9, 0.9),
        background_color=(0.6, 0.6, 0.8, 0.9),
        overlay_color=(0, 0, 0, 0),
    )
    popup.open()
