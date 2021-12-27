# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-15 07:15:28
# @Last Modified by:   lnorb.com
# @Last Modified time: 2021-12-28 04:45:35

from threading import Lock
from orb.misc.output import *
from collections import Counter
from kivy.properties import NumericProperty
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Line
from kivy.uix.widget import Widget
import math
from orb.logic.channel_selector import *
from kivy.clock import Clock
from orb.misc.utils import pref
from threading import Thread
from orb.logic.pay_logic import pay_thread, PaymentStatus

LOOP = "021c97a90a411ff2b10dc2a8e32de2f29d2fa49d41bfbb52bd416e460db0747d0d"
GAMMA = "02769a851d7d11eaeaef899b2ed8c34fd387828fa13f6fe27928de2b9fa75a0cd8"
pk_ignore = set([LOOP, GAMMA])
chan_ignore = set([])


class Autobalance(Widget):
    radius = NumericProperty(350)

    def __init__(self, *args, **kwargs):
        super(Autobalance, self).__init__(*args, **kwargs)

        import data_manager

        self.ratio = 0.5
        self.lock = Lock()
        self.drag_start = False
        self.output = Output(None)
        self.output.lnd = data_manager.data_man.lnd
        Clock.schedule_interval(
            lambda _: Thread(target=self.do_rebalancing).start(), 15
        )

    def do_rebalancing(self, *args):
        if not pref("autobalance.enable"):
            return
        if self.lock.locked():
            return
        self.lock.acquire()
        self.is_rebalancing = True
        print("--------------")
        print(self.ratio)
        from data_manager import data_man

        lnd = data_man.lnd
        num_sats = 100_000
        outbound_channel = get_low_inbound_channel(
            lnd=lnd, pk_ignore=pk_ignore, chan_ignore=chan_ignore, num_sats=num_sats
        )
        inbound_pubkey = (
            "033d8656219478701227199cbd6f670335c8d408a92ae88b962c49d4dc0e83e025"
        )
        # outbound_channel = 781406421302444032
        # inbound_channel, inbound_pubkey = get_low_outbound_channel(
        #     lnd=lnd,
        #     pk_ignore=pk_ignore,
        #     chan_ignore=chan_ignore,
        #     num_sats=num_sats,
        #     ratio=1 - self.ratio,
        # )
        print("out", outbound_channel)
        print("in ", inbound_pubkey)

        self.is_rebalancing = False

        raw, payment_request = data_man.lnd.generate_invoice(
            memo="rebalance", amount=num_sats
        )

        def stopped():
            pass

        status = pay_thread(
            inst=self,
            stopped=stopped,
            thread_n=0,
            fee_rate=int(400),
            payment_request=payment_request,
            payment_request_raw=raw,
            outgoing_chan_id=outbound_channel,
            last_hop_pubkey=inbound_pubkey,
            max_paths=1000,
        )
        if not status == PaymentStatus.success:
            try:
                lnd.cancel_invoice(payment_request.payment_hash)
            except:
                print("Exception while cancelling invoice")

        print("Autorebalance - done")
        self.lock.release()
