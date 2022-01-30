# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-27 04:05:23
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-01-30 16:41:43

from threading import Thread

from kivy.uix.label import Label
from kivy.graphics.context_instructions import Color
from kivy.properties import ObjectProperty
from kivy.properties import NumericProperty
from kivy.properties import ListProperty
from kivy.graphics.vertex_instructions import Line
from kivy.animation import Animation
from kivy.uix.widget import Widget

from orb.misc.utils import closest_point_on_line
from orb.math.Vector import Vector
from kivy.clock import mainthread


from orb.lnd import Lnd


class FeeWidgetLabel(Label):
    def show(self):
        Animation(color=(0.5, 0.5, 1, 1), duration=0.1).start(self)

    def hide(self):
        Animation(color=(0.5, 0.5, 1, 0), duration=0.1).start(self)


class FeeWidget(Widget):
    channel = ObjectProperty("")
    a = ListProperty([0, 0])
    b = ListProperty([0, 0])
    c = ListProperty([0, 0])
    to_fee_norm = NumericProperty(0)
    new_fee = 0

    def __init__(self, **kwargs):
        super(FeeWidget, self).__init__(**kwargs)
        self.lnd = Lnd()
        self.P1 = Vector()
        self.P2 = Vector()
        self.touch_pos = None

        with self.canvas.before:
            Color(0.5, 1, 0.5, 1)
            self.circle_1 = Line(circle=(150, 150, 50))
            self.circle_2 = Line(circle=(150, 150, 50))
            self.line = Line(points=[0, 0, 0, 0])

        self.label = FeeWidgetLabel(text="", color=(0.5, 1, 0.5, 0))
        self.add_widget(self.label)

        self.bind(a=self.update)
        self.bind(b=self.update)
        self.bind(c=self.update)
        self.channel.bind(fee_rate_milli_msat=self.update)

    def update(self, *args):
        self.to_fee_norm = min(int(self.channel.fee_rate_milli_msat) / 1000 * 30, 30)
        A = Vector(*self.a)
        B = Vector(*self.c)
        AB = B - A
        AB_perp_normed = AB.perp().normalized()
        self.P1 = B + AB_perp_normed * self.to_fee_norm
        self.P2 = B - AB_perp_normed * self.to_fee_norm
        self.circle_1.circle = (self.P1.x, self.P1.y, 5)
        self.circle_2.circle = (self.P2.x, self.P2.y, 5)
        self.line.points = (self.P1.x, self.P1.y, self.P2.x, self.P2.y)

    def set_points(self, a, b, c):
        self.a, self.b, self.c = a, b, c

    def on_touch_down(self, touch):
        if not touch.is_mouse_scrolling:
            B = Vector(touch.pos[0], touch.pos[1])
            self.OP1, self.OP2 = self.P1, self.P2
            self.orig_to_fee_norm = self.to_fee_norm
            for P in (self.P1, self.P2):
                if P.dist(B) < 5:
                    self.label.show()
                    self.touch_pos = closest_point_on_line(self.P1, self.P2, B)
                    return True
        return super(FeeWidget, self).on_touch_down(touch)

    def on_touch_up(self, touch):
        if self.touch_pos:
            self.touch_pos = None
            self.channel.fee_rate_milli_msat = self.new_fee
            self.label.hide()

            def update_fees(*args):
                print(f"Setting fees to: {self.channel.fee_rate_milli_msat / 1e6}")
                self.channel.update_lnd_with_policies()

            Thread(target=update_fees).start()
            return True
        return super(FeeWidget, self).on_touch_down(touch)

    def on_touch_move(self, touch):
        if self.touch_pos:
            C = closest_point_on_line(
                self.OP1, self.OP2, Vector(touch.pos[0], touch.pos[1])
            )
            mid = self.P1.mid(self.P2)
            self.to_fee_norm = C.dist(mid)
            diff = self.to_fee_norm / self.orig_to_fee_norm
            self.new_fee = self.channel.fee_rate_milli_msat * diff
            self.label.pos = (mid.x, mid.y)
            self.label.text = str(int(self.new_fee))
            return True

        return super(FeeWidget, self).on_touch_move(touch)
