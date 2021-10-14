from kivy.properties import ObjectProperty
from kivy.uix.widget import Widget
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Line


class SentReceivedWidget(Widget):
    channel = ObjectProperty(None)

    def __init__(self, channel, *args, **kwargs):
        super(SentReceivedWidget, self).__init__(*args, **kwargs)
        self.channel = channel

        with self.canvas:
            self.sent = Line(points=[0, 0, 0, 0], width=1)
            # self.received = Line(points=[0, 0, 0, 0], width=3)

    def update_rect(self, x, y):
        offset = 0.1
        sent = self.channel.total_satoshis_sent / 1e8
        received = self.channel.total_satoshis_received / 1e8
        x += x * offset
        y += y * offset
        self.sent.points = [x, y, x + x * sent, y + y * sent]
        # self.received.points = [x, y, x * received, y * received]
