# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-15 07:15:28
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-09-02 12:48:30

from time import time
from threading import Thread

from kivy.properties import ObjectProperty
from kivy.properties import ListProperty
from kivy.properties import NumericProperty
from kivy.graphics.vertex_instructions import RoundedRectangle
from kivy.graphics.context_instructions import Color
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.clock import mainthread

from orb.math.Vector import Vector
from orb.audio.audio_manager import audio_manager
from orb.channels.segment import Segment
from orb.channels.fee_widget import FeeWidget
from orb.math.lerp import lerp_2d
from orb.misc.colors import *
from orb.misc.auto_obj import dict2obj
from orb.misc.prefs import pref

op = lambda: float(pref("display.channel_opacity"))


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
        self._selected = False
        self.ttl = 30
        self.memo = {}
        with self.canvas.before:
            self.line_local = Segment(
                amt_sat=int(self.channel.local_balance),
                width=self.width,
                color=self.local_col,
            )
            self.line_pending = Segment(
                width=self.width, color=self.pending_col, label=""
            )
            self.line_remote = Segment(width=self.width, color=self.remote_col)
            self.anim_col = Color(0.5, 1, 0.5, 1)
            self.anim_rect = RoundedRectangle(
                pos=[-1000, -1000], size=[0, 0], radius=[5]
            )

        self.a, self.b, self.c = [0, 0], [0, 0], [0, 0]

        self.bind(points=self.update)
        self.channel.bind(pending_htlcs=self.update)

        app = App.get_running_app()
        app.bind(selection=self.set_selected)
        app.bind(
            highlighter_updated=lambda *_: Thread(
                target=lambda: self.animate_highlight()
            ).start()
        )

        Clock.schedule_interval(self.animate_highlight, 10)

    @property
    def remote_col(self):
        s = self.selected
        return Colour(
            ("#7f7fcc"), active=self.channel.active, alpha=(op(), 1)[s], selected=s
        ).rgba

    @property
    def local_col(self):
        s = self.selected
        return Colour(
            "#7fcc7f", active=self.channel.active, alpha=(op(), 1)[s], selected=s
        ).rgba

    @property
    def pending_col(self):
        s = self.selected
        return Colour(
            "#ff7f7f", active=self.channel.active, alpha=(op(), 1)[s], selected=s
        ).rgba

    @property
    def selected(self):
        if self._selected:
            return self._selected
        highlighted = False
        app = App.get_running_app()
        if not hasattr(app, "store"):
            return
        h = app.store.get("highlighter", {})
        text = h.get("highlight", "")
        if text:
            present = text in self.memo
            expired = not present or (
                present and time() - self.memo[text][0] > self.ttl
            )
            if expired:
                try:
                    c = self.channel
                    highlighted = eval(text)
                except:
                    highlighted = False
                if type(highlighted) != bool:
                    highlighted = False
                self.memo[text] = (time(), highlighted)
                return highlighted
            else:
                return self.memo[text][1]
        return highlighted

    def set_selected(self, widget, channel):
        selected = channel == self.channel
        if selected != self._selected:
            self._selected = selected
            self.animate_highlight()

    def animate_highlight(self, *args):
        (Animation(rgba=self.remote_col, duration=0.2)).start(self.line_remote.color)
        (Animation(rgba=self.local_col, duration=0.2)).start(self.line_local.color)
        (Animation(rgba=self.pending_col, duration=0.2)).start(self.line_pending.color)

    @mainthread
    def update(self, *args):
        chan, line, trim = self.channel, self.points, 0.1
        ratio = int(chan.local_balance) / int(chan.capacity)

        # trim starting point so it doesn't overlap node
        a = lerp_2d(line[:2], line[2:], trim)
        # trim ending points so it doesn't overlap node
        b = lerp_2d(line[:2], line[2:], 1 - trim)

        # c is the 'center point' where local meets remote
        # (given there are no pending HTLCs)
        c = lerp_2d(a, b, ratio)

        # cb is where the remote line beings, i.e local + all pending
        cb = lerp_2d(
            a,
            b,
            ratio
            + (self.channel.pending_in + self.channel.pending_out) / int(chan.capacity),
        )
        self.line_local.line.points = [a[0], a[1], c[0], c[1]]

        # the pending line goes from where local ends, and remote starts
        self.line_pending.line.points = [c[0], c[1], cb[0], cb[1]]
        self.line_remote.line.points = [cb[0], cb[1], b[0], b[1]]
        self.to_fee.set_points(a, b, c)
        self.a, self.b, self.c = a, b, c
        self.line_local.update(amt_sat=self.channel.local_balance)
        self.line_pending.update()
        if pref("debug.htlcs"):
            in_ids = ", ".join(str(x) for x in self.channel.pending_in_htlc_ids)
            out_ids = ", ".join(str(x) for x in self.channel.pending_out_htlc_ids)
            text = ""
            if in_ids:
                text += f"in: {in_ids} "
            if out_ids:
                text += f"out: {out_ids}"
            self.line_pending.label.text = text
        else:
            self.line_pending.label.text = ""
        self.line_remote.update()

    def anim_outgoing(self, s=10):
        start, end = (
            self.c,
            self.b,
        )
        dist = max(
            int(Vector(start[0], start[1]).dist(Vector(end[0], end[1])) / 500), 1
        )
        anim = Animation(pos=start, size=(s, s), duration=0, t="in_quad")
        anim += Animation(pos=end, size=(s, s), duration=dist, t="in_quad")
        anim += Animation(pos=end, size=(1, 1), duration=0, t="in_quad")
        anim.start(self.anim_rect)
        anim = Animation(rgba=[0.5, 1, 0.5, 1], duration=0, t="in_quad")
        anim += Animation(rgba=[0.5, 1, 0.5, 1], duration=dist, t="in_quad")
        anim += Animation(rgba=[0.5, 1, 0.5, 0], duration=0, t="in_quad")
        anim.start(self.anim_col)

    def anim_incoming(self, s=10):
        start, end = (
            self.b,
            self.c,
        )
        dist = max(
            int(Vector(start[0], start[1]).dist(Vector(end[0], end[1])) / 500), 1
        )
        anim = Animation(pos=start, size=(s, s), duration=0, t="out_quad")
        anim += Animation(pos=end, size=(s, s), duration=dist, t="out_quad")
        anim.start(self.anim_rect)
        anim = Animation(rgba=[0.5, 1, 0.5, 1], duration=0, t="out_quad")
        anim += Animation(rgba=[0.5, 1, 0.5, 1], duration=dist, t="out_quad")
        anim += Animation(rgba=[0.5, 1, 0.5, 0], duration=0, t="out_quad")
        anim.start(self.anim_col)

    def anim_to_pos(self, points):
        Animation(points=points, duration=1).start(self)

    def anim_htlc(self, htlc):
        col = Colour("white").rgba
        send = htlc.event_type == "SEND"
        forward = htlc.event_type == "FORWARD"
        receive = htlc.event_type == "RECEIVE"
        event_outcome = htlc.event_outcome if hasattr(htlc, "event_outcome") else None
        settle = event_outcome == "settle_event"
        link_fail = event_outcome == "link_fail_event"
        forward_fail = event_outcome == "forward_fail_event"
        outgoing = htlc.outgoing_channel_id == self.channel.chan_id
        incoming = htlc.incoming_channel_id == self.channel.chan_id
        c = self.channel
        app = App.get_running_app()

        get_pending_outgoing_event = lambda htlc: next(
            (
                x
                for x in c.pending_htlcs
                if (not x.incoming) and x.htlc_index == htlc.outgoing_htlc_id
            ),
            None,
        )

        get_pending_incoming_event = lambda htlc: next(
            (
                x
                for x in c.pending_htlcs
                if (x.incoming) and x.htlc_index == htlc.incoming_htlc_id
            ),
            None,
        )

        if send and outgoing:
            if event_outcome == "forward_fail_event":
                col = [255 / 255.0, 71 / 255.0, 71 / 255.0, 0.6]  # Colour("red").rgba
                pending = get_pending_outgoing_event(htlc)
                # should always be there...
                if pending:
                    c.pending_htlcs.remove(pending)
                    c.local_balance += pending.amount
            elif event_outcome == "forward_event":
                col = [71 / 255.0, 71 / 255.0, 255 / 255.0, 0.6]
                self.anim_outgoing()
                if settle:
                    # this is likely unreachable code
                    assert False
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
                            htlc_index=htlc.outgoing_htlc_id,
                            outgoing_htlc_id=htlc.outgoing_htlc_id,
                        )
                    )
                    c.pending_htlcs.append(phtlc)
                    c.local_balance -= out_amt_sat
            elif event_outcome == "settle_event":
                col = [71 / 255.0, 71 / 255.0, 255 / 255.0, 0.6]
                self.anim_outgoing()
                audio_manager.play_send_settle()
                pending = get_pending_outgoing_event(htlc)
                if pending:
                    c.pending_htlcs.remove(pending)
                    c.remote_balance += pending.amount
            else:
                print(event_outcome)
        elif receive and incoming:
            self.anim_incoming()

        elif forward:
            if forward_fail:
                col = [255 / 255.0, 71 / 255.0, 71 / 255.0, 0.6]
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
                                htlc_index=htlc.outgoing_htlc_id,
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
                                htlc_index=htlc.incoming_htlc_id,
                                incoming_htlc_id=htlc.incoming_htlc_id,
                            )
                        )
                        self.channel.pending_htlcs.append(phtlc)
                        self.channel.remote_balance -= in_amt_sat
                self.anim_incoming()

        if link_fail:
            col = [255 / 255.0, 71 / 255.0, 71 / 255.0, 0.6]
            if hasattr(htlc, "wire_failure"):
                """
                Not yet available for REST
                """
                if htlc.link_fail_event.wire_failure == "TEMPORARY_CHANNEL_FAILURE":
                    if htlc.incoming_channel_id and htlc.outgoing_channel_id:
                        print("FAIL!")
                        outgoing_channel = app.channels.channels[
                            htlc.outgoing_channel_id
                        ]
                        print(outgoing_channel.alias)
                        print(htlc.__dict__)
                        if htlc.link_fail_event.failure_detail != "HTLC_EXCEEDS_MAX":
                            audio_manager.play_link_fail_event()

        # cols = {"forward_fail_event": RED, "link_fail_event": RED}
        # col = cols.get(htlc.event_outcome, WHITE)
        self.flash(col)
        self.update()

    def flash(self, rgba):
        (
            Animation(rgba=rgba, duration=0.2)
            + Animation(rgba=self.remote_col, duration=1)
        ).start(self.line_remote.color)

        (
            Animation(rgba=rgba, duration=0.2)
            + Animation(rgba=self.local_col, duration=1)
        ).start(self.line_local.color)

        (
            Animation(rgba=rgba, duration=0.2)
            + Animation(rgba=self.pending_col, duration=1)
        ).start(self.line_pending.color)
