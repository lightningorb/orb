# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-27 04:03:13
# @Last Modified by:   lnorb.com
# @Last Modified time: 2021-12-27 08:59:11

"""
This module is used to interpolate values.
"""

def lerp(a, b, t):
    """
    Interpolate 2 values.

    >>> lerp(a=10, b=20, t=0.5)
    15.0
    """
    return a + (b - a) * t


def lerp_2d(a, b, t):
    """
    Interpolate 2 lists or tuples.

    >>> lerp_2d(a=[10,10], b=[20,20], t=0.5)
    (15.0, 15.0)
    """

    return (lerp(a[0], b[0], t), lerp(a[1], b[1], t))


def lerp_vec(a, b, t):
    """
    Interpolate 2 Vectors.

    >>> from orb.math.Vector import Vector
    >>> lerp_vec(a=Vector(10,10), b=Vector(20,20), t=0.5)
    (15.0, 15.0)
    """

    return (lerp(a.x, b.x, t), lerp(a.y, b.y, t))


if __name__ == "__main__":
    import doctest

    doctest.testmod()
