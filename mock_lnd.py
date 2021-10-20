from collections import namedtuple
from dataclasses import dataclass
from typing import Any

@dataclass
class Channel:

    capacity: Any
    remote_pubkey: Any
    local_balance: Any
    remote_balance: Any
    chan_id: Any
    pending_htlcs: Any

    def ListFields(self):
        return []

@dataclass
class Policy:
    fee_rate_milli_msat: Any
    min_htlc: Any = 1
    max_htlc_msat: Any = 1000000
    time_lock_delta: Any = 44
    last_update: Any = '0'


Info = namedtuple("Info", "alias")
NodeInfo = namedtuple("NodeInfo", "alias")
Balance = namedtuple("Balance", "total_balance confirmed_balance unconfirmed_balance")
ChannelBalance = namedtuple("ChannelBalance", "local_balance remote_balance")
CB = namedtuple("ChannelBalanceObj", "sat")
FeeReport = namedtuple("FeeReport", "day_fee_sum week_fee_sum month_fee_sum")


class Lnd(object):
    def get_channels(self):
        return [
            Channel(
                capacity=1000000,
                pending_htlcs=[],
                local_balance=750000,
                remote_balance=250000,
                remote_pubkey="a",
                chan_id="5",
            ),
            Channel(
                capacity=1000000,
                pending_htlcs=[],
                local_balance=600000,
                remote_balance=400000,
                remote_pubkey="b",
                chan_id="5",
            ),
            Channel(
                capacity=1000000,
                pending_htlcs=[],
                local_balance=500000,
                remote_balance=500000,
                remote_pubkey="c",
                chan_id="5",
            ),
            Channel(
                capacity=1000000,
                pending_htlcs=[],
                local_balance=500000,
                remote_balance=500000,
                remote_pubkey="d",
                chan_id="5",
            ),
            Channel(
                capacity=1000000,
                pending_htlcs=[],
                local_balance=500000,
                remote_balance=500000,
                remote_pubkey="e",
                chan_id="5",
            ),
            Channel(
                capacity=1000000,
                pending_htlcs=[],
                local_balance=500000,
                remote_balance=500000,
                remote_pubkey="f",
                chan_id="5",
            ),
        ]

    def get_info(self):
        return Info(alias="foobar")

    def get_node_alias(self, x):
        return x

    def get_policy_to(self, x):
        return Policy(fee_rate_milli_msat=1000)

    def get_policy_from(self, x):
        return Policy(fee_rate_milli_msat=1000)

    def get_balance(self):
        return Balance(total_balance=0, confirmed_balance=0, unconfirmed_balance=0)

    def channel_balance(self):
        return ChannelBalance(local_balance=CB(sat=0), remote_balance=CB(sat=0))

    def fee_report(self):
        return FeeReport(
            day_fee_sum=1000,
            week_fee_sum=1000,
            month_fee_sum=1000,
        )
