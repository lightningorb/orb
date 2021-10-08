# import numpy as np
import data_manager
from kivy.graphics.context_instructions import Color
from kivy.properties import NumericProperty
from kivy.properties import ObjectProperty
from kivy.properties import ListProperty
from kivy.graphics.vertex_instructions import Line
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


class ChannelWidget(Widget):
    local_line_col = ObjectProperty(None)
    remote_line_col = ObjectProperty(None)
    channel = ObjectProperty("")
    points = ListProperty([0, 0, 0, 0])
    a = ListProperty([0, 0])
    b = ListProperty([0, 0])
    c = ListProperty([0, 0])
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

        with self.canvas.before:
            self.local_line_col = Color(0.5, 1, 0.5, 1)
            self.line_local = Line(points=[0, 0, 0, 0], width=self.width)
            self.remote_line_col = Color(0.5, 0.5, 1, 1)
            self.line_remote = Line(points=[0, 0, 0, 0], width=self.width)

        self.bind(points=self.update_rect)

    def update_rect(self, *args):
        c, p = self.channel, self.points

        A = (p[0], p[1])
        B = (p[2], p[3])

        a = lerp_2d(A, B, 0.10)
        b = lerp_2d(A, B, 0.90)
        c = lerp_2d(a, b, (int(c.local_balance) / int(c.capacity)))

        self.line_local.points = [a[0], a[1], c[0], c[1]]
        self.line_remote.points = [c[0], c[1], b[0], b[1]]

        self.a = a
        self.b = b
        self.c = c

        self.to_fee.a = self.a
        self.to_fee.b = self.b
        self.to_fee.c = self.c

    def anim_htlc(self, htlc):
        # {'incoming_channel': '02234cf94dd9a4b76cb4', 'outgoing_channel': 'southxchange.com', 'outgoing_channel_id': 771459139617882112, 'outgoing_channel_capacity': 10000000, 'outgoing_channel_remote_balance': 1230859, 'outgoing_channel_local_balance': 8767049, 'timestamp': 1633386523, 'event_type': 'SEND', 'event_outcome': 'settle_event'}
        # {'incoming_channel': 'WalletOfSatoshi.com', 'incoming_channel_id': 770369523584794633, 'incoming_channel_capacity': 10000000, 'incoming_channel_remote_balance': 4165791, 'incoming_channel_local_balance': 5803036, 'outgoing_channel': 'OpenNode.com', 'outgoing_channel_id': 773460250725974024, 'outgoing_channel_capacity': 5000000, 'outgoing_channel_remote_balance': 26381, 'outgoing_channel_local_balance': 4971532, 'timestamp': 1633405927, 'event_type': 'FORWARD', 'event_outcome': 'settle_event'}
        if htlc.event_type == "SEND" and htlc.event_outcome == "settle_event":
            self.channel.local_balance = htlc.outgoing_channel_local_balance
            self.channel.remote_balance = htlc.outgoing_channel_remote_balance
            audio_manager.play_send_settle()
        elif htlc.event_type == "FORWARD" and htlc.event_outcome == "settle_event":
            audio_manager.play_forward_settle()
            if htlc.outgoing_channel_id == self.channel.chan_id:
                self.channel.local_balance = htlc.outgoing_channel_local_balance
                self.channel.remote_balance = htlc.outgoing_channel_remote_balance
            if htlc.incoming_channel_id == self.channel.chan_id:
                self.channel.local_balance = htlc.incoming_channel_local_balance
                self.channel.remote_balance = htlc.incoming_channel_remote_balance

        self.update_rect()

        cols = {"forward_fail_event": [1, 0.5, 0.5, 1]}
        col = cols.get(htlc.event_outcome, [1, 1, 1, 1])
        (
            Animation(rgba=col, duration=0.2)
            + Animation(rgba=[0.5, 0.5, 1, 1], duration=5)
        ).start(self.remote_line_col)

        (
            Animation(rgba=col, duration=0.2)
            + Animation(rgba=[0.5, 1, 0.5, 1], duration=5)
        ).start(self.local_line_col)
