# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-28 08:26:04
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-01-11 11:03:59

import threading
from traceback import print_exc

from orb.logic.channel_selector import get_low_inbound_channel
from orb.logic.channel_selector import get_low_outbound_channel
from orb.logic.pay_logic import pay_thread, PaymentStatus
from orb.logic.thread_manager import thread_manager
from orb.lnd import Lnd


class RebalanceThread(threading.Thread):
    def __init__(
        self,
        amount,
        chan_id,
        last_hop_pubkey,
        max_paths,
        fee_rate,
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
        self.name = name
        self.thread_n = thread_n
        self.lnd = Lnd()
        thread_manager.add_thread(self)

    def run(self):
        try:
            self.__run()
        except:
            print_exc()
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

        if self.last_hop_pubkey:
            print(f"Last hop pubkey is: {self.last_hop_pubkey}")
        if not self.last_hop_pubkey:
            _, self.last_hop_pubkey = get_low_outbound_channel(
                lnd=self.lnd,
                pk_ignore=[],
                chan_ignore=[],
                num_sats=self.amount,
            )
            print(f"Last hop pubkey not set, so selected one: {self.last_hop_pubkey}")

        raw, payment_request = self.lnd.generate_invoice(
            memo="rebalance", amount=self.amount
        )
        status = pay_thread(
            stopped=self.stopped,
            thread_n=0,
            fee_rate=self.fee_rate,
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
