import math

from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.widget import Widget

from orb.channels.channel_widget import ChannelWidget
from orb.widgets.node import Node
from orb.widgets.sent_received_widget import SentReceivedWidget
from orb.misc.utils import pref
from orb.misc.prefs import inverted_channels

import data_manager

class CNWidget(Widget):
    attribute_editor = ObjectProperty(None)

    def __init__(self, c, caps, attribute_editor, *args):
        super(CNWidget, self).__init__(*args)
        self.attribute_editor = attribute_editor
        lnd = data_manager.data_man.lnd
        self.l = ChannelWidget(points=[0, 0, 0, 0], channel=c, width=caps[c.chan_id])
        self.b = Node(text="", channel=c, attribute_editor=attribute_editor)
        self.show_sent_received = (
            App.get_running_app().config["display"]["show_sent_received"] == "1"
        )
        self.sent_received_widget = None
        if self.show_sent_received:
            self.sent_received_widget = SentReceivedWidget(channel=c)
            self.add_widget(self.sent_received_widget)
        self.add_widget(self.l)
        self.add_widget(self.b)

    def update_rect(self, i, n):
        self.radius = int(App.get_running_app().config["display"]["channel_length"])
        x = math.sin(i / n * 3.14378 * 2) * self.radius
        y = math.cos(i / n * 3.14378 * 2) * self.radius
        points = [x, y, 0, 0] if inverted_channels() else [0, 0, x, y]
        pos = (
            x - (pref('display.node_width') / 2),
            y - (pref('display.node_height') / 2),
        )
        if self.l.points == [0, 0, 0, 0]:
            self.l.points = points
            self.b.pos = pos
        else:
            self.l.anim_to_pos(points)
            self.b.anim_to_pos(pos)
        if self.show_sent_received and self.sent_received_widget:
            self.sent_received_widget.update_rect(x, y)
