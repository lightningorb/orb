import math
from kivy.graphics import InstructionGroup
from kivy.properties import ListProperty
from kivy.uix.scatter import Scatter
from kivy.uix.button import Button
from kivy.properties import ObjectProperty
import data_manager
from channel_widget import ChannelWidget
from traceback import print_exc
from kivy.graphics.transformation import Matrix

from htlcs_thread import HTLCsThread
from channels_thread import ChannelsThread


class Node(Button):
    col = ListProperty([80 / 255, 80 / 255, 80 / 255, 1])
    channel = ObjectProperty(None)

    def on_release(self):
        self.col = [150 / 255, 150 / 255, 150 / 255, 1]
        sw = self.parent
        sa = sw.parent
        cs = sa.parent
        ae = cs.children[0]
        ae.selection_type = "node"
        ae.selection = self.text
        if self.channel:
            ae.channel = self.channel


class ChannelsWidget(Scatter):
    def __init__(self, **kwargs):
        super(ChannelsWidget, self).__init__(**kwargs)

        self.htlcs_thread = HTLCsThread(inst=self)
        self.htlcs_thread.daemon = True
        self.htlcs_thread.start()

        self.channels_thread = ChannelsThread(inst=self)
        self.channels_thread.daemon = True
        self.channels_thread.start()

        self.nodes = []
        self.edges = []
        self.lines = []
        self.channels = []
        self.radius = 600
        self.node = None
        self.button = None
        self.obj = InstructionGroup()
        lnd = data_manager.data_man.lnd
        try:
            self.channels = sorted(
                lnd.get_channels(),
                key=lambda x: int(x.local_balance) / int(x.capacity),
                reverse=True,
            )
            if not self.channels:
                return
            self.info = lnd.get_info()
            max_cap = max([int(c.capacity) for c in self.channels])
            caps = {
                c.chan_id: max(2, int(int(c.capacity) / max_cap) * 5)
                for c in self.channels
            }
            for i, c in enumerate(self.channels):
                """
                The Node and ChannelWidget should live together in their own widget
                """
                l = ChannelWidget(points=[0, 0, 0, 0], channel=c, width=caps[c.chan_id])
                self.lines.append(l)
                b = Node(text=lnd.get_node_alias(c.remote_pubkey), channel=c)
                self.add_widget(b)
                self.add_widget(l)
                self.nodes.append(b)
            self.node = Node(text=self.info.alias)
            self.add_widget(self.node)
            self.bind(pos=self.update_rect, size=self.update_rect)
        except:
            print_exc()
            print("Issue getting channels")

    def refresh(self):
        print("refresh")

    def update_rect(self, *args):
        """
        The node + channel widget should know how to place itself, this
        code doesn't belong here.
        """
        w = self.size[0]
        h = self.size[1]
        w_2 = w / 2
        h_2 = h / 2
        if self.node:
            self.node.pos = (w_2 - (70 / 2), h_2 - (100 / 2))
        for i, line in enumerate(self.lines):
            x = math.sin(i / len(self.channels) * 3.14378 * 2) * self.radius + w_2
            y = math.cos(i / len(self.channels) * 3.14378 * 2) * self.radius + h_2
            line.points = [w_2, h_2, x, y]
        for i, node in enumerate(self.nodes):
            x = (
                math.sin(i / len(self.channels) * 3.14378 * 2) * self.radius
                + w_2
                - (70 / 2)
            )
            y = (
                math.cos(i / len(self.channels) * 3.14378 * 2) * self.radius
                + h_2
                - (100 / 2)
            )
            node.pos = [x, y]

    def on_touch_down(self, touch):
        if touch.is_mouse_scrolling:
            delta = 0.2
            s = dict(scrolldown=1 + delta, scrollup=1 - delta).get(touch.button)
            if s:
                mat = Matrix().scale(s, s, s)
                self.apply_transform(mat, anchor=touch.pos)
        else:
            self.node.col = [80 / 255, 80 / 255, 80 / 255, 1]
            for n in self.nodes:
                n.col = [80 / 255, 80 / 255, 80 / 255, 1]
            Scatter.on_touch_down(self, touch)
