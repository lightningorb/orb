from __future__ import print_function, absolute_import, division
import os
import json
from invoke import task
import arrow
import requests

try:
    from urwid import *
    import json
    from collections import defaultdict
    import urwid
except:
    pass

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
        raise ExitMainLoop()


@task
def balance(c, env=dict(PATH=os.environ["PATH"])):
    info = json.loads(c.run("lncli getinfo", hide=True, env=env).stdout)
    walletbal = json.loads(c.run("lncli walletbalance", hide=True, env=env).stdout)
    chanbal = json.loads(c.run("lncli channelbalance", hide=True, env=env).stdout)
    price = requests.get("https://api.coindesk.com/v1/bpi/currentprice.json").json()[
        "bpi"
    ]["USD"]["rate_float"]

    blank = Divider()

    chan_items = []

    for k, v in chanbal.items():
        sats = v["sat"] if type(v) is dict else v
        if sats != "0":
            chan_items.append(Text([k, ": ", f"丰{int(sats):,}"]))

    gt = (
        int(chanbal["balance"])
        + int(walletbal["total_balance"])
        + int(chanbal["pending_open_balance"])
        + int(chanbal["unsettled_remote_balance"]["sat"])
        + int(chanbal["unsettled_local_balance"]["sat"])
    )

    gtusd = gt / 1e8 * price

    items = (
        [
            AttrWrap(Divider("=", 1), "bright"),
            Text([f"On-Chain:"]),
            AttrWrap(Divider("-", 0, 1), "bright"),
            Text(f"Total balance: 丰{int(walletbal['total_balance']):,}"),
            Text(f"Confirmed balance: 丰{int(walletbal['confirmed_balance']):,}"),
            Text(f"Unconfirmed balance: 丰{int(walletbal['unconfirmed_balance']):,}"),
            AttrWrap(Divider("=", 1), "bright"),
            Text([f"Channel:"]),
            AttrWrap(Divider("-", 0, 1), "bright"),
        ]
        + chan_items
        + [
            AttrWrap(Divider("-", 0, 1), "bright"),
            Text([f"Grand Total balance: "]),
            Padding(Text([("important", f"丰{gt:,}")]), left=20),
            Padding(Text([("important", f" ${gtusd:,.2f}")]), left=20),
        ]
    )

    frame = Frame(
        AttrWrap(ListBox(SimpleListWalker(items)), "body"),
        header=AttrWrap(Text(f"{info['alias']}   F8 exits."), "header"),
    )

    MainLoop(frame, palette, unhandled_input=unhandled).run()


@task
def forwards(c, env=dict(PATH=os.environ["PATH"])):
    f = open("forwards.csv", "w")
    f.write("Date,Fee,Amount,Total Amount,Total Fees\n")
    price = requests.get("https://api.coindesk.com/v1/bpi/currentprice.json").json()[
        "bpi"
    ]["USD"]["rate_float"]
    info = json.loads(c.run("lncli getinfo", env=env, hide=True).stdout)
    blank = Divider()

    hist = json.loads(
        c.run(
            "lncli fwdinghistory --start_time=-6M --max_events=100000",
            hide=True,
            env=env,
        ).stdout
    )["forwarding_events"]

    items = []
    total = 0
    totalamt = 0
    totalus = 0

    for h in hist:
        dt = arrow.get(int(h["timestamp"])).format("YYYY-MM-DD HH:mm")
        totalus += (int(h["fee"]) / 1e8) * price
        total += int(h["fee"])
        totalamt += int(h["amt_out"])
        f.write(f"{dt},{int(h['fee'])},{int(h['amt_out'])},{int(totalamt)},{total}\n")

        items.append(
            Button(
                f"{dt:<10}          丰{int(h['fee']):<10,}     "
                f" 丰{int(h['amt_out']):<10,}      丰{int(totalamt):<10,}      "
                f" 丰{total:,}       ${totalus:.2f}        {h['chan_id_in']}       "
                f" {h['chan_id_out']}"
            )
        )

    items.append(
        Text(
            "Date                        Fee               Amount            Tot Amount"
            "         Tot Fees          Tot Fees $        chan_in                 "
            " chan_out"
        )
    )
    items = items[::-1]

    frame = Frame(
        AttrWrap(ListBox(SimpleListWalker(items)), "body"),
        header=AttrWrap(Text(f"{info['alias']}   F8 exits."), "header"),
    )

    loop = MainLoop(frame, palette, unhandled_input=unhandled)
    loop.run()


