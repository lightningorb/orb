# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-15 07:15:28
# @Last Modified by:   lnorb.com
# @Last Modified time: 2021-12-30 11:13:51

from threading import Thread

from kivy.clock import mainthread
from kivy.properties import ObjectProperty, NumericProperty
from kivy.uix.widget import Widget

from orb.misc.decorators import guarded
import data_manager


class AEFees(Widget):
    """
    This class displays and modifies fees on Channels in the
    :py:mod:`orb.attribute_editor.attribute_editor` class.
    """

    #: The channel an ObjectProperty
    channel = ObjectProperty(None)
    #: the fee_rate_milli_msat as a NumericProperty
    fee_rate_milli_msat = NumericProperty(0)
    #: the time_lock_delta as a NumericProperty
    time_lock_delta = NumericProperty(0)
    #: the min_htlc as a NumericProperty
    min_htlc = NumericProperty(0)
    #: the max_htlc_msat as a NumericProperty
    max_htlc_msat = NumericProperty(0)
    #: the fee_base_msat as a NumericProperty
    fee_base_msat = NumericProperty(0)
    #: the last_update as a NumericProperty
    last_update = NumericProperty(0)

    def on_channel(self, inst, channel):
        """
        Invoked whenever a channel is selected.
        """
        if channel:

            @mainthread
            def update(policy_to):
                self.fee_rate_milli_msat = policy_to.fee_rate_milli_msat
                self.time_lock_delta = policy_to.time_lock_delta
                self.min_htlc = policy_to.min_htlc
                self.max_htlc_msat = policy_to.max_htlc_msat
                self.last_update = policy_to.last_update
                self.fee_base_msat = policy_to.fee_base_msat

            def get_fees():
                policy_to = data_manager.data_man.lnd.get_policy_to(channel.chan_id)
                if policy_to:
                    update(policy_to)

            Thread(target=get_fees).start()

    @guarded
    def fee_rate_milli_msat_changed(self, val):
        """
        Invoked whenever the fee rate is changed.
        """
        val = int(val)
        if val != self.fee_rate_milli_msat:
            data_manager.data_man.lnd.update_channel_policy(
                channel=self.channel,
                fee_rate=val / 1e6,
                base_fee_msat=self.fee_base_msat,
                time_lock_delta=self.time_lock_delta,
            )
            self.fee_rate_milli_msat = val

    @guarded
    def fee_base_msat_changed(self, val):
        """
        Invoked whenever the fee base rate is changed.
        """
        val = int(val)
        if val != self.fee_base_msat:
            data_manager.data_man.lnd.update_channel_policy(
                channel=self.channel,
                fee_rate=self.fee_rate_milli_msat / 1e6,
                base_fee_msat=val,
                time_lock_delta=self.time_lock_delta,
            )
            self.fee_base_msat = val

    @guarded
    def min_htlc_changed(self, val):
        """
        Invoked whenever the min HTLC is changed.
        """
        val = int(val)
        if val != self.min_htlc:
            data_manager.data_man.lnd.update_channel_policy(
                channel=self.channel,
                time_lock_delta=self.time_lock_delta,
                fee_rate=self.fee_rate_milli_msat / 1e6,
                base_fee_msat=self.fee_base_msat,
                min_htlc_msat=val,
                min_htlc_msat_specified=True,
            )
            self.min_htlc = val

    @guarded
    def max_htlc_msat_changed(self, val):
        """
        Invoked whenever the max HTLC is changed.
        """
        val = int(val)
        if val != self.max_htlc_msat:
            data_manager.data_man.lnd.update_channel_policy(
                channel=self.channel,
                time_lock_delta=self.time_lock_delta,
                fee_rate=self.fee_rate_milli_msat / 1e6,
                base_fee_msat=self.fee_base_msat,
                max_htlc_msat=val,
            )
            self.max_htlc_msat = val

    @guarded
    def time_lock_delta_changed(self, val):
        """
        Invoked whenever timelock delta is changed.
        """
        val = int(val)
        if val != self.time_lock_delta:
            data_manager.data_man.lnd.update_channel_policy(
                channel=self.channel,
                time_lock_delta=val,
                fee_rate=self.fee_rate_milli_msat / 1e6,
                base_fee_msat=self.fee_base_msat,
            )
            self.time_lock_delta = val
