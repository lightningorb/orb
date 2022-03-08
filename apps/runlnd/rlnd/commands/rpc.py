import time
import codecs, grpc, os
from collections import Counter

from functools import lru_cache
import base64
from invoke import task
from simple_chalk import *
from routes import Routes
from output import *
from routable import Routable
import schemas
from invoices import Invoices
import json
from time import sleep
from random import choice


def hex_string_to_bytes(hex_string):
    decode_hex = codecs.getdecoder("hex_codec")
    return decode_hex(hex_string)[0]


@lru_cache(maxsize=None)
def get_alias(pub_key):
    node_info_req = ln.NodeInfoRequest(pub_key=pub_key, include_channels=False)
    return stub.GetNodeInfo(node_info_req, metadata=[("macaroon", macaroon)]).node.alias


from lnd import Lnd

lnd = Lnd(os.path.expanduser("~/.lnd"), "3.1.73.28:10009", "mainnet")
output = Output(lnd)

routable = Routable(lnd=lnd, dev_mode=False)


def get_failure_source_pubkey(response, route):
    if response.failure.failure_source_index == 0:
        failure_source_pubkey = route.hops[-1].pub_key
    else:
        failure_source_pubkey = route.hops[
            response.failure.failure_source_index - 1
        ].pub_key
    return failure_source_pubkey


def handle_error(output, response, route, routes, pk=None):
    code = response.failure.code
    failure_source_pubkey = get_failure_source_pubkey(response, route)
    if code == 15:
        output.print_line(format_warning("Temporary channel failure"))
        routes.ignore_edge_on_route(failure_source_pubkey, route)
        if pk == failure_source_pubkey:
            return "Temporary channel failure"
    elif code == 18:
        output.print_line(format_warning("Unknown next peer"))
        routes.ignore_edge_on_route(failure_source_pubkey, route)
        if pk == failure_source_pubkey:
            return "Unknown next peer"
    elif code == 12:
        output.print_line(format_warning("Fee insufficient"))
        if pk == failure_source_pubkey:
            return "Fee insufficient"
    elif code == 14:
        output.print_line(format_warning("Channel disabled"))
        routes.ignore_edge_on_route(failure_source_pubkey, route)
        if pk == failure_source_pubkey:
            return "Channel disabled"
    elif code == 13:
        output.print_line(format_warning("Incorrect CLTV expiry"))
        routes.ignore_edge_on_route(failure_source_pubkey, route)
        if pk == failure_source_pubkey:
            return "Incorrect CLTV expiry"
    else:
        output.print_line(format_error(f"Unknown error code {repr(code)}:"))
        output.print_line(format_error(repr(response)))
        if pk == failure_source_pubkey:
            return f"Unknown error code {repr(code)}:"


@task
def probe(c, pk):

    amount = 100_000
    payment_request = lnd.generate_invoice("test", amount)
    orig_pay_hash = payment_request.payment_hash
    payment_request.payment_hash = "a" * len(payment_request.payment_hash)

    successes = []
    failures = []

    peers = set(lnd.get_node_channels_pubkeys(pk))
    # if len(peers) > 100:
    #     print("Too many peers - skipping")
    #     return (None, None, 0)
    fee_limit_msat = 5_000 * (1_000_000 / amount) * 1_000

    for peer_pk in peers:
        for a, b in ((peer_pk, pk), (pk, peer_pk)):
            routes = Routes(
                lnd=lnd,
                outgoing_chan_id=None,
                pub_key=a,
                payment_request=payment_request,
                last_hop_pubkey=b,
                fee_limit_msat=fee_limit_msat,
                output=output,
            )

            print(blue("-" * 50))
            print(cyan(f"Probing: {lnd.get_node_alias(b)} -> {lnd.get_node_alias(a)}"))

            succeeded = False
            reason = "no route"
            while routes.has_next():
                route = routes.get_next()
                print(f"Route")
                for j, hop in enumerate(route.hops):
                    print(f"{green(j):<5}:        {lnd.get_node_alias(hop.pub_key)}")
                response = lnd.send_payment(payment_request, route)
                if response.failure.code == 1:
                    succeeded = True
                    print(
                        "SUCCESS"
                    )  # unknown or incorrect payment details - basically it worked
                    successes.append(
                        f"{lnd.get_node_alias(b)} -> {lnd.get_node_alias(a)}"
                    )
                    break
                else:
                    my_failure_reason = handle_error(output, response, route, routes, b)
                    if my_failure_reason:
                        reason = my_failure_reason

            if not succeeded:
                failures.append(
                    f"{lnd.get_node_alias(b)} -> {lnd.get_node_alias(a)}: {reason}"
                )

    print(cyan("-" * 50))
    print(cyan("-" * 50))
    print("The following channels were successes:")
    for s in successes:
        print(green(s))
    print(cyan("-" * 50))
    print(cyan("-" * 50))
    print("The following channels were failures:")
    for f in failures:
        print(red(f))
    print(cyan("-" * 50))
    success_rate = (len(successes) / 2) / len(peers) * 100
    print(f"Success rate for 1M probes: {success_rate}%")
    print(f"Fee-rate used (sats): 丰{int(fee_limit_msat/1000):,}")
    print(cyan("-" * 50))
    lnd.cancel_invoice(orig_pay_hash)
    return (pk, success_rate, lnd.get_node_alias(pk))


