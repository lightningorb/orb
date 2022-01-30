# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-15 07:15:28
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-01-30 16:44:38
import math

from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.widget import Widget

from orb.channels.channel_widget import ChannelWidget
from orb.widgets.node import Node
from orb.widgets.sent_received_widget import SentReceivedWidget
from orb.misc.utils import pref
from orb.misc.prefs import inverted_channels
from kivy.gesture import Gesture


class CNWidget(Widget):
    def __init__(self, c, caps, *args):
        super(CNWidget, self).__init__(*args)
        self.l = ChannelWidget(points=[0, 0, 0, 0], channel=c, width=caps[c.chan_id])
        self.c = c
        self.b = Node(text="", channel=c)
        self.gesture_in = None
        self.gesture_out = None
        self.show_sent_received = (
            App.get_running_app().config["display"]["show_sent_received"] == "1"
        )
        self.sent_received_widget = None
        if self.show_sent_received:
            self.sent_received_widget = SentReceivedWidget(channel=c)
            self.add_widget(self.sent_received_widget)
        self.add_widget(self.l)
        self.add_widget(self.b)

    def update(self, i, n):
        self.radius = int(App.get_running_app().config["display"]["channel_length"])
        x = math.sin(i / n * 3.14378 * 2) * self.radius
        y = math.cos(i / n * 3.14378 * 2) * self.radius
        points = [x, y, 0, 0] if inverted_channels() else [0, 0, x, y]
        pos = (
            x - (pref("display.node_width") / 2),
            y - (pref("display.node_height") / 2),
        )
        if not self.gesture_in:
            self.gesture_in = Gesture()
            self.gesture_out = Gesture()
            self.gesture_in.name = self.c.chan_id
            self.gesture_out.name = self.c.chan_id
            stroke = [(x * (f / 100), y * (f / 100)) for f in range(100)]
            self.gesture_in.add_stroke(stroke)
            self.gesture_out.add_stroke(stroke[::-1])
            self.gesture_in.normalize()
            self.gesture_out.normalize()
        if self.l.points == [0, 0, 0, 0]:
            self.l.points = points
            self.b.pos = pos
        else:
            self.l.anim_to_pos(points)
            self.b.anim_to_pos(pos)
        if self.show_sent_received and self.sent_received_widget:
            self.sent_received_widget.anim_to_pos((i / n), self.radius)
