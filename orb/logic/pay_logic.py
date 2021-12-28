# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-15 07:15:28
# @Last Modified by:   lnorb.com
# @Last Modified time: 2021-12-29 03:49:35
import json
import threading
import arrow

from orb.logic.routes import Routes
from orb.misc.forex import forex

import data_manager

lock = threading.Lock()


class PaymentStatus:
    success = 0
    exception = 1
    failure = 2
    no_routes = 3
    error = 4
    none = 5
    max_paths_exceeded = 6
    inflight = 7
    already_paid = 8


def get_failure_source_pubkey(response, route):
    if response.failure.failure_source_index == 0:
        failure_source_pubkey = route.hops[-1].pub_key
    else:
        failure_source_pubkey = route.hops[
            response.failure.failure_source_index - 1
        ].pub_key
    return failure_source_pubkey


def handle_error(response, route, routes, pk=None):
    if response:
        code = response.failure.code
        failure_source_pubkey = get_failure_source_pubkey(response, route)
    else:
        code = -1000
        failure_source_pubkey = route.hops[-1].pub_key
    if code == 15:
        print("Temporary channel failure")
        routes.ignore_edge_on_route(failure_source_pubkey, route)
        if pk == failure_source_pubkey:
            return "Temporary channel failure"
    elif code == 18:
        print("Unknown next peer")
        routes.ignore_edge_on_route(failure_source_pubkey, route)
        if pk == failure_source_pubkey:
            return "Unknown next peer"
    elif code == 12:
        print("Fee insufficient")
        if pk == failure_source_pubkey:
            return "Fee insufficient"
    elif code == 14:
        print("Channel disabled")
        routes.ignore_edge_on_route(failure_source_pubkey, route)
        if pk == failure_source_pubkey:
            return "Channel disabled"
    elif code == 13:
        print("Incorrect CLTV expiry")
        routes.ignore_edge_on_route(failure_source_pubkey, route)
        if pk == failure_source_pubkey:
            return "Incorrect CLTV expiry"
    elif code == -1000:
        print("Timeout")
        routes.ignore_edge_on_route(failure_source_pubkey, route)
        if pk == failure_source_pubkey:
            return "Timeout"
    else:
        print(f"Unknown error code {repr(code)}:")
        print(repr(response))
        if pk == failure_source_pubkey:
            return f"Unknown error code {repr(code)}:"


def pay_thread(
    stopped,
    thread_n,
    fee_rate,
    payment_request,
    outgoing_chan_id,
    last_hop_pubkey,
    max_paths,
    payment_request_raw,
):
    from orb.misc.prefs import is_rest

    func = pay_thread_rest if is_rest() else pay_thread_grpc

    return func(
        stopped=stopped,
        thread_n=thread_n,
        fee_rate=fee_rate,
        payment_request=payment_request,
        outgoing_chan_id=outgoing_chan_id,
        last_hop_pubkey=last_hop_pubkey,
        max_paths=max_paths,
        payment_request_raw=payment_request_raw,
    )


