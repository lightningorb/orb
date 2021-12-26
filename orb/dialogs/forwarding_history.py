# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-15 07:15:28
# @Last Modified by:   lnorb.com
# @Last Modified time: 2021-12-25 03:56:39

from collections import defaultdict
from threading import Thread
import arrow

from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout


from orb.misc.forex import forex

import data_manager


def get_forwarding_history():
    from orb.store import model

    return model.FowardEvent().select()


def download_forwarding_history(*args, **kwargs):
    def func():
        from orb.store import model

        last = (
            model.FowardEvent.select()
            .order_by(model.FowardEvent.timestamp_ns.desc())
            .first()
        )
        lnd = data_manager.data_man.lnd
        i = 0
        start_time = int(last.timestamp) if last else None
        while True:
            fwd = lnd.get_forwarding_history(
                start_time=start_time, index_offset=i, num_max_events=100
            )

            for j, f in enumerate(fwd.forwarding_events):
                if j == 0 and start_time:
                    # if this is not the first run, then skip the first
                    # event, else it will show up as a duplicate
                    continue

                ev = model.FowardEvent(
                    timestamp=int(f.timestamp),
                    chan_id_in=int(f.chan_id_in),
                    chan_id_out=int(f.chan_id_out),
                    amt_in=int(f.amt_in),
                    amt_out=int(f.amt_out),
                    fee=int(f.fee),
                    fee_msat=int(f.fee_msat),
                    amt_in_msat=int(f.amt_in_msat),
                    amt_out_msat=int(f.amt_out_msat),
                    timestamp_ns=int(f.timestamp_ns),
                )
                ev.save()
            i += 100
            if not fwd.forwarding_events:
                break

    Thread(target=func).start()


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
    from kivy.uix.popup import Popup
    from kivy_garden.graph import Graph, MeshLinePlot, SmoothLinePlot

    fh = get_forwarding_history()
    buckets = defaultdict(int)
    for f in fh:
        date = int(
            arrow.get(f.timestamp).replace(hour=0, minute=0, second=0).timestamp()
        )
        buckets[date] += f.fee
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
