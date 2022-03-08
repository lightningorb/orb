# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-01-21 10:52:31
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-01-21 11:06:44
import sys
from collections import namedtuple
from collections import Counter
from invoke import task
from os import path
import json
import os
import arrow
import time
import operator
from simple_chalk import *

get_conf_dir = lambda: path.normpath(path.join(path.dirname(__file__), "..", "confs"))
get_conf_file_path = lambda x: path.join(get_conf_dir(), x)


@task
def resources(c, env=dict(PATH=os.environ["PATH"])):
    """
    List a bunch of very useful external resources, to improve your node's
    ranking.
    """
    info = json.loads(c.run("lncli getinfo", hide=True, env=env).stdout)
    oneml = f"https://1ml.com/node/{info['identity_pubkey']}"

    import urwid
    import urwid.raw_display

    blank = urwid.Divider()

    def main():
        text_header = (
            f"{info['alias']}  UP / DOWN / PAGE UP / PAGE DOWN scroll.  F8 exits."
        )

        def button_press(button):
            frame.footer = urwid.AttrWrap(
                urwid.Text(["Pressed: ", button.get_label()]), "header"
            )

        radio_button_group = []

        listbox_content = [
            blank,
            urwid.Padding(urwid.Text([f"This is an experimental UI."])),
            blank,
            urwid.Padding(urwid.Text([f"lnd version: {info['version']}"])),
            blank,
            urwid.Padding(
                urwid.Text([f"Public Key Identity: {info['identity_pubkey']}"])
            ),
            blank,
            urwid.Padding(
                urwid.Text([f"Pending channels: {info['num_pending_channels']}"])
            ),
            urwid.Padding(
                urwid.Text([f"Active channels: {info['num_active_channels']}"])
            ),
            urwid.Padding(
                urwid.Text([f"Inactive channels: {info['num_inactive_channels']}"])
            ),
            urwid.Padding(urwid.Text([f"Peers: {info['num_peers']}"])),
            blank,
            urwid.Padding(
                urwid.Text(
                    [
                        ("important", oneml),
                        f"Good place to get started, to become visible to the network."
                        f" We recommend opening a 200k satoshis channel with them.",
                    ]
                ),
                left=2,
                right=2,
                min_width=20,
            ),
            blank,
            urwid.Padding(
                urwid.Text(
                    [
                        "Excellent place to give you actionable feedback to improve"
                        " your node's ranking ",
                        (
                            "important",
                            f"https://terminal.lightning.engineering/#/{info['identity_pubkey']}",
                        ),
                    ]
                ),
                left=2,
                right=2,
                min_width=20,
            ),
            blank,
            urwid.Padding(
                urwid.Text(
                    [
                        "Provides you with a ton of information about your node, and"
                        " channels ",
                        (
                            "important",
                            f"https://amboss.space/node/{info['identity_pubkey']}",
                        ),
                    ]
                ),
                left=2,
                right=2,
                min_width=20,
            ),
            blank,
            urwid.Padding(
                urwid.Text(
                    [
                        "Get insights in to your Terminal score and improve your"
                        " ranking. ",
                        (
                            "important",
                            f"https://lnrouter.app/scores/terminal?id={info['identity_pubkey']}",
                        ),
                    ]
                ),
                left=2,
                right=2,
                min_width=20,
            ),
            blank,
            urwid.Padding(
                urwid.Text(
                    [
                        "Creates a great chart, and simulates changes to centrality"
                        " when connecting to other peers ",
                        (
                            "important",
                            f"https://lnnodeinsight.com/?peer_network={info['alias']}",
                        ),
                    ]
                ),
                left=2,
                right=2,
                min_width=20,
            ),
            blank,
            urwid.Padding(
                urwid.Text(
                    [
                        "Find nodes to connect to ",
                        (
                            "important",
                            f"https://gridflare.xyz/explore/node/{info['identity_pubkey']}",
                        ),
                    ]
                ),
                left=2,
                right=2,
                min_width=20,
            ),
            blank,
            urwid.Padding(
                urwid.Text(
                    [
                        "Explore worldmap of nodes ",
                        (
                            "important",
                            f"https://explorer.acinq.co/n/{info['identity_pubkey']}",
                        ),
                    ]
                ),
                left=2,
                right=2,
                min_width=20,
            ),
        ]

        header = urwid.AttrWrap(urwid.Text(text_header), "header")
        listbox = urwid.ListBox(urwid.SimpleListWalker(listbox_content))
        frame = urwid.Frame(urwid.AttrWrap(listbox, "body"), header=header)

        palette = [
            ("body", "black", "light gray", "standout"),
            ("reverse", "light gray", "black"),
            ("header", "white", "dark red", "bold"),
            ("important", "dark blue", "light gray", ("standout", "underline")),
            ("editfc", "white", "dark blue", "bold"),
            ("editbx", "light gray", "dark blue"),
            ("editcp", "black", "light gray", "standout"),
            ("bright", "dark gray", "light gray", ("bold", "standout")),
            ("buttn", "black", "dark cyan"),
            ("buttnf", "white", "dark blue", "bold"),
        ]

        def unhandled(key):
            if key == "f8":
                raise urwid.ExitMainLoop()

        urwid.MainLoop(frame, palette, unhandled_input=unhandled).run()

    main()


