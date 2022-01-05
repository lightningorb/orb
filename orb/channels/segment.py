# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-27 04:03:20
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-01-06 01:07:41

from math import ceil

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Line
from kivy.graphics.vertex_instructions import Ellipse
from kivy.graphics.instructions import InstructionGroup

from orb.math.lerp import lerp_2d
from orb.misc.utils import prefs_col
from orb.misc.prefs import pref


class Segment(Widget):
    """
    A Segment is a section of the Channel in the GUI.
    It can represent local, pending, or remote balance.
    """

    def __init__(self, width, amt_sat=0, color=None, *args, **kwargs):
        super(Segment, self).__init__(*args, **kwargs)
        self.amt_sat = amt_sat
        self.diameter = 3
        self.radius = self.diameter / 2
        # the color is given to use by the caller, we are just
        # in charge of setting its opacity
        color[-1] = float(pref("display.channel_opacity"))
        self.ig = []
        with self.canvas:
            self.color = Color(*color)
            self.line = Line(points=[0, 0, 0, 0], width=width, cap="none")

    def update_rect(self, amt_sat=0):
        amt_sat = int(amt_sat)
        a = lerp_2d(self.line.points[:2], self.line.points[2:], 0.02)
        b = lerp_2d(self.line.points[:2], self.line.points[2:], 0.98)
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
                self.canvas.remove(self.ig.pop())
        for i, e in enumerate(self.ig):
            e.children[2].pos = lerp_2d(
                [a[0] - self.radius, a[1] - self.radius],
                [b[0] - self.radius, b[1] - self.radius],
                i / len(self.ig),
            )
