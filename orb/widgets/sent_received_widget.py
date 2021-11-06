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
            Color(*[0.5, 1, 0.5, 1])
            self.sent = Line(points=[0, 0, 0, 0], width=2)

    def update_rect(self, x, y):
        offset = 0.1
        sent = int(self.channel.total_satoshis_sent) / 1e8
        received = int(self.channel.total_satoshis_received) / 1e8
        x += x * offset
        y += y * offset
        self.sent.points = [x, y, x + x * sent, y + y * sent]