@task()
def suez(c, env=dict(PATH=os.environ["PATH"])):
    """
    Run the suez app from src/suez
    to find out more: https://github.com/prusnak/suez
    """
    with c.cd("~/src/suez"):
        c.run("poetry run ./suez", env=env, pty=True)


@task()
def stream_htlcs(c, env=dict(PATH=os.environ["PATH"])):
    with c.cd("~/src/stream-lnd-htlcs"):
        c.run("python3 ./stream-lnd-htlcs.py --stream-mode true", env=env)


@task(
    help=dict(
        from_path="the source path, on remote host",
        to_path="the dest path, on local host",
    )
)
def get(c, from_path, to_path):
    """
    Transfer a file from remote to local
    """

    c.get(from_path, to_path)


@task
def update_fees(c, env={"PATH": os.environ["PATH"]}):
    """
    Run a fee update with policy on every channel
    """
    from tabulate import tabulate

    lerp = lambda a, b, t: a + (b - a) * t
    table = []

    set_fees = {
        "021c97a90a411ff2b10dc2a8e32de2f29d2fa49d41bfbb52bd416e460db0747d0d": 1100
    }

    channels = json.loads(c.run("lncli listchannels", hide=True, env=env).stdout)
    peers = json.loads(c.run("lncli listpeers", hide=True, env=env).stdout)
    print("Updating fees: ", end="")
    for chan in channels["channels"]:
        lb, rb = int(chan["local_balance"]), int(chan["remote_balance"])
        ca = lb + rb
        print(".", end="")
        sys.stdout.flush()
        pk = chan["remote_pubkey"]
        if ca:
            if pk in set_fees:
                # Drains
                c.run(
                    f"""lncli updatechanpolicy --base_fee_msat 0 --fee_rate {set_fees[pk]/1e6} --time_lock_delta 40 --chan_point {chan['channel_point']}""",
                    env=env,
                    hide=True,
                )
            else:
                # everything else
                r = rb / ca
                if r <= 0.5:
                    fee_rate = 500
                    # if r <= 0.2:
                    # fee_rate = 0
                else:
                    fee_rate = int(max(0, lerp(-1500, 2000, r)))
                    if r > 0.8:
                        fee_rate = 10000

                table.append([f"{lb:,}", f"{rb:,}", f"{ca:,}", r, f"{fee_rate:,}"])

                c.run(
                    f"""lncli updatechanpolicy --base_fee_msat 0 --fee_rate {fee_rate/1e6} --time_lock_delta 40 --chan_point {chan['channel_point']}""",
                    env=env,
                    hide=True,
                )
    print("")
    print(tabulate(table, headers=["local", "remote", "cap", "ratio", "fee rate"]))


@task
def channel_balance(c):
    """
    Report on whether node liquidity is balanced
    """
    total_in, total_out, channels = (
        0,
        0,
        json.loads(c.run("lncli listchannels", hide=True).stdout),
    )
    for chan in channels["channels"]:
        total_out += int(chan["local_balance"])
        total_in += int(chan["remote_balance"])
    print(f"inbound:  {total_in:,}, outbound: {total_out:,}")
    if total_in > total_out:
        print("Inbound liquidity is higher than outbound")
    else:
        print("Outbound liquidity is higher than inbound")
    print(
        f"Please increase {['in','out'][total_in > total_out]}bound liquidity by, or"
        f" decrease {['in','out'][total_in < total_out]}bound by:"
        f" 丰{abs(total_in-total_out):,}"
    )


def save_to_log(stdout, name="bos_pay"):
    with open(
        f'data/{name}_{arrow.utcnow().format("YYYY-MM-DD_HH:mm:ss")}.log', "w"
    ) as f:
        f.write(stdout)


