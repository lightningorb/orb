from threading import Lock
from ui_actions import console_output
from output import *
from collections import Counter
from kivy.properties import NumericProperty
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Line
from kivy.uix.widget import Widget
import math
from channel_selector import *
from kivy.clock import Clock
from utils import pref
from threading import Thread
from pay_logic import pay_thread, PaymentStatus
from lerp import *

avoid = Counter()
LOOP = '021c97a90a411ff2b10dc2a8e32de2f29d2fa49d41bfbb52bd416e460db0747d0d'
GAMMA = '02769a851d7d11eaeaef899b2ed8c34fd387828fa13f6fe27928de2b9fa75a0cd8'
pk_ignore = set([LOOP, GAMMA])
chan_ignore = set([])


class Autobalance(Widget):
    radius = NumericProperty(350)

    def __init__(self, *args, **kwargs):
        super(Autobalance, self).__init__(*args, **kwargs)

        import data_manager

        self.lock = Lock()
        self.drag_start = False
        self.output = Output(None)
        self.output.lnd = data_manager.data_man.lnd
        with self.canvas:
            Color(0.1, 0.1, 0.2, 0),  # (1 if pref('autobalance.enable') else 0))
            self.circle = Line(pos=self.pos, circle=(0, 0, self.radius))
        self.bind(radius=self.update_rect)
        Clock.schedule_interval(
            lambda _: Thread(target=self.do_rebalancing).start(), 15
        )

    def update_rect(self, *args):
        self.circle.circle = (0, 0, self.radius)

    def on_touch_down(self, touch):
        dist = math.sqrt(touch.pos[0] ** 2 + touch.pos[1] ** 2)
        epsilon = 5
        if abs(dist - self.radius) < epsilon:
            self.drag_start = True
            return True
        return super(Autobalance, self).on_touch_down(touch)

    def on_touch_move(self, touch):
        if self.drag_start:
            self.radius = math.sqrt(touch.pos[0] ** 2 + touch.pos[1] ** 2)
        return super(Autobalance, self).on_touch_move(touch)

    def on_touch_up(self, touch):
        if self.drag_start:
            self.drag_start = False
            return True
        return super(Autobalance, self).on_touch_up(touch)

    @property
    def ratio(self):
        return self.radius / pref('display.channel_length')

    def do_rebalancing(self, *args):
        if not pref('autobalance.enable'):
            return
        if self.lock.locked():
            return
        self.lock.acquire()
        self.is_rebalancing = True
        print('--------------')
        print(self.ratio)
        from data_manager import data_man

        lnd = data_man.lnd
        avoid = set([])
        num_sats = 100_000
        outbound_channel = get_low_inbound_channel(
            lnd=lnd,
            avoid=avoid,
            pk_ignore=pk_ignore,
            chan_ignore=chan_ignore,
            num_sats=num_sats,
            ratio=self.ratio,
        )
        inbound_channel, inbound_pubkey = get_low_outbound_channel(
            lnd=lnd,
            avoid=avoid,
            pk_ignore=pk_ignore,
            chan_ignore=chan_ignore,
            num_sats=num_sats,
            ratio=1 - self.ratio,
        )
        print('out', outbound_channel)
        print('in ', inbound_channel)

        self.is_rebalancing = False

        payment_request = data_man.lnd.generate_invoice(
            memo='rebalance', amount=num_sats
        )

        _, _, status = pay_thread(
            inst=self,
            thread_n=0,
            fee_rate=int(100),
            payment_request=payment_request,
            payment_request_raw=None,
            outgoing_chan_id=outbound_channel,
            last_hop_pubkey=inbound_pubkey,
            max_paths=100,
        )
        if not status == PaymentStatus.success:
            lnd.cancel_invoice(payment_request.payment_hash)

        print("Autorebalance - done")
        self.lock.release()