def pay_thread_grpc(
    stopped,
    thread_n,
    fee_rate,
    payment_request,
    outgoing_chan_id,
    last_hop_pubkey,
    max_paths,
    payment_request_raw,
):
    from orb.store import model

    print(f"starting payment thread {thread_n} for chan: {outgoing_chan_id}")
    fee_limit_sat = fee_rate * int(payment_request.num_satoshis) / 1_000_000
    fee_limit_msat = fee_limit_sat * 1_000
    print(f"amount: {payment_request.num_satoshis}")
    print(f"fee_limit_sat: {fee_limit_sat}")
    print(f"fee_limit_msat: {fee_limit_msat}")
    routes = Routes(
        lnd=data_manager.data_man.lnd,
        pub_key=payment_request.destination,
        payment_request=payment_request,
        outgoing_chan_id=outgoing_chan_id,
        last_hop_pubkey=last_hop_pubkey,
        fee_limit_msat=fee_limit_msat,
    )
    has_next = False
    count = 0
    payment = model.Payment(
        amount=int(payment_request.num_satoshis),
        dest=payment_request.destination,
        fees=0,
        succeeded=False,
        timestamp=int(arrow.now().timestamp()),
    )
    while routes.has_next() and not stopped():
        if count > max_paths:
            return PaymentStatus.max_paths_exceeded
        count += 1
        has_next = True
        route = routes.get_next()
        with lock:
            payment.save()
        if route:
            attempt = model.Attempt(
                payment=payment, weakest_link_pk="", code=0, succeeded=False
            )
            with lock:
                attempt.save()
                for j, hop in enumerate(route.hops):
                    node_alias = data_manager.data_man.lnd.get_node_alias(hop.pub_key)
                    text = f"{j:<5}:        {node_alias}"
                    print(f"T{thread_n}: {text}")
                    # no actual need for hops for now
                    p = model.Hop(pk=hop.pub_key, succeeded=False, attempt=attempt)
                    p.save()
            try:
                response = data_manager.data_man.lnd.send_payment(
                    payment_request, route
                )
            except Exception as e:
                print(e)
                code = e.args[0].code.name
                details = e.args[0].details
                # 'attempted value exceeds paymentamount'
                if (
                    code == "UNKNOWN"
                    and details == "attempted value exceeds paymentamount"
                ):
                    print(f"T{thread_n}: INVOICE CURRENTLY INFLIGHT")
                    return PaymentStatus.inflight
                if code == "ALREADY_EXISTS" and details == "invoice is already paid":
                    print(f"T{thread_n}: INVOICE IS ALREADY PAID")
                    return PaymentStatus.already_paid
                print(f"T{thread_n}: exception.. not sure what's up")
                return PaymentStatus.exception
            is_successful = response and (
                response.failure is None or response.failure.code == 0
            )
            if is_successful:
                print(
                    f"T{thread_n}: SUCCESS: {forex(response.route.total_amt)} (fees: {forex(response.route.total_fees)})"
                )
                attempt.succeeded = True
                payment.succeeded = True
                payment.fees = route.total_fees
                with lock:
                    for hop in attempt.hops:
                        hop.succeeded = True
                        hop.save()
                    attempt.save()
                    payment.save()
                return PaymentStatus.success
            else:
                attempt.code = response.failure.code if response else -1000
                attempt.weakest_link_pk = (
                    get_failure_source_pubkey(response, route)
                    if response
                    else route.hops[-1].pub_key
                )
                with lock:
                    attempt.save()
                handle_error(response, route, routes)
    if not has_next:
        print(f"T{thread_n}: No routes found!")
        return PaymentStatus.no_routes
    print("No more routes found.")
    return PaymentStatus.none


def pay_thread_rest(
    stopped,
    thread_n,
    fee_rate,
    payment_request,
    outgoing_chan_id,
    last_hop_pubkey,
    max_paths,
    payment_request_raw,
):
    print(f"starting payment thread {thread_n} for chan: {outgoing_chan_id}")
    fee_limit_sat = fee_rate * int(payment_request.num_satoshis) / 1_000_000
    fee_limit_msat = fee_limit_sat * 1_000
    print(f"fee_limit_sat: {fee_limit_sat}")
    print(f"fee_limit_msat: {fee_limit_msat}")
    from data_manager import data_man

    r = data_man.lnd.router_send(
        pub_key=payment_request.destination,
        amount=payment_request.num_satoshis,
        payment_request=payment_request,
        last_hop_pubkey=last_hop_pubkey,
        outgoing_chan_id=outgoing_chan_id,
        fee_limit_msat=fee_limit_msat,
        payment_request_raw=payment_request_raw,
    )

    for raw_response in r.iter_lines():
        json_response = json.loads(raw_response)
        print(json_response)
        # print(raw_response)
        if "result" in json_response:
            if json_response["result"]["status"] == "SUCCEEDED":
                return PaymentStatus.success
        elif "error" in json_response:
            if json_response["error"]["message"] == "invoice is already paid":
                return PaymentStatus.already_paid
    return PaymentStatus.none
