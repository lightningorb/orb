# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-15 07:15:28
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-01-30 16:43:47

from kivy.properties import ObjectProperty
from kivy.properties import ListProperty
from kivy.properties import NumericProperty
from kivy.graphics.vertex_instructions import RoundedRectangle
from kivy.graphics.context_instructions import Color

from kivy.uix.widget import Widget
from kivy.animation import Animation

from orb.audio.audio_manager import audio_manager
from orb.channels.segment import Segment
from orb.channels.fee_widget import FeeWidget
from orb.math.lerp import lerp_2d
from orb.misc.colors import *
from orb.misc.auto_obj import dict2obj


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

        self.bind(points=self.update)

    def update(self, *args):
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
        self.line_local.update(amt_sat=self.channel.local_balance)
        self.line_pending.update()
        self.line_remote.update()

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
        col = WHITE
        send = htlc.event_type == "SEND"
        forward = htlc.event_type == "FORWARD"
        receive = htlc.event_type == "RECEIVE"
        if receive:
            pass
        settle = htlc.event_outcome == "settle_event"
        link_fail = htlc.event_outcome == "link_fail_event"
        forward_fail = htlc.event_outcome == "forward_fail_event"
        outgoing = htlc.outgoing_channel_id == self.channel.chan_id
        c = self.channel

        get_pending_outgoing_event = lambda html: next(
            (
                x
                for x in c.pending_htlcs
                if (not x.incoming)
                and hasattr(x, "outgoing_htlc_id")
                and x.outgoing_htlc_id == htlc.outgoing_htlc_id
            ),
            None,
        )

        get_pending_incoming_event = lambda html: next(
            (
                x
                for x in c.pending_htlcs
                if (x.incoming)
                and hasattr(x, "incoming_htlc_id")
                and x.incoming_htlc_id == htlc.incoming_htlc_id
            ),
            None,
        )

        if send and outgoing:
            if htlc.event_outcome == "forward_fail_event":
                col = RED_FULL
                pending = get_pending_outgoing_event(htlc)
                if pending:
                    c.pending_htlcs.remove(pending)
                    c.local_balance += pending.amount
            else:
                col = BLUE_FULL
                self.anim_outgoing()
                if settle:
                    audio_manager.play_send_settle()
                    pending = get_pending_outgoing_event(htlc)
                    if pending:
                        c.pending_htlcs.remove(pending)
                        c.remote_balance += pending.amount
                else:
                    out_amt_sat = int(
                        htlc.event_outcome_info["outgoing_amt_msat"] / 1_000
                    )
                    phtlc = dict2obj(
                        dict(
                            incoming=False,
                            amount=out_amt_sat,
                            outgoing_htlc_id=htlc.outgoing_htlc_id,
                        )
                    )
                    c.pending_htlcs.append(phtlc)
                    c.local_balance -= out_amt_sat
        elif receive:
            self.anim_incoming()
        elif forward:
            if forward_fail:
                col = RED_FULL
            if outgoing:
                if forward_fail:
                    pending = get_pending_outgoing_event(htlc)
                    if pending:
                        c.pending_htlcs.remove(pending)
                        c.local_balance += pending.amount
                else:
                    if settle:
                        audio_manager.play_forward_settle()
                        pending = get_pending_outgoing_event(htlc)
                        if pending:
                            c.pending_htlcs.remove(pending)
                            c.remote_balance += pending.amount
                    else:
                        out_amt_sat = int(
                            htlc.event_outcome_info["outgoing_amt_msat"] / 1_000
                        )
                        phtlc = dict2obj(
                            dict(
                                incoming=False,
                                amount=out_amt_sat,
                                outgoing_htlc_id=htlc.outgoing_htlc_id,
                            )
                        )
                        self.channel.pending_htlcs.append(phtlc)
                        self.channel.local_balance -= out_amt_sat
                self.anim_outgoing()
            else:
                if forward_fail:
                    pending = get_pending_incoming_event(htlc)
                    if pending:
                        c.pending_htlcs.remove(pending)
                        c.remote_balance += pending.amount
                else:
                    if settle:
                        pending = get_pending_incoming_event(htlc)
                        if pending:
                            c.pending_htlcs.remove(pending)
                            c.local_balance += pending.amount
                    else:
                        in_amt_sat = int(
                            htlc.event_outcome_info["incoming_amt_msat"] / 1_000
                        )
                        phtlc = dict2obj(
                            dict(
                                incoming=True,
                                amount=in_amt_sat,
                                incoming_htlc_id=htlc.incoming_htlc_id,
                            )
                        )
                        self.channel.pending_htlcs.append(phtlc)
                        self.channel.remote_balance -= in_amt_sat
                self.anim_incoming()

        if link_fail:
            col = RED_FULL
            if hasattr(htlc, "wire_failure"):
                """
                Not yet available for REST
                """
                if htlc.wire_failure == "TEMPORARY_CHANNEL_FAILURE":
                    if htlc.incoming_channel_id and htlc.outgoing_channel_id:
                        print("FAIL!")
                        print(htlc.__dict__)
                        if htlc.failure_detail != "HTLC_EXCEEDS_MAX":
                            audio_manager.play_link_fail_event()

        # cols = {"forward_fail_event": RED, "link_fail_event": RED}
        # col = cols.get(htlc.event_outcome, WHITE)
        self.flash(col)
        self.update()

    def flash(self, rgba):
        (Animation(rgba=rgba, duration=0.2) + Animation(rgba=BLUE, duration=1)).start(
            self.line_remote.color
        )

        (Animation(rgba=rgba, duration=0.2) + Animation(rgba=GREEN, duration=1)).start(
            self.line_local.color
        )
