# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-27 04:03:20
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-02-11 09:14:08

from math import ceil
from threading import Lock

from kivy.uix.widget import Widget
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Line
from kivy.graphics.vertex_instructions import Ellipse
from kivy.graphics.instructions import InstructionGroup
from kivy.uix.label import Label
from kivy.animation import Animation

from orb.math.lerp import lerp_2d
from orb.misc.utils import prefs_col
from orb.misc.prefs import pref


class SegmentLabel(Label):
    def show(self):
        Animation(color=(0.5, 0.5, 1, 1), duration=0.1).start(self)

    def hide(self):
        Animation(color=(0.5, 0.5, 1, 0), duration=0.1).start(self)


class Segment(Widget):
    """
    A Segment is a section of the Channel in the GUI.
    It can represent local, pending, or remote balance.
    """

    def __init__(self, width, amt_sat=0, color=None, label="", *args, **kwargs):
        super(Segment, self).__init__(*args, **kwargs)
        self.amt_sat = amt_sat
        self.diameter = 3
        self.radius = self.diameter / 2
        self.ig = []
        with self.canvas:
            self.color = Color(*color)
            self.line = Line(points=[0, 0, 0, 0], width=width, cap="none")

        if label is not None:
            self.label = SegmentLabel(text=label, color=(0.5, 1, 0.5, 0))
            self.add_widget(self.label)
        else:
            self.label = None

    def update(self, amt_sat=0):
        amt_sat = int(amt_sat)
        a = lerp_2d(self.line.points[:2], self.line.points[2:], 0.02)
        b = lerp_2d(self.line.points[:2], self.line.points[2:], 0.98)

        if self.label:
            self.label.pos = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
            self.label.show()

        n = ceil(amt_sat / 1e6)
        diff = n - len(self.ig)
        for _ in range(abs(diff)):
            if diff > 0:
                ig = InstructionGroup()
                ig.add(Color(*prefs_col("display.1m_color")))
                ig.add(Ellipse(pos=[0, 0], size=[self.diameter, self.diameter]))
                self.ig.append(ig)
                self.canvas.add(ig)
            else:
                if self.ig:
                    self.canvas.remove(self.ig.pop())
        for i, e in enumerate(self.ig):
            e.children[2].pos = lerp_2d(
                [a[0] - self.radius, a[1] - self.radius],
                [b[0] - self.radius, b[1] - self.radius],
                i / len(self.ig),
            )
