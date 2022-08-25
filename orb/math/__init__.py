# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-27 04:02:50
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-08-17 07:30:06

"""
A package for math-related modules.
"""

from .Vector import Vector


def closest_point_on_line(p1: Vector, p2: Vector, p3: Vector) -> Vector:
    """
    p1 and p2 are 2 points that form a line.
    p3 is an arbitrary point.
    This function returns the closest point, on the line, to p3.
    """
    dx, dy = p2.x - p1.x, p2.y - p1.y
    det = dx * dx + dy * dy
    a = (dy * (p3.y - p1.y) + dx * (p3.x - p1.x)) / det
    return Vector(p1.x + a * dx, p1.y + a * dy)