@task
def rank(c):
    pks = [
        "03bb88ccc444534da7b5b64b4f7b15e1eccb18e102db0e400d4b9cfe93763aa26d",
        "02dfdcca40725ca204eec5d43a9201ff13fcd057c369c058ce4f19e5c178da09f3",
        "0309bd6a02c71f288977b15ec3ac7283cfdd3d17dde65732981d5a718aa5fb0ebc",
        "02b686ccf655ece9aec77d4d80f19bb9193f7ce224ab7c8bbe72feb3cdd7187e01",
        "03c262d20edcf2acd25bc70139097bd7af3a4f691a178b8a88c9f52109d3cb6269",
        "037659a0ac8eb3b8d0a720114efc861d3a940382dcfa1403746b4f8f6b2e8810ba",
        "0242a4ae0c5bef18048fbecf995094b74bfb0f7391418d71ed394784373f41e4f3",
        "031015a7839468a3c266d662d5bb21ea4cea24226936e2864a7ca4f2c3939836e0",
        "02644f80b5d32ed9a9888690571159692a17d7ead7db2df5124a8e2a72a8447d30",
        "025f1456582e70c4c06b61d5c8ed3ce229e6d0db538be337a2dc6d163b0ebc05a5",
        "03271338633d2d37b285dae4df40b413d8c6c791fbee7797bc5dc70812196d7d5c",
        "0296b46141cd8baf13f3eff9bb217c5f62ce0a871886559d661af0ef422c042d4b",
        "03b75897555da10fc84c93fd1543f4e166a025582057dd58a97c029baba2deb1ab",
        "027ce055380348d7812d2ae7745701c9f93e70c1adeb2657f053f91df4f2843c71",
        "02816caed43171d3c9854e3b0ab2cf0c42be086ff1bd4005acc2a5f7db70d83774",
        "03bec0f5799c4ae2d0fa8943f089324bddd6cbbbb6178f7ac2f2588696280e6587",
        "0340796fc55aec99d8f142659cd67e19080100a98ea14e8916525789b57e054eb3",
        "03fb822818be083e0a954db85257a2911a3d55458b8c1ea4124b157e865a836d12",
        "039edc94987c8f3adc28dab455efc00dea876089a120f573bd0b03c40d9d3fb1e1",
        "026165850492521f4ac8abd9bd8088123446d126f648ca35e60f88177dc149ceb2",
        "02572c2e1b43a78bb060e7d322b033443efc0d8d60fc2b111dd8bb999aa940d1f5",
        "03ac80cae732282e57f23c8c5dc5ae5dd86a77dcb378213c36cecfd28a2aa04339",
    ]

    ranks = []
    for pk in pks:
        ranks.append(probe(c, pk))

    print(ranks)

    for r in sorted(ranks, key=lambda x: x[1]):
        print(r)


@task
def decode_request(c, req: str):
    print(lnd.decode_request(req).payment_hash)


