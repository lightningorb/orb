from kivy.clock import mainthread
from kivy.properties import ObjectProperty, NumericProperty
from kivy.uix.widget import Widget

from threading import Thread
import data_manager
from orb.misc.decorators import guarded


class AEFees(Widget):
    channel = ObjectProperty(None)
    fee_rate_milli_msat = NumericProperty(0)
    time_lock_delta = NumericProperty(0)
    min_htlc = NumericProperty(0)
    max_htlc_msat = NumericProperty(0)
    fee_base_msat = NumericProperty(0)
    last_update = NumericProperty(0)

    def on_channel(self, inst, channel):
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
                update(policy_to)

            Thread(target=get_fees).start()

    @guarded
    def fee_rate_milli_msat_changed(self, val):
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
        val = int(val)
        if val != self.time_lock_delta:
            data_manager.data_man.lnd.update_channel_policy(
                channel=self.channel,
                time_lock_delta=val,
                fee_rate=self.fee_rate_milli_msat / 1e6,
                base_fee_msat=self.fee_base_msat,
            )
            self.time_lock_delta = val