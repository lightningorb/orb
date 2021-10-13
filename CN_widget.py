from kivy.properties import ObjectProperty
import math
from kivy.uix.widget import Widget
from channel_widget import ChannelWidget
from node import Node
import data_manager


class CNWidget(Widget):
    attribute_editor = ObjectProperty(None)

    def __init__(self, c, caps, attribute_editor, *args):
        super(CNWidget, self).__init__(*args)
        self.attribute_editor = attribute_editor
        self.radius = 600
        lnd = data_manager.data_man.lnd
        self.l = ChannelWidget(points=[0, 0, 0, 0], channel=c, width=caps[c.chan_id])
        self.b = Node(
            text=lnd.get_node_alias(c.remote_pubkey),
            channel=c,
            attribute_editor=attribute_editor,
        )
        self.add_widget(self.b)
        self.add_widget(self.l)

    def update_rect(self, w_2, h_2, i, n):
        x = math.sin(i / n * 3.14378 * 2) * self.radius + w_2
        y = math.cos(i / n * 3.14378 * 2) * self.radius + h_2
        self.l.points = [w_2, h_2, x, y]
        self.b.pos = (x - (70 / 2), y - (100 / 2))
