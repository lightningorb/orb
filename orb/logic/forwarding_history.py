# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-01-30 17:01:24
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-08-29 13:44:29

import arrow
from time import sleep
from threading import Thread, Lock

from orb.app import App
from orb.misc.decorators import guarded
from orb.misc.decorators import db_connect
from orb.core.stoppable_thread import StoppableThread
from orb.store.db_meta import channel_stats_db_name, forwarding_events_db_name

lock = Lock()


class DownloadFowardingHistory(StoppableThread):
    def run(self):
        from orb.store import model

        def update_stats(f, ev):
            out_stats = (
                model.ChannelStats()
                .select()
                .where(model.ChannelStats.chan_id == int(f.chan_id_out))
            )
            if out_stats:
                out_stats = out_stats.first()
                out_stats.earned_msat += ev.fee_msat
            else:
                out_stats = model.ChannelStats(
                    chan_id=int(f.chan_id_out), earned_msat=int(f.fee_msat)
                )
            out_stats.save()
            in_stats = (
                model.ChannelStats()
                .select()
                .where(model.ChannelStats.chan_id == int(f.chan_id_in))
            )
            if in_stats:
                in_stats = in_stats.first()
                in_stats.helped_earn_msat += ev.fee_msat
            else:
                in_stats = model.ChannelStats(
                    chan_id=int(f.chan_id_in), helped_earn_msat=int(f.fee_msat)
                )
            in_stats.save()

        def clear_stats():
            stats = model.ChannelStats().select()
            if stats:
                for s in stats:
                    s.earned_msat = 0
                    s.helped_earn_msat = 0
                    s.save()

        @guarded
        @db_connect(channel_stats_db_name, lock=False)
        @db_connect(forwarding_events_db_name, lock=False)
        def func():
            if lock.locked():
                return
            with lock:
                chunk_size = 100

                last = (
                    model.ForwardEvent.select()
                    .order_by(model.ForwardEvent.timestamp_ns.desc())
                    .first()
                )
                start_offset = last.id if last else 0
                if start_offset == 0:
                    clear_stats()
                app = App.get_running_app()
                while not self.stopped():
                    print(".")
                    fwd = app.ln.get_forwarding_history(
                        index_offset=start_offset, num_max_events=chunk_size
                    )
                    for f in fwd.forwarding_events:
                        ev = model.ForwardEvent(
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
                        print(
                            f"Saving switch event ({arrow.get(ev.timestamp).format('YYYY-MM-DD HH:mm:SS')})"
                        )
                        update_stats(f, ev)
                    start_offset = fwd.last_offset_index
                    if not fwd.forwarding_events:
                        break

        while not self.stopped():
            func()
            sleep(30)
