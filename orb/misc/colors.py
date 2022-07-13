# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-15 07:15:28
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-07-13 11:08:41

from colour import Color as LibColour


class Colour:
    def __init__(self, rgb, active=False, selected=False, alpha=1):
        self.alpha = alpha
        if not active:
            rgb = "#333333"
            self.col = LibColour(rgb)
            return
        if selected:
            self.col = LibColour(rgb, luminance=0.6, saturation=0.5)
            return
        self.col = LibColour(rgb, luminance=0.5, saturation=0.5)

    @property
    def rgba(self):
        rgb = self.col.rgb
        return [rgb[0], rgb[1], rgb[2], self.alpha]


GREEN = [0.5, 0.8, 0.5, 1]

# BLUE

BLUE = [0.5, 0.5, 0.8, 1]

# ORANGE

ORANGE = [1, 0.5, 0.5, 1]


WHITE = [1, 1, 1, 1]
