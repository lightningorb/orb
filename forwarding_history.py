from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
import data_manager
from ui_actions import console_output
from threading import Thread
from collections import defaultdict
import arrow


def get_forwarding_history():
    from store import model

    return (
        model.FowardEvent().select()
    )  # .where(model.FowardEvent.chan_id_in == '772380530381488129')


def download_forwarding_history():
    def func():
        from store import model

        console_output('downloading forwarding history')
        last = (
            model.FowardEvent.select()
            .order_by(model.FowardEvent.timestamp_ns.desc())
            .first()
        )
        console_output('last event:')
        console_output(last)
        lnd = data_manager.data_man.lnd
        i = 0
        start_time = int(last.timestamp_ns / 1000) if last else None
        while True:
            console_output(f'fetching events {i} -> {i + 100}')
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
        console_output('downloaded forwarding history')

    Thread(target=func).start()


def clear_forwarding_history():
    from store import model

    model.FowardEvent.delete().execute()


def view_forwarding_history():
    from kivy.uix.popup import Popup
    from kivy.uix.label import Label
    from data_manager import data_man
    import requests

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
    Satoshis:

    total fees: s{total_fee:,}
    total out: s{total_out:,} 
    total in: s{total_in:,}

    last event:
    {arrow.get(last_event).format('YYYY-MM-DD HH:mm:ss')}
    """

    popup = Popup(
        title='Total Routing',
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
            ret.append(float('nan'))
    return ret


def graph_fees_earned():
    from kivy.uix.popup import Popup
    from kivy_garden.graph import Graph, MeshLinePlot

    fh = get_forwarding_history()
    buckets = defaultdict(int)
    for f in fh:
        date = int(
            arrow.get(f.timestamp).replace(hour=0, minute=0, second=0).timestamp()
        )
        buckets[date] += f.fee
    graph = Graph(
        size_hint=[1, 0.9],
        xlabel='Day',
        ylabel='Sats',
        x_ticks_major=5,
        y_ticks_major=10_000,
        y_ticks_minor=1000,
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
        MeshLinePlot(
            color=[1, 0.5, 0.5, 1],
            points=[(k, v) for k, v in enumerate(buckets.values())],
        )
    )
    graph.add_plot(
        MeshLinePlot(
            color=[0.5, 0.5, 1, 1],
            points=[(k, v) for k, v in enumerate(sma(list(buckets.values()), 7))],
        )
    )
    bl = BoxLayout(orientation='vertical')
    bl.add_widget(graph)
    bl.add_widget(
        Label(
            size_hint=(1, 0.1),
            text=(
                f'Total routing fees earned: {round((sum(buckets.values())/1e8), 8)}'
                f' BTC ({sum(buckets.values()):,} sats)'
            ),
        )
    )
    popup = Popup(
        title='fees earned',
        content=bl,
        size_hint=(1, 1),
        background_color=(0.6, 0.6, 0.8, 0.9),
        overlay_color=(0, 0, 0, 0),
    )
    popup.open()
