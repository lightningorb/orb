# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-01-30 17:01:24
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-01-30 17:01:54

from orb.lnd import Lnd
from threading import Thread


def download_forwarding_history(*args, **kwargs):
    def func():
        from orb.store import model

        last = model.ForwardEvent.select().order_by(
            model.ForwardEvent.timestamp_ns.desc()
        )
        if last:
            last = last.first()
        i = 0
        start_time = int(last.timestamp) if last else None
        while True:
            fwd = Lnd().get_forwarding_history(
                start_time=start_time, index_offset=i, num_max_events=100
            )

            for j, f in enumerate(fwd.forwarding_events):
                if j == 0 and start_time:
                    # if this is not the first run, then skip the first
                    # event, else it will show up as a duplicate
                    continue

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
            i += 100
            if not fwd.forwarding_events:
                break

    Thread(target=func).start()
