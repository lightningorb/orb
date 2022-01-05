# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-15 07:15:28
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-01-06 01:06:31

from kivy.properties import ObjectProperty
from kivy.properties import ListProperty
from kivy.properties import NumericProperty
from kivy.graphics.vertex_instructions import RoundedRectangle
from kivy.graphics.context_instructions import Color

from kivy.uix.widget import Widget
from orb.audio.audio_manager import audio_manager
from orb.channels.segment import Segment

from orb.channels.fee_widget import FeeWidget
from orb.math.lerp import lerp_2d
from kivy.animation import Animation
from orb.misc.colors import *
from orb.misc.prefs import inverted_channels


class ChannelWidget(Widget):
    """
    This is the Channel line ------------ between two nodes.
    The actual line Segments are implemented by the Segment class.
    It also handles animating the 1M sat circles as HTLCs occur,
    and flashing the channel.
    """

    #: the channel object
    channel = ObjectProperty("")

    #: where the channel starts and ends
    points = ListProperty([0, 0, 0, 0])

    #: the girth of the channel
    width = NumericProperty(0)

    def __init__(self, **kwargs):
        super(ChannelWidget, self).__init__(**kwargs)
        self.to_fee = FeeWidget(channel=self.channel)
        self.add_widget(self.to_fee)
        self.anim_rectangles = []

        self.pending_in = sum(
            int(p.amount) for p in self.channel.pending_htlcs if p.incoming
        )
        self.pending_out = sum(
            int(p.amount) for p in self.channel.pending_htlcs if not p.incoming
        )

        with self.canvas.before:
            self.line_local = Segment(
                amt_sat=int(self.channel.local_balance), width=self.width, color=GREEN
            )
            self.line_pending = Segment(width=self.width, color=ORANGE)
            self.line_remote = Segment(width=self.width, color=BLUE)
            self.anim_col = Color(0.5, 1, 0.5, 1)
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

        lerp a, b, ratio - pending/cap      lerp a, b, ratio + pending/cap

        """

        self.pending_in = sum(
            int(p.amount) for p in self.channel.pending_htlcs if p.incoming
        )
        self.pending_out = sum(
            int(p.amount) for p in self.channel.pending_htlcs if not p.incoming
        )

        chan, line, trim = self.channel, self.points, 0.1
        ratio = int(chan.local_balance) / int(chan.capacity)

        # trim starting point so it doesn't overlap node
        a = lerp_2d(line[:2], line[2:], trim)
        # trim ending points so it doesn't overlap node
        b = lerp_2d(line[:2], line[2:], 1 - trim)

        # c is the 'center point' where local meets remote
        # (given there are no pending HTLCs)
        c = lerp_2d(a, b, ratio + (self.pending_out / chan.capacity))

        # ca is where the local line ends, minus pending out HTLC amounts
        # e.g the outbound that's actually available
        ca = lerp_2d(a, b, ratio)

        # cb is where the remote line beings, i.e local + all pending
        cb = lerp_2d(
            a, b, ratio + (self.pending_in + self.pending_out) / int(chan.capacity)
        )
        self.line_local.line.points = [a[0], a[1], ca[0], ca[1]]

        # the pending line goes from where local ends, and remote starts
        self.line_pending.line.points = [ca[0], ca[1], cb[0], cb[1]]
        self.line_remote.line.points = [cb[0], cb[1], b[0], b[1]]
        self.to_fee.set_points(a, b, c)
        self.a, self.b, self.c = a, b, c
        self.line_local.update_rect(amt_sat=self.channel.local_balance)
        self.line_pending.update_rect()
        self.line_remote.update_rect()

    def anim_outgoing(self, s=10):
        start, end = (
            self.c,
            self.b,
        )
        anim = Animation(pos=start, size=(s, s), duration=0)
        anim += Animation(pos=end, size=(s, s), duration=0.4)
        anim += Animation(pos=end, size=(1, 1), duration=0)
        anim.start(self.anim_rect)
        anim = Animation(rgba=[0.5, 1, 0.5, 1], duration=0)
        anim += Animation(rgba=[0.5, 1, 0.5, 1], duration=0.4)
        anim += Animation(rgba=[0.5, 1, 0.5, 0], duration=0)
        anim.start(self.anim_col)

    def anim_incoming(self, s=10):
        start, end = (
            self.b,
            self.c,
        )
        anim = Animation(pos=start, size=(s, s), duration=0)
        anim += Animation(pos=end, size=(s, s), duration=0.4)
        anim.start(self.anim_rect)
        anim = Animation(rgba=[0.5, 1, 0.5, 1], duration=0)
        anim += Animation(rgba=[0.5, 1, 0.5, 1], duration=0.4)
        anim += Animation(rgba=[0.5, 1, 0.5, 0], duration=0)
        anim.start(self.anim_col)

    def anim_to_pos(self, points):
        Animation(points=points, duration=1).start(self)

    def anim_htlc(self, htlc):
        send = htlc.event_type == "SEND"
        forward = htlc.event_type == "FORWARD"
        receive = htlc.event_type == "RECEIVE"
        if receive:
            pass
        settle = htlc.event_outcome == "settle_event"
        fail = htlc.event_outcome == "link_fail_event"
        outgoing = (
            hasattr(htlc, "outgoing_channel_id")
            and htlc.outgoing_channel_id == self.channel.chan_id
        )
        incoming = (
            forward or receive
        ) and htlc.incoming_channel_id == self.channel.chan_id

        if send and outgoing:
            self.anim_outgoing()
        elif receive:
            self.anim_incoming()
        elif forward:
            if outgoing:
                self.anim_outgoing()
            else:
                self.anim_incoming()

        if send and settle:
            audio_manager.play_send_settle()
        elif (forward or receive) and settle:
            if forward:
                audio_manager.play_forward_settle()
        elif fail:
            if htlc.wire_failure == "TEMPORARY_CHANNEL_FAILURE":
                if htlc.incoming_channel_id and htlc.outgoing_channel_id:
                    print("FAIL!")
                    print(htlc.__dict__)
                    if htlc.failure_detail != "HTLC_EXCEEDS_MAX":
                        audio_manager.play_link_fail_event()

        self.update_rect()

        cols = {"forward_fail_event": RED, "link_fail_event": RED}
        col = cols.get(htlc.event_outcome, WHITE)
        (Animation(rgba=col, duration=0.2) + Animation(rgba=BLUE, duration=1)).start(
            self.line_remote.color
        )

        (Animation(rgba=col, duration=0.2) + Animation(rgba=GREEN, duration=1)).start(
            self.line_local.color
        )
