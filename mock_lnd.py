from collections import namedtuple

Channel = namedtuple(
    "Channel", "capacity remote_pubkey local_balance remote_balance chan_id"
)
Info = namedtuple("Info", "alias")
NodeInfo = namedtuple("NodeInfo", "alias")
Policy = namedtuple("Policy", "fee_rate_milli_msat")
Balance = namedtuple("Balance", "total_balance confirmed_balance unconfirmed_balance")
ChannelBalance = namedtuple("ChannelBalance", "local_balance remote_balance")
CB = namedtuple("ChannelBalanceObj", "sat")
FeeReport = namedtuple("FeeReport", "day_fee_sum week_fee_sum month_fee_sum")


class Lnd(object):
    def get_channels(self):
        return [
            Channel(
                capacity=1000000,
                local_balance=750000,
                remote_balance=250000,
                remote_pubkey="a",
                chan_id="5",
            ),
            Channel(
                capacity=1000000,
                local_balance=600000,
                remote_balance=400000,
                remote_pubkey="b",
                chan_id="5",
            ),
            Channel(
                capacity=1000000,
                local_balance=500000,
                remote_balance=500000,
                remote_pubkey="c",
                chan_id="5",
            ),
            Channel(
                capacity=1000000,
                local_balance=500000,
                remote_balance=500000,
                remote_pubkey="d",
                chan_id="5",
            ),
            Channel(
                capacity=1000000,
                local_balance=500000,
                remote_balance=500000,
                remote_pubkey="e",
                chan_id="5",
            ),
            Channel(
                capacity=1000000,
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
