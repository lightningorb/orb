# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-10 08:11:54
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-08-07 12:29:47

from collections import defaultdict
import json
from orb.misc.decorators import db_connect
from orb.store.db_meta import path_finding_db_name

from orb.ln import Ln


def get_payments():
    from orb.store import model

    return model.Payment().select()


def print_logs():
    ln = Ln()
    payments = get_payments()
    for r in payments.iterator():
        if not r.succeeded:
            continue
        print("=====================")
        print(f"Payment of {r.amount} to {ln.get_node_alias(r.dest)}")
        print(r.amount, r.dest, r.fees, r.succeeded)
        for a in r.attempts:
            print("----------")
            print("Attempt:")
            prev = None
            for h in a.hops:
                if prev:
                    print(f"{ln.get_node_alias(prev.pk)} -> {ln.get_node_alias(h.pk)}")
                prev = h
            if a.succeeded:
                print("SUCCESS!")
            else:
                print(
                    f"Failed with code: {a.code} at"
                    f" {ln.get_node_alias(a.weakest_link_pk)}"
                )


def export(path):
    payments = []
    hops = []
    for r in get_payments().iterator():
        if not r.succeeded:
            continue
        attempts = []
        for a in r.attempts:
            hops = []
            for h in a.hops:
                data = h.__data__
                del data["id"]
                del data["attempt"]
                hops.append(dict(data=data))
            data = a.__data__
            del data["id"]
            del data["payment"]
            attempts.append(dict(data=data, hops=hops))
        data = r.__data__
        del data["id"]
        payments.append(dict(data=data, attempts=attempts))
    with open(path, "w") as f:
        f.write(json.dumps(payments, indent=4))
    print(f"exported to: {path}")


def ingest(path):
    from orb.store import model

    print(f"Ingesting {path}")

    with open(path, "r") as f:
        payments = json.loads(f.read())
        for p in payments:
            payment = model.Payment(**p["data"])
            payment.save()
            for a in p["attempts"]:
                attempt = model.Attempt(**a["data"], payment=payment)
                attempt.save()
                for h in a["hops"]:
                    hop = model.Hop(**h["data"], attempt=attempt)
                    hop.save()
    print("Ingestion done. Re-open the Rankings window.")


@db_connect(path_finding_db_name)
def count_successes_failures():
    ln = Ln()
    payments = get_payments()
    nodes = defaultdict(lambda: dict(successes=0, failures=0))
    remote_pubkeys = set([x.remote_pubkey for x in Ln().get_channels()])
    for r in payments.iterator():
        if not r.succeeded:
            continue
        for a in r.attempts.iterator():
            if a.succeeded:
                for hop in a.hops.iterator():
                    nodes[hop.pk]["successes"] += 1
            elif a.code == 15:
                nodes[a.weakest_link_pk]["failures"] += 1

    rank_without_direct_peers = {
        pk: nodes[pk] for pk in nodes if pk not in remote_pubkeys
    }

    sorted_by_successes = sorted(
        [
            [
                f"{ln.get_node_alias(node)} {node[:10]}",
                rank_without_direct_peers[node]["successes"],
                rank_without_direct_peers[node]["failures"],
                node,
            ]
            for node in rank_without_direct_peers
        ],
        key=lambda x: x[1],
        reverse=True,
    )

    pks = {x[0]: x[-1] for x in sorted_by_successes}
    sorted_by_successes = [x[:-1] for x in sorted_by_successes]
    return pks, sorted_by_successes


def ingest_db(path):
    pass
