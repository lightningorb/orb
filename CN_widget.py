from kivy.properties import ObjectProperty
import math
from kivy.uix.widget import Widget
from channel_widget import ChannelWidget
from node import Node
import data_manager
from sent_received_widget import SentReceivedWidget


class CNWidget(Widget):
    attribute_editor = ObjectProperty(None)

    def __init__(self, c, caps, attribute_editor, *args):
        super(CNWidget, self).__init__(*args)
        self.attribute_editor = attribute_editor
        self.radius = 600
        lnd = data_manager.data_man.lnd
        self.l = ChannelWidget(points=[0, 0, 0, 0], channel=c, width=caps[c.chan_id])
        self.b = Node(
            text="",
            channel=c,
            attribute_editor=attribute_editor,
        )
        self.sent_received_widget = SentReceivedWidget(channel=c)
        self.add_widget(self.sent_received_widget)
        self.add_widget(self.b)
        self.add_widget(self.l)

    def update_rect(self, i, n):
        x = math.sin(i / n * 3.14378 * 2) * self.radius
        y = math.cos(i / n * 3.14378 * 2) * self.radius
        points = [0, 0, x, y]
        pos = (x - (70 / 2), y - (100 / 2))
        if self.l.points == [0, 0, 0, 0]:
            self.l.points = points
            self.b.pos = pos
        else:
            self.l.anim_to_pos(points)
            self.b.anim_to_pos(pos)
        self.sent_received_widget.update_rect(x, y)