def get_peers(c, env, avoid, ratio, cmp):
    to_rebal = []
    channels = json.loads(c.run("lncli listchannels", hide=True, env=env).stdout)
    for chan in channels["channels"]:
        lb, rb = int(chan["local_balance"]), int(chan["remote_balance"])
        ca = lb + rb
        r = rb / ca
        pk = chan["remote_pubkey"]
        if (
            ca
            and cmp(r, ratio)
            and pk
            not in [
                "021c97a90a411ff2b10dc2a8e32de2f29d2fa49d41bfbb52bd416e460db0747d0d",
                "0277e9adedb07d04c9caae4884026d3dbda75dfb78bc10fae06c02ae8702fe1ce6",
                "02ba9508eb244215a6469bebc7c941f47d5fbd6e9b3d412c1bdb381150ce115fd0",
            ]
        ):
            if pk in avoid:
                if avoid[pk] >= 5:
                    del avoid[pk]
                else:
                    avoid[pk] += 1
            if pk not in avoid:
                alias = json.loads(
                    c.run(
                        f'lncli getnodeinfo {chan["remote_pubkey"]}', env=env, hide=True
                    ).stdout
                )["node"]["alias"]
                to_rebal.append(
                    Channel(
                        alias=alias,
                        outbound=lb,
                        inbound=rb,
                        ratio=r,
                        pk=chan["remote_pubkey"],
                    )
                )
    if to_rebal:
        return next(
            iter(sorted(to_rebal, key=lambda x: x.ratio, reverse=cmp == operator.gt)),
            None,
        )


Channel = namedtuple("Channel", "alias outbound inbound ratio pk")


@task
def rebalance(c, env=dict(PATH=os.environ["PATH"])):
    """
    Automagically rebalance channels
    """
    avoid = Counter()
    while True:
        print("getting peer 1")
        peer1 = get_peers(c, env, avoid, 0.3, operator.lt)
        print("getting peer 2")
        peer2 = get_peers(c, env, avoid, 0.7, operator.gt)
        print(peer1)
        print(peer2)
        if peer1 and peer2:
            amount = int(1e6)
            cmd = c.run(
                f"bos rebalance --out {peer1.pk} --in {peer2.pk} --max-fee-rate 500"
                f" --amount {amount}",
                warn=True,
                env=env,
            )
            out = cmd.stdout
            save_to_log(out, "bos_rebalance")
            err = cmd.stderr
            if (
                err
                or "RebalanceTotalFeeTooHigh" in out
                or "NoActiveChannelWithOutgoingPeer" in out
            ):
                avoid[peer1.pk] += 1
                avoid[peer2.pk] += 1
        else:
            print("Peers no longer need rebalancing")
            time.sleep(60)


def struct():
    struct = {"fee": 0}
    return struct


counter = 0


@task
def list_payments(c, env=dict(PATH=os.environ["PATH"])):
    """
    List lightning payments
    """
    import string

    utf8 = lambda s: "".join(x for x in s if x in string.printable)
    tmp_s = struct()
    root = tmp_s
    with open("graph.json") as f:
        j = json.loads(f.read())
        nodes, edges = j["nodes"], j["edges"]
        aliases = {n["pub_key"]: utf8(n["alias"]) for n in nodes}

    # pay = json.loads(c.run("lncli listpayments", hide=True, env=env).stdout)["payments"]
    pay = json.loads(open("data/payments.json").read())["payments"]
    for p in pay:
        print("-" * 100)
        date = arrow.get(int(p["creation_date"])).format("YYYY-MM-DD HH:mm")
        print(
            f"{date}    {p['value_sat']:<10}   {p['status']:<10}    {p['fee']:<10}   "
            f" {p['payment_hash']:<10}"
        )
        for h in p["htlcs"][0]["route"]["hops"]:
            pk = h["pub_key"]
            alias = aliases[pk]
            if alias not in tmp_s:
                tmp_s[alias] = struct()
            tmp_s[alias]["fee"] += int(
                h["fee"]
            )  # int(int(h["fee"]) / (int(p["value_sat"]) / 1e6))
            tmp_s = tmp_s[alias]
        tmp_s = root

    print(f"Num Payments {len(pay)}")

    with open("output.json", "w") as fp:
        json.dump(root, fp, indent=4)

    rt = {"root": root}

    def draw(parent_name, child_name):
        global counter
        counter += 1
        p_n = parent_name
        c_n = child_name
        graph.add_node(pydot.Node(p_n, color="blue", label=parent_name.split("_")[0]))
        graph.add_node(pydot.Node(c_n, color="green", label=child_name.split("_")[0]))
        edge = pydot.Edge(p_n, c_n)
        graph.add_edge(edge)

    def visit(node, parent=None):
        global counter
        for k, v in node.items():
            if isinstance(v, dict):
                # We start with the root node whose parent is None
                # we don't want to graph the None node
                k = str(k) + "_" + str(counter)
                if parent:
                    draw(parent, k)
                visit(v, k)
            else:
                # drawing the label using a distinct name
                v = str(v) + "_" + str(counter)
                draw(parent, v)

    graph = pydot.Dot(graph_type="digraph")
    visit(rt)
    graph.write_pdf("paytrie.pdf")


@task
def get_logs(c):
    c.local(
        "rsync -azv -e 'ssh -i ~/.rln/lnd2/lnd2_key.pem'"
        " ubuntu@54.251.191.236:/home/ubuntu/src/rln/data/*.log ."
    )
