import requests
import arrow
import re
import json
import string
from collections import namedtuple
from collections import defaultdict
from collections import Counter
import os
from glob import glob
import sys
from functools import cmp_to_key
import random
from invoke import task
from datetime import timedelta

PUBKEY = "0243d1c24e3a76cbdd661e56b71e7eeffd06ef5ac6179a28020be1d9414d0560a7"

Path = namedtuple("Path", "alias pk rate fee code")


class Attempt:
    def __init__(self, path, weakest_link, succeeded):
        self.path = path
        self.weakest_link = weakest_link
        self.weakest_link_pk = None
        self.succeeded = succeeded

    def __repr__(self):
        return f"{str(self.path)}, weakest link: {self.weakest_link}, succeeded: {self.succeeded}"


utf8 = lambda s: "".join(x for x in s if x in string.printable)


@task
def parse_log(c, log_file):
    res = parse_log_file(log_file)
    print(res)


def parse_log_file(log_file):
    with open(log_file) as f:
        attempts = []
        avoid, dest, dest_pk, tokens, header_done = "", "", "", 0, False
        start_eval = False
        paths = []
        code = None
        for l in f.readlines():
            l = (
                l.replace("", "")
                .replace("[90m", "")
                .replace("[39m", "")
                .replace("[92m", "")
            )
            # print(l, end="")
            if not header_done:
                if l.startswith("avoiding_tag: "):
                    avoid = l
                elif l.startswith("description: "):
                    dest = l[len("description: ") : -1]
                elif l.startswith("destination: "):
                    dest_pk = l[len("destination: ") : -1]
                elif l.startswith("tokens:      "):
                    tokens = int(l[len("tokens:      ") : -1])
                    header_done = True
                    # print(dest, dest_pk, tokens)
            if l == "evaluating: \n":
                start_eval = True
            elif start_eval and l == "\n":
                start_eval = False
                attempts.append(
                    Attempt(path=paths[:], weakest_link=None, succeeded=True)
                )
                paths[:] = []
            elif start_eval:
                m = re.search(r"(\d+x\d+x\d+)", l)
                if m:
                    code = m.groups()[0]
                m = re.search(
                    r"  - (.*) ([0-9 a-z]{66}). Fee rate: ([^ ]+)% \((\d+)\)", l
                )
                if m:
                    alias, pk, rate, fee = m.groups()
                    paths.append(Path(alias, pk, float(rate), int(fee), code))
            elif "failure: TemporaryChannelFailure" in l:
                failure_code, failure = re.search(
                    r"failure: TemporaryChannelFailure at (\d+x\d+x\d+) from (.*)", l
                ).groups()
                attempts[-1].weakest_link = failure
                attempts[-1].weakest_link_pk = next(
                    iter([x.pk for x in attempts[-1].path if x.code == failure_code]),
                    attempts[-1].path[-1].pk,
                )
                print("-" * 20)
                print(attempts[-1].weakest_link_pk)
                print(failure)
                attempts[-1].succeeded = False

        payment_succeeded = attempts and attempts[-1].succeeded == True
        failed_attempts = attempts[:-1] if payment_succeeded else attempts
        succeeded_attempt = attempts[-1] if payment_succeeded else None

        return (
            tokens,
            dest,
            dest_pk,
            failed_attempts,
            succeeded_attempt,
        )


def load_table():
    if os.path.exists("table.json"):
        with open("table.json") as f:
            return json.load(f)
    return {}


@task
def probe(c):
    while True:
        with open("graph.json") as f:
            j = json.loads(f.read())
            nodes, edges = j["nodes"], j["edges"]
            while True:
                node = random.choice(nodes)
                last_update = arrow.get(node["last_update"])
                print(arrow.utcnow() - last_update)
                if arrow.utcnow() - last_update < timedelta(days=1):
                    break
                print("too old")
            print(f"probing: {node['alias']}")
            out = c.run(f'bos probe {node["pub_key"]} 1000000 --no-color').stdout
            with open("probe.log", "w") as f:
                f.write(out)
            # tokens, dest, dest_pk, attempts, success = parse_log_file(log)
            # get_rankings("probe.log")
            res = get_rankings(c, "probe.log")
            resj = load_table()
            for r in res:
                alias, pk, failures, successes, ratio = r
                if pk in resj:
                    resj[pk]["alias"] = alias
                    resj[pk]["failures"] += failures
                    resj[pk]["successes"] += successes
                    resj[pk]["ratio"] = resj[pk]["successes"] / (
                        resj[pk]["failures"] + resj[pk]["successes"]
                    )
                else:
                    resj[pk] = dict(
                        alias=alias,
                        failures=failures,
                        successes=successes,
                        ratio=(successes / (successes + failures)),
                    )
            with open("table.json", "w") as f:
                f.write(json.dumps(resj, indent=4))


