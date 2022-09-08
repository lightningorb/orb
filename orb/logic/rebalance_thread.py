# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-28 08:26:04
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-09-08 12:18:27

from traceback import format_exc

from orb.app import App

from orb.logic.channel_selector import get_low_inbound_channel
from orb.logic.channel_selector import get_low_outbound_channel
from orb.logic.pay_logic import pay_thread, PaymentStatus
from orb.core.stoppable_thread import StoppableThread


class RebalanceThread(StoppableThread):
    def __init__(
        self,
        amount,
        chan_id,
        last_hop_pubkey,
        max_paths,
        fee_rate,
        time_pref,
        name,
        thread_n,
        ln=None,
        *args,
        **kwargs,
    ):
        super(RebalanceThread, self).__init__(*args, **kwargs)
        self.amount = amount
        self.chan_id = chan_id
        self.last_hop_pubkey = last_hop_pubkey
        self.max_paths = max_paths
        self.fee_rate = fee_rate
        self.time_pref = time_pref
        self.name = name
        self.thread_n = thread_n
        app = App.get_running_app()
        if not ln:
            ln = app.ln
        self.ln = ln

    def run(self):
        try:
            self.__run()
        except Exception as e:
            print(format_exc())
        finally:
            self.stop()

    def __run(self):
        if not self.chan_id:
            self.chan_id = get_low_inbound_channel(
                pk_ignore=[self.last_hop_pubkey] if self.last_hop_pubkey else [],
                chan_ignore=[],
                num_sats=self.amount,
            )

        if not self.last_hop_pubkey:
            _, self.last_hop_pubkey = get_low_outbound_channel(
                pk_ignore=[],
                chan_ignore=[self.chan_id],
                num_sats=self.amount,
            )
        app = App.get_running_app()
        from_pk = app.channels.channels[self.chan_id].remote_pubkey
        from_alias = self.ln.get_node_alias(from_pk)
        to_alias = self.ln.get_node_alias(self.last_hop_pubkey)

        print(f"Rebalancing {self.amount} from {from_alias} to {to_alias}")

        payment_request = self.ln.generate_invoice(memo="rebalance", amount=self.amount)
        status = pay_thread(
            ln=self.ln,
            stopped=self.stopped,
            thread_n=0,
            fee_rate=self.fee_rate,
            time_pref=self.time_pref,
            payment_request=payment_request,
            outgoing_chan_id=self.chan_id,
            last_hop_pubkey=self.last_hop_pubkey,
            max_paths=self.max_paths,
        )

        if not status == PaymentStatus.success:
            try:
                self.ln.cancel_invoice(payment_request.payment_hash)
            except:
                pass
                # print("Exception while cancelling invoice")
