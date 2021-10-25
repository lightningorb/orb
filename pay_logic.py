from routes import Routes
from ui_actions import console_output
import data_manager
from traceback import print_exc

class PaymentStatus:
    success = 0
    exception = 1
    failure = 2
    no_routes = 3
    error = 4
    none = 5
    max_paths_exceeded = 6

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

def pay_thread(inst, thread_n, fee_rate, payment_request, payment_request_raw, outgoing_chan_id, last_hop_pubkey, max_paths):
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
    while routes.has_next():
        if count > max_paths:
            return payment_request_raw, outgoing_chan_id, PaymentStatus.max_paths_exceeded
        count += 1
        has_next = True
        route = routes.get_next()
        if route:
            for j, hop in enumerate(route.hops):
                node_alias = data_manager.data_man.lnd.get_node_alias(
                    hop.pub_key
                )
                text = f"{j:<5}:        {node_alias}"
                console_output(f'T{thread_n}: {text}')
        try:
            response = data_manager.data_man.lnd.send_payment(
                payment_request, route
            )
        except:
            console_output(f'T{thread_n}: {str(print_exc())}')
            console_output(f"T{thread_n}: exception - removing invoice")
            return payment_request_raw, outgoing_chan_id, PaymentStatus.exception
        is_successful = response and response.failure.code == 0
        if is_successful:
            console_output(f"T{thread_n}: SUCCESS")
            return payment_request_raw, outgoing_chan_id, PaymentStatus.success
        else:
            handle_error(inst, response, route, routes)
    if not has_next:
        console_output(f"T{thread_n}: No routes found!")
        return payment_request_raw, outgoing_chan_id, PaymentStatus.no_routes
    return payment_request_raw, outgoing_chan_id, PaymentStatus.none
