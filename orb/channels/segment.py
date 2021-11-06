from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Line
from kivy.graphics.vertex_instructions import Ellipse
from orb.misc.lerp import lerp_2d
from math import ceil
from orb.misc.utils import prefs_col


class Segment(Widget):
    def __init__(self, points, width, cap, amount=0, color=None, *args, **kwargs):
        super(Segment, self).__init__(*args, **kwargs)
        self.amount = amount
        self.d = 3
        self.r = self.d / 2
        opacity = float(App.get_running_app().config["display"]["channel_opacity"])
        color[-1] = opacity
        self.e = []
        self.c = []
        with self.canvas:
            self.color = Color(*color)
            self.line = Line(points=points, width=width, cap=cap)

    def update_rect(self, amount=0):
        amount = int(amount)
        a = lerp_2d(self.line.points[:2], self.line.points[2:], 0.02)
        b = lerp_2d(self.line.points[:2], self.line.points[2:], 0.98)
        n = ceil(amount / 1e6)
        diff = n - len(self.e)
        for _ in range(abs(diff)):
            if diff > 0:
                c = Color(*prefs_col('display.1m_color'))
                e = Ellipse(pos=[0, 0], size=[self.d, self.d])
                self.e.append(e)
                self.c.append(c)
                self.canvas.add(c)
                self.canvas.add(e)
            else:
                e = self.e.pop()
                c = self.e.pop()
                self.canvas.remove(e)
                self.canvas.remove(c)
        for i, e in enumerate(self.e):
            e.pos = lerp_2d(
                [a[0] - self.r, a[1] - self.r],
                [b[0] - self.r, b[1] - self.r],
                i / len(self.e),
            )
