# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-01-30 17:01:24
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-02-20 13:36:12

import arrow
from threading import Thread, Lock
from collections import defaultdict

from orb.lnd import Lnd

lock = Lock()


def download_payment_history(*_, **__):
    from orb.store import model

    def save_payment(p):
        pay = model.LNDPayment(
            creation_date=p.creation_date,
            creation_time_ns=p.creation_time_ns,
            failure_reason=p.failure_reason,  # needs getting
            fee=p.fee,
            fee_msat=p.fee_msat,
            fee_sat=p.fee_sat,
            payment_hash=p.payment_hash,
            payment_index=p.payment_index,
            payment_preimage=p.payment_preimage,
            payment_request=p.payment_request,
            status=p.status,  # needs getting
            value=p.value,
            value_msat=p.value_msat,
            value_sat=p.value_sat,
            dest_pubkey="",
            last_hop_pubkey="",
            last_hop_chanid=0,
            total_fees_msat=0,
        )
        pay.save()
        last_route = None

        for h in p.htlcs:
            attempt = model.LNDPaymentAttempt(
                attempt_id=h.attempt_id,
                attempt_time_ns=h.attempt_time_ns,
                # failure=h.failure if h.failure else "",
                preimage=h.preimage,
                resolve_time_ns=h.resolve_time_ns,
                status=h.status,
                payment=pay,
            )
            attempt.save()
            r = h.route
            route = model.LNDAttemptRoute(
                total_amt=r.total_amt,
                total_amt_msat=r.total_amt_msat,
                total_fees=r.total_fees,
                total_fees_msat=r.total_fees_msat,
                total_time_lock=r.total_time_lock,
                attempt=attempt,
            )
            route.save()

            for h in r.hops:
                last_route = r
                hop = model.LNDHop(
                    # amp_record=h.amp_record if h.amp_record else "",
                    amt_to_forward=h.amt_to_forward,
                    amt_to_forward_msat=h.amt_to_forward_msat,
                    chan_capacity=h.chan_capacity,
                    chan_id=h.chan_id,
                    custom_records=h.custom_records.toJSON()
                    if h.custom_records
                    else {},
                    expiry=h.expiry,
                    fee=h.fee,
                    fee_msat=h.fee_msat,
                    # mpp_record=h.mpp_record.toJSON() if h.mpp_record else {},
                    pub_key=h.pub_key,
                    tlv_payload=h.tlv_payload,
                    route=route,
                )
                hop.save()

        pay.dest_pubkey = last_route.hops[-1].pub_key
        if len(last_route.hops) > 1:
            pay.last_hop_pubkey = last_route.hops[-2].pub_key
            pay.last_hop_chanid = last_route.hops[-2].chan_id
            stats = (
                model.ChannelStats()
                .select()
                .where(model.ChannelStats.chan_id == last_route.hops[-2].chan_id)
            )
            if stats:
                stats = stats.first()
                stats.debt_msat += last_route.total_fees_msat
            else:
                stats = model.ChannelStats(
                    chan_id=int(last_route.hops[-2].chan_id),
                    earned_msat=last_route.total_fees_msat,
                )
            stats.save()

        pay.total_fees_msat = last_route.total_fees_msat
        pay.save()

    def payment_exists(p):
        return (
            model.LNDPayment()
            .select()
            .where(model.LNDPayment.creation_time_ns == p.creation_time_ns)
            .first()
        )

    def get_last_payment():
        return (
            model.LNDPayment()
            .select()
            .order_by(model.LNDPayment.creation_time_ns.desc())
            .first()
        )

    def clear_stats():
        stats = model.ChannelStats().select()
        if stats:
            for s in stats:
                s.debt = 0
                s.save()

    def func():
        if lock.locked():
            return
        with lock:
            chunk_size = 100
            last = get_last_payment()
            start_offset = last.payment_index if last else 0
            if start_offset == 0:
                clear_stats()
            while True:
                res = Lnd().list_payments(
                    include_incomplete=False,
                    index_offset=start_offset,
                    max_payments=chunk_size,
                    reversed=False,
                )
                for p in res.payments:
                    if payment_exists(p):
                        continue
                    print(
                        f"Saving payment event {arrow.get(p.creation_date).format('YYYY-MM-DD HH:mm:SS')}"
                    )
                    save_payment(p)
                if not res.payments:
                    break
                start_offset = res.last_index_offset

    Thread(target=func).start()
