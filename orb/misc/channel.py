# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-15 07:15:28
# @Last Modified by:   lnorb.com
# @Last Modified time: 2021-12-31 07:09:14

from kivy.properties import NumericProperty
from kivy.properties import StringProperty
from kivy.properties import ListProperty
from kivy.properties import BooleanProperty
from kivy.event import EventDispatcher


class Channel(EventDispatcher):
    """
    This class is still a bit experimental. It intends to host
    all channel related data in Kivy properties.

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
    #: The channel's initiator
    initiator = BooleanProperty(False)

    def __init__(self, channel, *args, **kwargs):
        """
        Channel constructor.
        """
        super(Channel, self).__init__(*args, **kwargs)
        self.update(channel)

    def update(self, channel):
        """
        Update the given Channel object with the given lnd
        channel.
        """
        self.local_balance = channel.local_balance
        self.capacity = channel.capacity
        self.remote_pubkey = channel.remote_pubkey
        self.local_balance = channel.local_balance
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
