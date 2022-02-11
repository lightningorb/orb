# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-15 07:15:28
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-02-11 05:32:23

# GREEN
from colour import Color as LibColour


class Colour:
    def __init__(self, *args, selected=False, alpha=1, **kwargs):
        lum = (0.5, 0.6)[selected]
        sat = (0.5, 0.5)[selected]
        self.alpha = alpha
        self.col = LibColour(*args, luminance=lum, saturation=sat, **kwargs)

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
