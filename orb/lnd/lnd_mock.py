# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-31 04:49:50
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-08-31 15:46:50

from collections import namedtuple
from dataclasses import dataclass
from typing import Any
from time import sleep
from random import choice, randrange

from orb.misc.auto_obj import dict2obj

M = lambda **kwargs: dict2obj(kwargs)


@dataclass
class Channel:

    capacity: Any
    remote_pubkey: Any
    local_balance: Any
    remote_balance: Any
    chan_id: Any
    pending_htlcs: Any
    total_satoshis_sent: Any
    total_satoshis_received: Any
    initiator: Any
    commit_fee: Any
    unsettled_balance: Any
    channel_point: Any

    def ListFields(self):
        return []


@dataclass
class Policy:
    fee_rate_milli_msat: Any
    min_htlc: Any = 1
    max_htlc_msat: Any = 1000000
    time_lock_delta: Any = 44
    last_update: Any = "0"
    fee_base_msat: Any = 1000


Info = namedtuple("Info", "alias identity_pubkey")
NodeInfo = namedtuple("NodeInfo", "alias")
Balance = namedtuple("Balance", "total_balance confirmed_balance unconfirmed_balance")
ChannelBalance = namedtuple(
    "ChannelBalance",
    "local_balance remote_balance unsettled_local_balance unsettled_remote_balance",
)
CB = namedtuple("ChannelBalanceObj", "sat")
FeeReport = namedtuple("FeeReport", "day_fee_sum week_fee_sum month_fee_sum")

adj = [
    "unfightable",
    "weary",
    "stubborn",
    "indignant",
    "vehemant",
    "green",
    "sleepy",
    "screamy",
    "happy",
    "sad",
    "blue",
    "determined",
    "unstoppable",
    "jovial",
]

nouns = [
    "fiat",
    "visa",
    "bukele",
    "chivo",
    "volcano",
    "exchange",
    "strike",
    "bolt",
    "sats",
    "coin",
    "elon",
    "satoshi",
    "dolphin",
    "herring",
    "fighter",
    "pilot",
    "hoarder",
]


class LndMock(object):
    def get_channels(self):
        channels = []
        for cid in range(50):
            capacity = choice([3e6, 5e6, 10e6])
            f = 0.5
            local = randrange(0, capacity)
            remote = capacity - local
            sent = randrange(1e6, 10e8)
            c = Channel(
                capacity=capacity,
                pending_htlcs=[],
                local_balance=int(local),
                remote_balance=int(remote),
                remote_pubkey=f"peer_{cid}",
                chan_id=cid,
                total_satoshis_sent=sent,
                total_satoshis_received=sent,
                initiator=False,
                commit_fee=5,
                unsettled_balance=0,
                channel_point="123:0",
            )
            channels.append(c)
        return channels

    def get_info(self):
        return Info(alias="mock node", identity_pubkey="mock_pubkey")

    def get_node_alias(self, x):
        return f"{choice(adj)}_{choice(nouns)}"

    def get_policy_to(self, x):
        return Policy(fee_rate_milli_msat=1000, fee_base_msat=1000)

    def get_policy_from(self, x):
        return Policy(fee_rate_milli_msat=1000, fee_base_msat=1000)

    def get_balance(self):
        return Balance(total_balance=0, confirmed_balance=0, unconfirmed_balance=0)

    def channel_balance(self):
        return ChannelBalance(
            local_balance=CB(sat=10_000_000),
            remote_balance=CB(sat=10_000_000),
            unsettled_local_balance=CB(sat=0),
            unsettled_remote_balance=CB(sat=0),
        )

    def fee_report(self):
        daily = randrange(30_000, 120_000)
        weekly = randrange(30_000 * 7, 120_000 * 7)
        monthly = randrange(30_000 * 30, 70_000 * 30)
        return FeeReport(day_fee_sum=daily, week_fee_sum=weekly, month_fee_sum=monthly)

    def get_pending_channels(self):
        m = M(
            total_limbo_balance=1000,
            pending_open_channels=[
                dict(
                    channel=dict(
                        capacity=1000000,
                        pending_htlcs=[],
                        local_balance=500000,
                        remote_balance=500000,
                        remote_pubkey="f",
                        chan_id="5",
                        total_satoshis_sent=50000,
                        total_satoshis_received=50000,
                        initiator=False,
                        commit_fee=5,
                        unsettled_balance=0,
                        channel_point="123:0",
                    )
                )
            ],
        )
        return m

    def subscribe_channel_graph(self):
        while True:
            cid = choice([x for x in range(5)])
            yield M(
                channel_updates=[
                    M(
                        advertising_node=f"peer_{cid}",
                        chan_id=cid,
                        routing_policy=M(fee_rate_milli_msat=10),
                    )
                ]
            )
            sleep(1)

    def get_forwarding_history(self, index_offset=0, num_max_events=100):
        class ForwardHistory:
            forwarding_events = []
            last_offset_index = 0

        return ForwardHistory()

    def update_channel_policy(self, channel, *args, **kwargs):
        pass

    def get_htlc_events(self):
        return []

    def get_channel_events(self):
        return []

    def list_payments(
        self, include_incomplete=True, index_offset=0, max_payments=100, reversed=False
    ):
        class Payments:
            payments = []
            last_offset_index = 0

        return Payments()