@task
def get_rankings(c, log_file=""):
    from glob import glob
    from tabulate import tabulate

    with open("graph.json") as f:
        j = json.loads(f.read())
        nodes, edges = j["nodes"], j["edges"]
        aliases = {n["pub_key"]: utf8(n["alias"]) for n in nodes}

    count = defaultdict(lambda: {"fail": 0, "succeed": 0})
    for log in [log_file] if log_file else glob("data/*.log"):
        tokens, dest, dest_pk, attempts, success = parse_log_file(log)
        for a in attempts:
            if a.weakest_link_pk:
                count[a.weakest_link_pk]["fail"] += 1
        if success:
            for p in success.path:
                count[p.pk]["succeed"] += 1
    table = []
    for k, v in count.items():
        table.append(
            [
                aliases[k],
                k,
                v["fail"],
                v["succeed"],
                round(v["succeed"] / (v["fail"] + v["succeed"]), 1),
            ]
        )

    def cmp(a, b):
        a = a[1:][::-1]
        b = b[1:][::-1]
        if a == b:
            return 0
        if a < b:
            return -1
        if a > b:
            return 1

    table.sort(key=cmp_to_key(cmp), reverse=True)
    print(tabulate(table, headers=["Peer", "pk", "Failures", "Successes", "Ratio"]))
    # print(success)
    # for entry in table:
    #     peer, failures, successes, ratio = entry
    #     if ratio < 0.1 and failures > 10:
    #         print(f"bos tags {ratio} --add {peer}")
    return table


@task
def draw_payment_graph(c, log_file):
    import matplotlib.pyplot as plt
    import networkx as nx

    tokens, dest, dest_pk, attempts, _ = parse_log_file(log_file)

    print(f"Attempts: {len(attempts)}")

    G = nx.Graph()
    edge_added = set([])

    with open("graph.json") as f:
        j = json.loads(f.read())
        nodes, edges = j["nodes"], j["edges"]
        aliases = {n["pub_key"]: utf8(n["alias"]) for n in nodes}
        for e in edges:
            n1, n2 = [e["node1_pub"], e["node2_pub"]]
            if PUBKEY in [n1, n2]:
                other = next(iter(set([n1, n2]) - set([PUBKEY])))
                G.add_edge(aliases[PUBKEY], aliases[other], weight=1)

        for a in attempts:
            prev = None
            for p in a:
                if prev:
                    if (aliases[p.pk], prev) not in edge_added:
                        G.add_edge(aliases[p.pk], prev, weight=1)
                        edge_added.add((prev, dest))
                prev = aliases[p.pk]
            if (prev, dest) not in edge_added:
                G.add_edge(prev, dest, weight=1)

    pos = nx.spring_layout(G, seed=7)
    figure = plt.gcf()
    figure.set_size_inches(2880 / 200, 1500 / 200)
    nx.draw_networkx_nodes(G, pos, node_size=80)
    nx.draw_networkx_edges(G, pos, width=1)
    nx.draw_networkx_labels(G, pos, font_size=10, font_family="sans-serif")
    ax = plt.gca()
    ax.margins(0.08)
    ax.set_title(f"Payment for: {int(tokens):,} via: {attempts[0][0].alias} to: {dest}")
    plt.axis("off")
    plt.tight_layout()
    idir = f"data/img/{aliases[attempts[0][0].pk]}"
    if not os.path.isdir(idir):
        os.mkdir(idir)
    path = f"{idir}/{os.path.splitext(os.path.basename(log_file))[0]}.jpg"
    plt.savefig(path, dpi=200)
