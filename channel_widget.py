# import numpy as np
import data_manager
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import RoundedRectangle, Line
from kivy.properties import NumericProperty
from kivy.properties import ObjectProperty
from kivy.properties import ListProperty
from kivy.uix.widget import Widget
from audio_manager import audio_manager

try:
    from numpy.linalg import norm
    import numpy as np
except:
    pass

from HUD import *
from fee_widget import FeeWidget
from lerp import *
from kivy.animation import Animation

RED = [1, 0.5, 0.5, 1]
WHITE = [1, 1, 1, 1]
BLUE = [0.5, 0.5, 1, 1]
GREEN = [0.5, 1, 0.5, 1]
ORANGE = [1, 1, 0.5, 1]


class ChannelWidget(Widget):
    """
    This is the Channel line ------------ between two nodes.
    """

    local_line_col = ObjectProperty(None)
    remote_line_col = ObjectProperty(None)
    channel = ObjectProperty("")
    points = ListProperty([0, 0, 0, 0])
    width = NumericProperty(0)

    # def on_touch_down(self, touch):
    #     Widget.on_touch_down(self, touch)
    #     p1 = np.array(self.a)
    #     p2 = np.array(self.b)
    #     p3 = np.array(touch.pos)
    #     d = np.cross(p2 - p1, p3 - p1) / np.linalg.norm(p2 - p1)
    #     line_width = (self.width, 7)[abs(d) < 10]
    #     self.line_local.width = line_width
    #     self.line_remote.width = line_width

    def __init__(self, **kwargs):
        super(ChannelWidget, self).__init__(**kwargs)
        lnd = data_manager.data_man.lnd
        self.to_fee = FeeWidget(channel=self.channel)
        self.add_widget(self.to_fee)
        self.anim_rectangles = []

        self.pending_in = sum(
            p.amount for p in self.channel.pending_htlcs if p.incoming
        )
        self.pending_out = sum(
            p.amount for p in self.channel.pending_htlcs if not p.incoming
        )

        with self.canvas.before:
            self.local_line_col = Color(*GREEN)
            self.line_local = Line(points=[0, 0, 0, 0], width=self.width)
            Color(*ORANGE)
            self.line_pending = Line(points=[0, 0, 0, 0], width=self.width)
            self.remote_line_col = Color(*BLUE)
            self.line_remote = Line(points=[0, 0, 0, 0], width=self.width)
            Color(0.5, 1, 0.5, 1)
            self.anim_rect = RoundedRectangle(
                pos=[-1000, -1000], size=[0, 0], radius=[5]
            )

        self.a, self.b, self.c = [0, 0], [0, 0], [0, 0]

        self.bind(points=self.update_rect)

    def update_rect(self, *args):
        """
        CAPACITY: 1,000,000
        LOCAL: 3,000,000
        REMOTE: 7,000,000
        PENDING IN:  500,000
        PENDING OUT: 300,000

        LOCAL                                                           REMOTE
        |                  |                                                |
        |-----------|------|----|-------------------------------------------|
        |                  |                                                |
        a          ca      c    cb                                          b

            lerp a, b, r - pending/cap      lerp a, b, r + pending/cap

        """
        chan, p = self.channel, self.points
        trim = 0.1
        r = int(chan.local_balance) / int(chan.capacity)
        a = lerp_2d(p[:2], p[2:], trim)
        b = lerp_2d(p[:2], p[2:], 1 - trim)
        c = lerp_2d(a, b, r)
        ca = lerp_2d(a, b, r - self.pending_out / int(chan.capacity))
        cb = lerp_2d(a, b, r + self.pending_in / int(chan.capacity))
        self.line_local.points = [a[0], a[1], ca[0], ca[1]]
        self.line_pending.points = [ca[0], ca[1], cb[0], cb[1]]
        self.line_remote.points = [cb[0], cb[1], b[0], b[1]]
        self.to_fee.set_points(a, b, c)
        self.a, self.b, self.c = a, b, c

    def anim_outgoing(self, s=10):
        anim = Animation(pos=self.c, size=(0, 0), duration=0)
        anim += Animation(pos=self.c, size=(0, 0), duration=0.4)
        anim += Animation(size=(s, s), duration=0)
        anim += Animation(pos=self.b, duration=0.4)
        anim += Animation(pos=(-1000, -1000), duration=0)
        anim.start(self.anim_rect)

    def anim_incoming(self, s=10):
        anim = Animation(pos=self.b, size=(s, s), duration=0)
        anim += Animation(pos=self.c, duration=0.4)
        anim += Animation(size=(0, 0), duration=0.1)
        anim += Animation(pos=(-1000, -1000), duration=0.1)
        anim.start(self.anim_rect)

    def anim_htlc(self, htlc):
        send = htlc.event_type == "SEND"
        forward = htlc.event_type == "FORWARD"
        settle = htlc.event_outcome == "settle_event"
        fail = htlc.event_outcome == "link_fail_event"
        outgoing = htlc.outgoing_channel_id == self.channel.chan_id
        incoming = forward and htlc.incoming_channel_id == self.channel.chan_id

        if incoming:
            self.pending_in = htlc.incoming_channel_pending_htlcs["pending_in"]
            self.pending_out = htlc.incoming_channel_pending_htlcs["pending_out"]
        if outgoing:
            self.pending_in = htlc.outgoing_channel_pending_htlcs["pending_in"]
            self.pending_out = htlc.outgoing_channel_pending_htlcs["pending_out"]

        if send and outgoing:
            self.anim_outgoing()
        elif forward:
            if outgoing:
                self.anim_outgoing()
            else:
                self.anim_incoming()

        if send and settle:
            audio_manager.play_send_settle()
            self.channel.local_balance = htlc.outgoing_channel_local_balance
            self.channel.remote_balance = htlc.outgoing_channel_remote_balance
        elif forward and settle:
            audio_manager.play_forward_settle()
            if htlc.outgoing_channel_id == self.channel.chan_id:
                self.channel.local_balance = htlc.outgoing_channel_local_balance
                self.channel.remote_balance = htlc.outgoing_channel_remote_balance
            if htlc.incoming_channel_id == self.channel.chan_id:
                self.channel.local_balance = htlc.incoming_channel_local_balance
                self.channel.remote_balance = htlc.incoming_channel_remote_balance
        elif fail:
            if htlc.wire_failure in ["FEE_INSUFFICIENT"]:
                pass
            else:
                print("FAIL!")
                print(htlc.__dict__)
                audio_manager.play_link_fail_event()

        self.update_rect()

        cols = {
            "forward_fail_event": RED,
            "link_fail_event": RED,
        }
        col = cols.get(htlc.event_outcome, WHITE)
        (Animation(rgba=col, duration=0.2) + Animation(rgba=BLUE, duration=1)).start(
            self.remote_line_col
        )

        (Animation(rgba=col, duration=0.2) + Animation(rgba=GREEN, duration=1)).start(
            self.local_line_col
        )
