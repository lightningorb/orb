import data_manager
from kivy.graphics.context_instructions import Color
from kivy.properties import ObjectProperty
from kivy.properties import NumericProperty
from kivy.properties import ListProperty
from kivy.graphics.vertex_instructions import Line
from kivy.uix.widget import Widget
from threading import Thread

try:
    import numpy as np
except:
    pass


class FeeWidget(Widget):
    channel = ObjectProperty("")
    a = ListProperty([0, 0])
    b = ListProperty([0, 0])
    c = ListProperty([0, 0])
    to_fee = NumericProperty(0)
    to_fee_norm = NumericProperty(0)

    def __init__(self, **kwargs):
        super(FeeWidget, self).__init__(**kwargs)
        self.lnd = data_manager.data_man.lnd

        def update():
            self.policy_to = self.lnd.get_policy_to(self.channel.chan_id)
            self.policy_from = self.lnd.get_policy_from(self.channel.chan_id)
            self.to_fee = self.policy_to.fee_rate_milli_msat
            self.to_fee_norm = min(int(self.policy_to.fee_rate_milli_msat) / 1000 * 30, 30)
            self.from_fee = self.policy_from.fee_rate_milli_msat

        self.bind(a=self.update_rect)
        self.bind(b=self.update_rect)
        self.bind(c=self.update_rect)
        self.bind(to_fee_norm=self.update_rect)

        Thread(target=update).start()

        with self.canvas.before:
            Color(0.5, 1, 0.5, 1)
            self.circle_1 = Line(circle=(150, 150, 50))
            self.circle_2 = Line(circle=(150, 150, 50))
            self.line = Line(points=[0, 0, 0, 0])

    def update_rect(self, *args):
        try:
            v = np.array(self.b) - np.array(self.a)
            ub = v / np.linalg.norm(v)
            orth = np.random.randn(2)
            orth -= orth.dot(ub) * ub
            orth = orth / np.linalg.norm(orth)
            handle_a = self.c + orth * self.to_fee_norm
            handle_b = self.c + orth * -self.to_fee_norm
            self.circle_1.circle = (handle_a[0], handle_a[1], 5)
            self.circle_2.circle = (handle_b[0], handle_b[1], 5)
            self.line.points = (handle_a[0], handle_a[1], handle_b[0], handle_b[1])
        except:
            pass

    def set_points(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c
