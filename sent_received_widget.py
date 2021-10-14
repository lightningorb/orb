from kivy.uix.widget import Widget
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Line


class SentReceivedWidget(Widget):
    def __init__(self, *args, **kwargs):
        super(SentReceivedWidget, self).__init__(*args, **kwargs)

        with self.canvas:
            self.sent = Line(points=[0, 0, 0, 0])
            self.received = Line(points=[0, 0, 0, 0])

    def update_rect(self, x, y):
        self.sent.points = [x, y, x * 5, y * 5]
        self.received.points = [x, y, x * 5, y * 5]