@task
def forwards_per_peer(c, env=dict(PATH=os.environ["PATH"])):
    chans = json.loads(c.run("lncli listchannels", env=env, hide=True).stdout)[
        "channels"
    ]
    chans = {x["chan_id"]: x for x in chans}

    with open("graph.json") as f:
        j = json.loads(f.read())
        nodes, edges = j["nodes"], j["edges"]
        aliases = {n["pub_key"]: n["alias"] for n in nodes}

    hist = json.loads(
        c.run(
            "lncli fwdinghistory --start_time=-6M --max_events=100000",
            hide=True,
            env=env,
        ).stdout
    )["forwarding_events"]

    cid_out = defaultdict(lambda: 0)

    print("\n")
    print("Most hungry channels:")
    print("\n")

    for h in hist:
        c = h["chan_id_out"]
        if c in chans:
            pk = chans[c]["remote_pubkey"]
            cid_out[aliases[pk]] += int(int(h["amt_out"]) / int(chans[c]["uptime"]))

    for k, v in sorted([*cid_out.items()], key=lambda x: x[1], reverse=True):
        print(f"{k:<40}          {v:<10}")

    print("\n\n\n")
    print("Most giving channels:")
    print("\n")

    for h in hist:
        c = h["chan_id_in"]
        if c in chans:
            pk = chans[c]["remote_pubkey"]
            cid_out[aliases[pk]] += int(int(h["amt_in"]) / int(chans[c]["uptime"]))

    for k, v in sorted([*cid_out.items()], key=lambda x: x[1], reverse=True):
        print(f"{k:<40}          {v:<10}")
    print("\n")


@task
def connect(c):
    info = json.loads(c.run("lncli getinfo", hide=True).stdout)
    blank = Divider()

    def button_press(button):
        frame.footer = AttrWrap(Text(["Connecting..."]), "header")
        loop.draw_screen()
        cmd = c.run(f"lncli connect {edit.text}", hide=True, warn=True)
        if cmd.stderr:
            frame.footer = AttrWrap(Text([cmd.stderr.strip()]), "header")
        else:
            r = json.loads(cmd.stdout)
            if not r:
                frame.footer = AttrWrap(Text(["connected"]), "header")
            else:
                print(r)

    edit = Edit()

    frame = Frame(
        AttrWrap(
            ListBox(
                SimpleListWalker(
                    [
                        AttrWrap(Divider("=", 1), "bright"),
                        Text([f"Connect"]),
                        blank,
                        Text([f"Address: "]),
                        AttrWrap(edit, "editbx", "editfc"),
                        AttrWrap(Divider("-", 0, 1), "bright"),
                        AttrWrap(Button("connect", button_press), "buttn", "buttnf"),
                    ]
                )
            ),
            "body",
        ),
        header=AttrWrap(Text(f"{info['alias']}   F8 exits."), "header"),
    )

    loop = MainLoop(frame, palette, unhandled_input=unhandled)
    loop.run()


