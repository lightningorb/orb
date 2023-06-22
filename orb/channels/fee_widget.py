# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-27 04:05:23
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-08-25 07:32:17

from threading import Thread

from kivy.clock import mainthread
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.animation import Animation
from kivy.properties import ListProperty
from kivy.properties import ObjectProperty
from kivy.properties import NumericProperty
from kivy.graphics.vertex_instructions import Line
from kivy.graphics.context_instructions import Color

from orb.math.Vector import Vector
from orb.misc.decorators import guarded
from orb.math import closest_point_on_line


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
        self.handle1 = Vector()
        self.handle2 = Vector()
        self.touch_pos_down = None

        with self.canvas.before:
            self.col = Color(0.5, 1, 0.5, 1)
            self.circle_1 = Line(circle=(150, 150, 50))
            self.circle_2 = Line(circle=(150, 150, 50))
            self.line = Line(points=[0, 0, 0, 0])
            Color(255 / 255.0, 164 / 255.0, 0 / 255.0, 0.8)
            self.line_balanced_ratio = Line(points=[0, 0, 0, 0])

        self.label = FeeWidgetLabel(text="", color=(0.5, 1, 0.5, 0))
        self.add_widget(self.label)

        self.bind(a=self.update)
        self.bind(b=self.update)
        self.bind(c=self.update)
        self.channel.bind(fee_rate_milli_msat=self.update)
        self.channel.bind(fee_rate_milli_msat=self.flash)
        self.channel.bind(balanced_ratio=self.update_balanced_ratio_line)
        self.channel.bind(max_htlc_msat=self.update_max_htlc_msat)
        self.update_max_htlc_msat()

    def update_max_htlc_msat(self, *_):
        if self.channel.max_htlc_msat <= 1000:
            (
                Animation(rgba=(1, 1, 1, 1), duration=0.2)
                + Animation(rgba=(0.1, 0.1, 1, 1), duration=0.2)
            ).start(self.col)
        else:
            (
                Animation(rgba=(1, 1, 1, 1), duration=0.2)
                + Animation(rgba=(0.5, 1, 0.5, 1), duration=0.2)
            ).start(self.col)

    def flash(self, *_):
        (
            Animation(rgba=(1, 1, 1, 1), duration=0.2)
            + Animation(rgba=(0.5, 1, 0.5, 1), duration=0.2)
        ).start(self.col)

    @guarded
    @mainthread
    def update(self, *_):
        self.to_fee_norm = min(int(self.channel.fee_rate_milli_msat) / 1000 * 30, 30)
        A = Vector(*self.a)
        B = Vector(*self.c)
        AB = B - A
        AB_perp_normed = AB.perp().normalized()
        self.handle1 = B + AB_perp_normed * (self.to_fee_norm or 1)
        self.handle2 = B - AB_perp_normed * (self.to_fee_norm or 1)
        self.circle_1.circle = (self.handle1.x, self.handle1.y, 5)
        self.circle_2.circle = (self.handle2.x, self.handle2.y, 5)
        self.line.points = (
            self.handle1.x,
            self.handle1.y,
            self.handle2.x,
            self.handle2.y,
        )
        self.update_balanced_ratio_line()

    @mainthread
    def update_balanced_ratio_line(self, *_):
        A = Vector(*self.a)
        B = Vector(*self.b)
        AB = B - A
        C = AB * self.channel.balanced_ratio
        AB_perp_normed = AB.perp().normalized()
        handle1 = A + C + AB_perp_normed * 5
        handle2 = A + C - AB_perp_normed * 5
        self.line_balanced_ratio.points = (handle1.x, handle1.y, handle2.x, handle2.y)

    def set_points(self, a, b, c):
        self.a, self.b, self.c = a, b, c

    @guarded
    def on_touch_down(self, touch):
        if not touch.is_mouse_scrolling:
            touch_pos = Vector(touch.pos[0], touch.pos[1])
            self.handle1_down, self.handle2_down = self.handle1, self.handle2
            self.orig_to_fee_norm = self.to_fee_norm
            for handle in (self.handle1, self.handle2):
                # if user touched close to a fee handle
                if handle.dist(touch_pos) < 5:
                    self.label.show()
                    # get closest point on the line, this will help
                    # compute the slide later
                    self.touch_pos_down = closest_point_on_line(
                        self.handle1, self.handle2, touch_pos
                    )
                    return True
        return super(FeeWidget, self).on_touch_down(touch)

    @guarded
    def on_touch_up(self, touch):
        if self.touch_pos_down:
            self.touch_pos_down = None
            self.channel.fee_rate_milli_msat = int(self.new_fee)
            self.label.hide()

            def update_fees(*_):
                print(f"Setting fees to: {self.channel.fee_rate_milli_msat / 1e6}")
                self.channel.update_lnd_with_policies()

            Thread(target=update_fees).start()
            return True
        return super(FeeWidget, self).on_touch_down(touch)

    @guarded
    def on_touch_move(self, move):
        if self.touch_pos_down:
            # find the position (where the user is pressing now after sliding)
            new_pos = closest_point_on_line(
                self.handle1_down, self.handle2_down, Vector(move.pos[0], move.pos[1])
            )
            # get the mid-point between the two handles
            mid = self.handle1.mid(self.handle2)
            # what's the distance between the mid-point, and where the user is now
            self.to_fee_norm = new_pos.dist(mid)
            diff = self.to_fee_norm / (self.orig_to_fee_norm or 1)
            self.new_fee = (self.channel.fee_rate_milli_msat or 1) * diff
            self.label.pos = (mid.x, mid.y)
            self.label.text = str(int(self.new_fee))
            return True

        return super(FeeWidget, self).on_touch_move(move)
