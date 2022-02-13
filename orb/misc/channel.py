# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-15 07:15:28
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-02-13 10:46:23

from threading import Thread, Lock

from kivy.clock import Clock
from kivy.properties import NumericProperty
from kivy.properties import StringProperty
from kivy.properties import ListProperty
from kivy.properties import BooleanProperty
from kivy.event import EventDispatcher

from orb.lnd import Lnd


class CountLock:
    """
    A Lock context manager, that locks the lock if
    there are more than _num threads currently
    within the context.
    """

    def __init__(self, num):
        self._count = 0
        self._num = num
        self._lock = Lock()

    def __enter__(self):
        self._count += 1
        if self._count > self._num:
            self._lock.acquire()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._count -= 1
        if self._lock.locked():
            self._lock.release()


edge_mutex = CountLock(50)


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
    #: The channel's local_balance
    local_balance = NumericProperty(0)
    #: The channel's remote_balance
    remote_balance = NumericProperty(0)
    #: The channel's chan_id
    chan_id = NumericProperty(0)
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

        self.schedule_updates()

    @property
    def active(self):
        return self.channel.active

    def schedule_updates(self):
        def get_policies(*_):
            """
            Get the channel policies from LND on a thread,
            and bind them to update_lnd_with_policies. This means whenever
            a fee policy is changed in Orb, it immediately gets updated
            in LND.
            """
            with edge_mutex:
                policy_to = Lnd().get_policy_to(self.chan_id)
                self._unbind_policies()
                self.fee_rate_milli_msat = policy_to.fee_rate_milli_msat
                self.fee_base_msat = policy_to.fee_base_msat
                self.time_lock_delta = policy_to.time_lock_delta
                self.max_htlc_msat = policy_to.max_htlc_msat
                self.min_htlc_msat = policy_to.min_htlc
                self._bind_policies()

        # get the policies now
        Clock.schedule_once(lambda *_: Thread(target=get_policies).start(), 0)

        # and update the policies every 5 minutes, in case they change
        # in LND
        Clock.schedule_interval(lambda *_: Thread(target=get_policies).start(), 5 * 60)

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
        result = Lnd().update_channel_policy(
            channel=self,
            fee_rate=self.fee_rate_milli_msat / 1e6,
            base_fee_msat=self.fee_base_msat,
            time_lock_delta=self.time_lock_delta,
            max_htlc_msat=self.max_htlc_msat,
            min_htlc_msat=self.min_htlc_msat,
        )
        print(result)

    def update(self, channel):
        """
        Update the given Channel object with the given lnd
        channel.
        """
        self.local_balance = channel.local_balance
        self.capacity = channel.capacity
        self.remote_pubkey = channel.remote_pubkey
        self.remote_balance = channel.remote_balance
        self.chan_id = int(channel.chan_id)
        self.pending_htlcs = channel.pending_htlcs
        self.total_satoshis_sent = channel.total_satoshis_sent
        self.total_satoshis_received = channel.total_satoshis_received
        self.ListFields = channel.ListFields if hasattr(channel, "ListFields") else None
        self.initiator = channel.initiator
        self.commit_fee = channel.commit_fee
        self.unsettled_balance = channel.unsettled_balance
        self.channel_point = channel.channel_point
        self.channel = channel

    @property
    def alias(self):
        return Lnd().get_node_alias(self.remote_pubkey)

    @property
    def local_balance_include_pending(self):
        """
        Get the channel's local balance, plus its pending outgoing HTLCs.
        This is because the local balance does not including the pending HTLCs,
        which means the local balance changes based on HTLC activity. This
        may not always be desireable.
        """
        return self.local_balance + sum(
            int(p.amount) for p in self.pending_htlcs if not p.incoming
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
    def _profit(self):
        """
        Channel profit is how much the channel made in fees
        minus how much was spent rebalancing towards it.
        """
        pass

    @property
    def _debt(self):
        """
        How much was spent rebalancing towards that channel.
        """
        pass

    @property
    def earned(self):
        """
        How much the channel has earned in fees.
        """
        from orb.store import model

        try:
            return sum(
                [
                    x.fee
                    for x in model.ForwardEvent()
                    .select()
                    .where(model.ForwardEvent.chan_id_out == str(self.chan_id))
                ]
            )
        except:
            return 0

    @property
    def helped_earn(self):
        """
        How much the channel helped earned in fees.
        """
        from orb.store import model

        try:
            return sum(
                [
                    x.fee
                    for x in model.ForwardEvent()
                    .select()
                    .where(model.ForwardEvent.chan_id_in == str(self.chan_id))
                ]
            )
        except:
            return 0

    @property
    def pending_in(self):
        return sum(int(p.amount) for p in self.pending_htlcs if p.incoming)

    @property
    def pending_out(self):
        return sum(int(p.amount) for p in self.pending_htlcs if not p.incoming)

    @property
    def pending_in_htlc_ids(self):
        return [p.htlc_index for p in self.pending_htlcs if p.incoming]

    @property
    def pending_out_htlc_ids(self):
        return [p.htlc_index for p in self.pending_htlcs if not p.incoming]