def get_failure_source_pubkey(response, route):
    if response.failure.failure_source_index == 0:
        failure_source_pubkey = route.hops[-1].pub_key
    else:
        failure_source_pubkey = route.hops[
            response.failure.failure_source_index - 1
        ].pub_key
    return failure_source_pubkey


def get_low_inbound_peer(avoid):
    chans = []
    channels = lnd.get_channels(active_only=True)
    for chan in channels:
        print(red("chan.remote_balance: "), green(f"{chan.remote_balance:,}"))
        if (chan.remote_balance + 1e6) / chan.capacity < 0.5:
            if chan.chan_id in [*avoid.keys()]:
                avoid[chan.chan_id] += 1
                if avoid[chan.chan_id] > 5:
                    del avoid[chan.chan_id]
                else:
                    continue
            alias = lnd.get_node_alias(chan.remote_pubkey)
            if alias in ["LOOP"]:
                continue
            chans.append(chan)
    if chans:
        return choice(chans)


avoid = Counter()


@task
def pay(c, env=dict(PATH=os.environ["PATH"])):
    avoid = Counter()
    while True:
        print("loading invoices")
        invs = Invoices(lnd)
        print("loaded")
        inv = invs.get_invoice()
        if not inv:
            print("no more invoies")
            return
        if inv:
            peer = get_low_inbound_peer(avoid)
            if peer:
                print(lnd.get_node_alias(peer.remote_pubkey))
                payment_request = lnd.decode_request(inv)
                routes = Routes(
                    lnd=lnd,
                    pub_key=payment_request.destination,
                    payment_request=payment_request,
                    outgoing_chan_id=peer.chan_id,
                    last_hop_pubkey=None,
                    fee_limit_msat=(
                        1_000 * (1_000_000 / payment_request.num_satoshis) * 1_000
                    ),
                    output=output,
                )

                start = time.time()

                attempts = []

                has_next = False

                while routes.has_next():
                    has_next = True
                    route = routes.get_next()

                    paths = []
                    for h in route.hops:
                        p = schemas.Path(
                            alias="",
                            pk=h.pub_key,
                            rate=int(h.fee * (1e6 / payment_request.num_satoshis)),
                            fee=h.fee,
                            succeeded=False,
                        )
                        paths.append(p)

                    for j, hop in enumerate(route.hops):
                        print(
                            f"{green(j):<5}:        {lnd.get_node_alias(hop.pub_key)}"
                        )

                    try:
                        response = lnd.send_payment(payment_request, route)
                    except:
                        invs.set_paid(inv)
                        break

                    is_successful = response.failure.code == 0

                    attempt = schemas.Attempt(
                        path=paths,
                        code=response.failure.code,
                        weakest_link="",
                        weakest_link_pk="",
                        succeeded=is_successful,
                    )

                    attempts.append(attempt)

                    if is_successful:
                        print("SUCCESS")
                        invs.set_paid(inv)
                        # log = schemas.Log(
                        #     tokens=payment_request.num_satoshis,
                        #     dest=lnd.get_info().identity_pubkey,
                        #     attempts=attempts,
                        #     failed_attempts=attempts[:-1],
                        #     succeeded_attempt=attempts[-1] if is_successful else None,
                        #     succeeded=is_successful,
                        #     log_id="",
                        #     fee=route.total_fees,
                        #     paid=payment_request.num_satoshis,
                        #     preimage="",
                        #     relays=[],
                        #     success=[],
                        #     latency=int((time.time() - start) * 1000),
                        # )
                        # fn = routable.ingest(log)
                        # output.print_line("")
                        # output.print_line("Routable.space ingest:")
                        # output.print_line(fn, end="  ")
                        # output.print_line(f"https://routable.space/log/{fn}")
                        break
                    else:
                        attempt.weakest_link_pk = get_failure_source_pubkey(
                            response, route
                        )
                        handle_error(output, response, route, routes)

                if not has_next:
                    print("No routes found!")
                    sleep(2)
                    print(f"adding {peer.chan_id} to avoid list")
                    avoid[peer.chan_id] += 1
            else:
                print("No channels left to rebalance")
                sleep(60)
