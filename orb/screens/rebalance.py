import threading

from kivy.clock import mainthread

from orb.components.popup_drop_shadow import PopupDropShadow
from orb.misc.output import *
from orb.logic.pay_logic import pay_thread
from orb.logic.channel_selector import get_low_inbound_channel
from orb.logic.channel_selector import get_low_outbound_channel
import data_manager


class Rebalance(PopupDropShadow):
    def __init__(self, **kwargs):
        PopupDropShadow.__init__(self, **kwargs)
        self.output = Output(None)
        self.output.lnd = data_manager.data_man.lnd
        self.lnd = data_manager.data_man.lnd
        self.chan_id = None
        self.last_hop_pubkey = None
        self.alias_to_pk = {}

        @mainthread
        def delayed():
            channels = self.lnd.get_channels()
            for c in channels:
                self.ids.spinner_out_id.values.append(
                    f"{c.chan_id}: {self.lnd.get_node_alias(c.remote_pubkey)}"
                )
                self.ids.spinner_in_id.values.append(
                    f"{self.lnd.get_node_alias(c.remote_pubkey)}"
                )
                self.alias_to_pk[
                    self.lnd.get_node_alias(c.remote_pubkey)
                ] = c.remote_pubkey

        delayed()

    def first_hop_spinner_click(self, chan):
        self.chan_id = int(chan.split(":")[0])

    def last_hop_spinner_click(self, alias):
        self.last_hop_pubkey = self.alias_to_pk[alias]

    def rebalance(self):
        def thread_function():
            amount = int(self.ids.amount.text)

            if not self.chan_id:
                self.chan_id = get_low_inbound_channel(
                    lnd=self.lnd,
                    avoid=[],
                    pk_ignore=[],
                    chan_ignore=[],
                    num_sats=amount,
                    ratio=0.5,
                )

            if not self.last_hop_pubkey:
                _, self.last_hop_pubkey = get_low_outbound_channel(
                    lnd=self.lnd,
                    avoid=[],
                    pk_ignore=[],
                    chan_ignore=[],
                    num_sats=amount,
                    ratio=0.5,
                )

            raw, payment_request = data_manager.data_man.lnd.generate_invoice(
                memo='rebalance', amount=amount
            )
            status = pay_thread(
                inst=self,
                thread_n=0,
                fee_rate=int(self.ids.fee_rate.text),
                payment_request=payment_request,
                payment_request_raw=raw,
                outgoing_chan_id=self.chan_id,
                last_hop_pubkey=self.last_hop_pubkey,
                max_paths=int(self.ids.max_paths.text),
            )

        self.thread = threading.Thread(target=thread_function)
        self.thread.daemon = True
        self.thread.start()

    def kill(self):
        self.thread.stop()
