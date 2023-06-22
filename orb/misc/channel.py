# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-15 07:15:28
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-09-08 15:33:33

import inspect

from kivy.properties import NumericProperty
from kivy.properties import StringProperty
from kivy.properties import ListProperty
from kivy.properties import BooleanProperty
from kivy.event import EventDispatcher
from kivy.clock import mainthread

from orb.app import App
from orb.store.db_meta import channel_stats_db_name
from orb.misc.decorators import db_connect


class Channel(EventDispatcher):
    """
    This class intends to host all channel related data in Kivy properties,
    including channel policies.

    This means the class object should not be replaced, as other
    objects in memory should be allowed to refer to it.

    Instead the properties should be modified when the channel's
    internal state changes.
    """

    #: The channel's chapacity in satoshis
    capacity = NumericProperty(0)
    #: The channel's remote_pubkey
    remote_pubkey = StringProperty("")
    #: The channel's channel_point
    channel_point = StringProperty("")
    #: The channel's local_balance in sats
    local_balance = NumericProperty(0)
    #: The channel's remote_balance in sats
    remote_balance = NumericProperty(0)
    #: The channel's chan_id
    chan_id = StringProperty(0)
    #: The channel's pending_htlcs
    pending_htlcs = ListProperty([])
    #: The channel's total_satoshis_sent
    total_satoshis_sent = NumericProperty(0)
    #: The channel's total_satoshis_received
    total_satoshis_received = NumericProperty(0)
    #: The channel's unsettled_balance
    unsettled_balance = NumericProperty(0)
    #: The channel's commit_fee
    commit_fee = NumericProperty(0)
    #: Whether we are the initiator
    initiator = BooleanProperty(False)
    #: Balanced ratio, i.e the ratio at which the channel needs to be for the node to be balanced
    balanced_ratio = NumericProperty(-1)
    #: Whether the channel is active or not
    active = BooleanProperty(True)

    # POLICY

    #: the fee_rate_milli_msat as a NumericProperty
    fee_rate_milli_msat = NumericProperty(0)
    #: the time_lock_delta as a NumericProperty
    time_lock_delta = NumericProperty(40)
    #: the min_htlc as a NumericProperty
    min_htlc_msat = NumericProperty(0)
    #: the max_htlc_msat as a NumericProperty
    max_htlc_msat = NumericProperty(0)
    #: the fee_base_msat as a NumericProperty
    fee_base_msat = NumericProperty(0)

    def __init__(self, channel, *args, **kwargs):
        """
        Channel constructor.
        """
        super(Channel, self).__init__(*args, **kwargs)
        self.update(channel)

        self._policies_are_bound = False

    def get_policies(self):
        """
        Get the channel policies from LND,
        and bind them to update_lnd_with_policies. This means whenever
        a fee policy is changed in Orb, it immediately gets updated
        in LND.
        """
        policy_to = App.get_running_app().ln.get_policy_to(self.chan_id)

        @mainthread
        def do_update(policy_to):
            self._unbind_policies()
            self.fee_rate_milli_msat = policy_to.fee_rate_milli_msat
            self.fee_base_msat = policy_to.fee_base_msat
            self.time_lock_delta = policy_to.time_lock_delta
            self.max_htlc_msat = policy_to.max_htlc_msat
            self.min_htlc_msat = policy_to.min_htlc
            self._bind_policies()

        do_update(policy_to)

    def _bind_policies(self):
        """
        Bind local policy updates to the channel to LND
        """
        if not self._policies_are_bound:
            self.bind(fee_rate_milli_msat=self.update_lnd_with_policies)
            self.bind(fee_base_msat=self.update_lnd_with_policies)
            self.bind(time_lock_delta=self.update_lnd_with_policies)
            self.bind(max_htlc_msat=self.update_lnd_with_policies)
            self.bind(min_htlc_msat=self.update_lnd_with_policies)
            self._policies_are_bound = True

    def _unbind_policies(self):
        """
        Unbind local policy updates to the channel to LND
        """
        if self._policies_are_bound:
            self.unbind(fee_rate_milli_msat=self.update_lnd_with_policies)
            self.unbind(fee_base_msat=self.update_lnd_with_policies)
            self.unbind(time_lock_delta=self.update_lnd_with_policies)
            self.unbind(max_htlc_msat=self.update_lnd_with_policies)
            self.unbind(min_htlc_msat=self.update_lnd_with_policies)
            self._policies_are_bound = False

    def update_lnd_with_policies(self, *_):
        """
        Update LND with the channel policies specified
        in tbis object.
        """
        result = App.get_running_app().ln.update_channel_policy(
            channel=self,
            fee_rate=max(self.fee_rate_milli_msat / 1e6, 1e-06),
            base_fee_msat=self.fee_base_msat,
            time_lock_delta=self.time_lock_delta,
            max_htlc_msat=self.max_htlc_msat,
            min_htlc_msat=self.min_htlc_msat,
        )

    def update(self, channel):
        """
        Update the given Channel object with the given lnd
        channel.
        """
        self.local_balance = channel.local_balance
        self.capacity = channel.capacity
        self.remote_pubkey = channel.remote_pubkey
        self.remote_balance = channel.remote_balance
        self.chan_id = str(channel.chan_id)
        self.pending_htlcs = channel.pending_htlcs[:]
        self.total_satoshis_sent = channel.total_satoshis_sent
        self.total_satoshis_received = channel.total_satoshis_received
        self.initiator = channel.initiator
        self.commit_fee = channel.commit_fee
        self.unsettled_balance = channel.unsettled_balance
        self.channel_point = channel.channel_point
        self.active = channel.active

    @property
    def alias(self):
        return App.get_running_app().ln.get_node_alias(self.remote_pubkey)

    @property
    def local_balance_include_pending(self):
        """
        Get the channel's local balance, plus its pending outgoing HTLCs.
        This is because the local balance does not including the pending HTLCs,
        which means the local balance changes based on HTLC activity. This
        may not always be desireable.
        """
        return self.local_balance + sum(
            [int(p.amount) for p in self.pending_htlcs if not p.incoming]
        )

    @property
    def remote_balance_include_pending(self):
        return self.remote_balance + sum(
            [int(p.amount) for p in self.pending_htlcs if p.incoming]
        )

    @property
    def ratio(self):
        """
        Get the channels's ratio
        """
        return self.local_balance / self.capacity

    @property
    def ratio_include_pending(self):
        """
        Get the channels's ratio
        """
        return self.local_balance_include_pending / self.capacity

    @property
    def profit(self):
        """
        Channel profit is how much the channel made in fees
        minus how much was spent rebalancing towards it.
        """
        return self.earned - self.debt

    @property
    @db_connect(channel_stats_db_name)
    def debt(self):
        """
        How much was spent rebalancing towards that channel.
        """
        from orb.store import model

        stats = (
            model.ChannelStats()
            .select()
            .where(model.ChannelStats.chan_id == self.chan_id)
        )
        if stats:
            return int(stats.first().debt_msat / 1000)
        return 0

    @property
    @db_connect(channel_stats_db_name)
    def earned(self):
        """
        How much the channel has earned in fees.
        """
        from orb.store import model

        out_stats = (
            model.ChannelStats()
            .select()
            .where(model.ChannelStats.chan_id == self.chan_id)
        )
        if out_stats:
            return int(out_stats.first().earned_msat / 1000)
        return 0

    @property
    @db_connect(channel_stats_db_name)
    def helped_earn(self):
        """
        How much the channel helped earned in fees.
        """
        from orb.store import model

        in_stats = (
            model.ChannelStats()
            .select()
            .where(model.ChannelStats.chan_id == self.chan_id)
        )
        if in_stats:
            return int(in_stats.first().helped_earn_msat / 1000)
        return 0

    @property
    def pending_in(self):
        return sum([int(p.amount) for p in self.pending_htlcs if p.incoming])

    @property
    def pending_out(self):
        return sum([int(p.amount) for p in self.pending_htlcs if not p.incoming])

    @property
    def pending_in_htlc_ids(self):
        return [p.htlc_index for p in self.pending_htlcs if p.incoming]

    @property
    def pending_out_htlc_ids(self):
        return [p.htlc_index for p in self.pending_htlcs if not p.incoming]

    def as_dict(self):
        ret = {}
        for i in inspect.getmembers(self):
            if not i[0].startswith("_"):
                if not inspect.ismethod(i[1]):
                    if type(i[1]) in [str, int, float, bool]:
                        ret[i[0]] = i[1]
        return ret
