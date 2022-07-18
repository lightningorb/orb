# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-28 08:26:04
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-01-11 11:03:59

import threading
from traceback import format_exc

from orb.logic.channel_selector import get_low_inbound_channel
from orb.logic.channel_selector import get_low_outbound_channel
from orb.logic.pay_logic import pay_thread, PaymentStatus
from orb.logic.thread_manager import thread_manager
from orb.misc import data_manager
from orb.lnd import Lnd


class RebalanceThread(threading.Thread):
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
        *args,
        **kwargs,
    ):
        super(RebalanceThread, self).__init__(*args, **kwargs)
        self._stop_event = threading.Event()
        self.amount = amount
        self.chan_id = chan_id
        self.last_hop_pubkey = last_hop_pubkey
        self.max_paths = max_paths
        self.fee_rate = fee_rate
        self.time_pref = time_pref
        self.name = name
        self.thread_n = thread_n
        self.lnd = Lnd()
        thread_manager.add_thread(self)

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
                lnd=self.lnd,
                pk_ignore=[],
                chan_ignore=[],
                num_sats=self.amount,
            )

        if not self.last_hop_pubkey:
            _, self.last_hop_pubkey = get_low_outbound_channel(
                lnd=self.lnd,
                pk_ignore=[],
                chan_ignore=[],
                num_sats=self.amount,
            )

        from_pk = data_manager.data_man.channels.channels[self.chan_id].remote_pubkey
        from_alias = Lnd().get_node_alias(from_pk)
        to_alias = Lnd().get_node_alias(self.last_hop_pubkey)

        print(f"Rebalancing {self.amount} from {from_alias} to {to_alias}")

        raw, payment_request = self.lnd.generate_invoice(
            memo="rebalance", amount=self.amount
        )
        status = pay_thread(
            stopped=self.stopped,
            thread_n=0,
            fee_rate=self.fee_rate,
            time_pref=self.time_pref,
            payment_request=payment_request,
            payment_request_raw=raw,
            outgoing_chan_id=self.chan_id,
            last_hop_pubkey=self.last_hop_pubkey,
            max_paths=self.max_paths,
        )

        if not status == PaymentStatus.success:
            try:
                self.lnd.cancel_invoice(payment_request.payment_hash)
            except:
                pass
                # print("Exception while cancelling invoice")

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()