@task
def open_channel(c, env=dict(PATH=os.environ["PATH"])):
    """
    Open a channel with another node, uses lncli
    """
    info = json.loads(c.run("lncli getinfo", hide=True, env=env).stdout)
    blank = Divider()

    def button_press(button):
        frame.footer = AttrWrap(Text(["Connecting..."]), "header")
        loop.draw_screen()
        cmd_str = (
            f"lncli openchannel --node_key={node_key.text} --local_amt={local_amt.text}"
            f" --sat_per_vbyte={sat_per_vbyte.text}"
        )
        frame.footer = AttrWrap(Text([cmd_str]), "header")
        cmd = c.run(cmd_str, hide=True, warn=True, env=env)
        if cmd.stderr:
            frame.footer = AttrWrap(Text([cmd.stderr.strip()]), "header")
        elif cmd.stdout:
            frame.footer = AttrWrap(Text([cmd.stdout.strip()]), "header")
        else:
            frame.footer = AttrWrap(Text(["No output"]), "header")

    node_key = Edit()
    local_amt = Edit()
    sat_per_vbyte = Edit(edit_text="1")

    debug = urwid.Text("")

    def handler(widget, newtext):
        try:
            debug.set_text(f"丰{int(newtext):,}")
        except:
            pass

    key = connect_signal(local_amt, "change", handler)

    pad = lambda x: [Padding(Pile(x), left=2, right=2, min_width=20)]

    frame = Frame(
        AttrWrap(
            ListBox(
                SimpleListWalker(
                    [
                        AttrWrap(Divider("=", 1), "bright"),
                        Text([f"Open Channel"]),
                        blank,
                    ]
                    + pad(
                        [
                            Text([f"Node Key: "]),
                            blank,
                            Padding(AttrWrap(node_key, "editbx", "editfc"), width=67),
                        ]
                    )
                    + [blank, AttrWrap(Divider("-", 0, 1), "bright")]
                    + pad(
                        [
                            Text([f"Local Amount: "]),
                            blank,
                            Padding(AttrWrap(local_amt, "editbx", "editfc"), width=15),
                            debug,
                        ]
                    )
                    + [blank, AttrWrap(Divider("-", 0, 1), "bright"), blank]
                    + pad(
                        [
                            Text([f"Sat per VByte: "]),
                            blank,
                            Padding(
                                AttrWrap(sat_per_vbyte, "editbx", "editfc"), width=5
                            ),
                        ]
                    )
                    + [
                        blank,
                        AttrWrap(Divider("-", 0, 1), "bright"),
                        blank,
                        Padding(
                            AttrWrap(
                                Button("Open Channel", button_press), "buttn", "buttnf"
                            ),
                            width=20,
                        ),
                    ]
                )
            ),
            "body",
        ),
        header=AttrWrap(Text(f"{info['alias']}   F8 exits."), "header"),
    )

    loop = MainLoop(frame, palette, unhandled_input=unhandled)
    loop.run()


@task
def close_channel(c, env=dict(PATH=os.environ["PATH"])):
    """
    Close a channel
    """
    info = json.loads(c.run("lncli getinfo", hide=True, env=env).stdout)
    blank = Divider()
    sat_per_vbyte = Edit(edit_text="1")
    force = CheckBox("Force:")
    dry_run = CheckBox("Dry Run:")

    pad = lambda x: [Padding(Pile(x), left=2, right=2, min_width=20)]

    channels = json.loads(c.run("lncli listchannels", hide=True, env=env).stdout)
    items = pad(
        [
            Text([f"Sat per VByte: "]),
            blank,
            Padding(AttrWrap(sat_per_vbyte, "editbx", "editfc"), width=5),
            blank,
            force,
            dry_run,
            blank,
        ]
    )

    def button_press(b):
        frame.footer = AttrWrap(Text(["Closing..."]), "header")
        loop.draw_screen()
        txid, oi = b.channel_point.split(":")
        force_close_flag = "--force" if force.get_state() else ""
        sat_per_vbyte_flag = (
            f"--sat_per_vbyte {sat_per_vbyte.text}"
            if force.get_state() == False
            else ""
        )
        cmd = (
            f"lncli closechannel --funding_txid {txid} --output_index {oi}"
            f" {sat_per_vbyte_flag} {force_close_flag}"
        )
        frame.footer = AttrWrap(Text([cmd]), "header")
        loop.draw_screen()
        if dry_run.get_state() == False:
            out = c.run(cmd, hide=True, warn=True, env=env)
            if out.stderr:
                frame.footer = AttrWrap(Text([out.stderr.strip()]), "header")
            else:
                frame.footer = AttrWrap(Text([out.stdout.strip()]), "header")
        else:
            frame.footer = AttrWrap(Text(cmd), "header")

    for ch in channels["channels"]:
        key = ch["remote_pubkey"]
        lb = int(ch["local_balance"])
        rb = int(ch["remote_balance"])
        alias = json.loads(
            c.run(f"lncli getnodeinfo {key}", env=env, hide=True).stdout
        )["node"]["alias"]
        b = Button(f"{alias:<30}    local  {lb:<20,}    remote  {rb:,}", button_press)
        b.pubkey = key
        b.channel_point = ch["channel_point"]
        items.append(b)

    frame = Frame(AttrWrap(ListBox(SimpleListWalker(items)), "body"))

    loop = MainLoop(frame, palette, unhandled_input=unhandled)
    loop.run()
