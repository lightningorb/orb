# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-15 07:15:28
# @Last Modified by:   lnorb.com
# @Last Modified time: 2021-12-21 08:13:39
from kivy.properties import ObjectProperty
from kivy.uix.widget import Widget
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Line

from orb.math.Vector import Vector


class SentReceivedWidget(Widget):
    channel = ObjectProperty(None)

    def __init__(self, channel, *args, **kwargs):
        super(SentReceivedWidget, self).__init__(*args, **kwargs)
        from orb.store import model

        self.channel = channel
        c = self.channel
        self.received = (
            sum(
                [
                    x.amt_in
                    for x in model.FowardEvent()
                    .select()
                    .where(model.FowardEvent.chan_id_in == str(c.chan_id))
                ]
            )
            / 1e8
        )
        self.sent = (
            sum(
                [
                    x.amt_in
                    for x in model.FowardEvent()
                    .select()
                    .where(model.FowardEvent.chan_id_out == str(c.chan_id))
                ]
            )
            / 1e8
        )
        with self.canvas:
            Color(*[0.5, 1, 0.5, 1])
            self.sent_line = Line(points=[0, 0, 0, 0], width=2)
            Color(*[0.5, 0.5, 1, 1])
            self.received_line = Line(points=[0, 0, 0, 0], width=2)

    def update_rect(self, x, y):
        offset = 0.1
        x += x * offset
        y += y * offset
        sa = Vector(x, y)
        sb = Vector(x + x * self.sent, y + y * self.sent)
        ra = Vector(x, y)
        rb = Vector(x + x * self.received, y + y * self.received)
        sAB_norm = (sa - sb).perp().normalized() * 10
        sP1 = sa + sAB_norm
        sP2 = sb + sAB_norm
        self.sent_line.points = [sP1.x, sP1.y, sP2.x, sP2.y]
        rAB_norm = (ra - rb).perp().normalized() * 10
        rP1 = ra - rAB_norm
        rP2 = rb - rAB_norm
        self.received_line.points = [rP1.x, rP1.y, rP2.x, rP2.y]
