from orb.logic.routes import Routes
from orb.misc.ui_actions import console_output
import data_manager
from traceback import print_exc
import arrow


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


def handle_error(inst, response, route, routes, pk=None):
    if response:
        code = response.failure.code
        failure_source_pubkey = get_failure_source_pubkey(response, route)
    else:
        code = -1000
        failure_source_pubkey = route.hops[-1].pub_key
    if code == 15:
        console_output("Temporary channel failure")
        routes.ignore_edge_on_route(failure_source_pubkey, route)
        if pk == failure_source_pubkey:
            return "Temporary channel failure"
    elif code == 18:
        console_output("Unknown next peer")
        routes.ignore_edge_on_route(failure_source_pubkey, route)
        if pk == failure_source_pubkey:
            return "Unknown next peer"
    elif code == 12:
        console_output("Fee insufficient")
        if pk == failure_source_pubkey:
            return "Fee insufficient"
    elif code == 14:
        console_output("Channel disabled")
        routes.ignore_edge_on_route(failure_source_pubkey, route)
        if pk == failure_source_pubkey:
            return "Channel disabled"
    elif code == 13:
        console_output("Incorrect CLTV expiry")
        routes.ignore_edge_on_route(failure_source_pubkey, route)
        if pk == failure_source_pubkey:
            return "Incorrect CLTV expiry"
    elif code == -1000:
        console_output("Timeout")
        routes.ignore_edge_on_route(failure_source_pubkey, route)
        if pk == failure_source_pubkey:
            return "Timeout"
    else:
        console_output(f"Unknown error code {repr(code)}:")
        console_output(repr(response))
        if pk == failure_source_pubkey:
            return f"Unknown error code {repr(code)}:"


def pay_thread(
    inst,
    thread_n,
    fee_rate,
    payment_request,
    outgoing_chan_id,
    last_hop_pubkey,
    max_paths,
):
    from orb.store import model

    print(f"starting payment thread {thread_n} for chan: {outgoing_chan_id}")
    fee_limit_sat = fee_rate * payment_request.num_satoshis / 1_000_000
    fee_limit_msat = fee_limit_sat * 1_000
    console_output(f'fee_limit_sat: {fee_limit_sat}')
    console_output(f'fee_limit_msat: {fee_limit_msat}')
    routes = Routes(
        lnd=data_manager.data_man.lnd,
        pub_key=payment_request.destination,
        payment_request=payment_request,
        outgoing_chan_id=outgoing_chan_id,
        last_hop_pubkey=last_hop_pubkey,
        fee_limit_msat=fee_limit_msat,
        inst=inst,
    )
    has_next = False
    count = 0
    payment = model.Payment(
        amount=payment_request.num_satoshis,
        dest=payment_request.destination,
        fees=0,
        succeeded=False,
        timestamp=int(arrow.now().timestamp()),
    )
    while routes.has_next():
        if count > max_paths:
            return PaymentStatus.max_paths_exceeded
        count += 1
        has_next = True
        route = routes.get_next()
        payment.save()
        if route:
            attempt = model.Attempt(
                payment=payment, weakest_link_pk='', code=0, succeeded=False
            )
            attempt.save()
            for j, hop in enumerate(route.hops):
                node_alias = data_manager.data_man.lnd.get_node_alias(hop.pub_key)
                text = f"{j:<5}:        {node_alias}"
                console_output(f'T{thread_n}: {text}')
                # no actual need for hops for now
                p = model.Hop(pk=hop.pub_key, succeeded=False, attempt=attempt)
                p.save()
            try:
                response = data_manager.data_man.lnd.send_payment(
                    payment_request, route
                )
            except Exception as e:
                code = e.args[0].code.name
                details = e.args[0].details
                # 'attempted value exceeds paymentamount'
                if (
                    code == 'UNKNOWN'
                    and details == 'attempted value exceeds paymentamount'
                ):
                    console_output(f'T{thread_n}: INVOICE CURRENTLY INFLIGHT')
                    return PaymentStatus.inflight
                if code == 'ALREADY_EXISTS' and details == 'invoice is already paid':
                    console_output(f'T{thread_n}: INVOICE IS ALREADY PAID')
                    return PaymentStatus.already_paid
                console_output(f"T{thread_n}: exception.. not sure what's up")
                return PaymentStatus.exception
            is_successful = response and response.failure.code == 0
            if is_successful:
                console_output(f"T{thread_n}: SUCCESS")
                attempt.succeeded = True
                payment.succeeded = True
                payment.fees = route.total_fees
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
                attempt.save()
                handle_error(inst, response, route, routes)
    if not has_next:
        console_output(f"T{thread_n}: No routes found!")
        return PaymentStatus.no_routes
    console_output('No more routes found.')
    return PaymentStatus.none
