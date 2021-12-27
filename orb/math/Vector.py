# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-15 07:15:28
# @Last Modified by:   lnorb.com
# @Last Modified time: 2021-12-27 11:12:02

import math


class Vector:
    """
    The Vector class is a 2D object. It is used to store points in 2D
    space and perform common Vector maths.
    """

    def __init__(self, x=0, y=0):
        """
        Vector class constructor.

        >>> v = Vector(5, 5)
        >>> v.x
        5
        """
        self.x = x
        self.y = y

    def __str__(self):
        """
        String representation of a Vector.

        >>> str(Vector(5, 5))
        'Vector(5, 5)'
        """
        return f"Vector({self.x}, {self.y})"

    def __sub__(self, other):
        """
        Subtract two Vectors.

        >>> v = Vector(5, 5) - Vector(2, 2)
        >>> (v.x, v.y)
        (3, 3)
        """
        return Vector(self.x - other.x, self.y - other.y)

    def __add__(self, other):
        """
        Subtract two Vectors.

        >>> v = Vector(3, 3) + Vector(2, 2)
        >>> (v.x, v.y)
        (5, 5)
        """
        return Vector(self.x + other.x, self.y + other.y)

    def __mul__(self, scalar):
        """
        Multiply a Vector by a Scalar.

        >>> v = Vector(3, 3) * 2
        >>> (v.x, v.y)
        (6, 6)
        """
        return Vector(self.x * scalar, self.y * scalar)

    def dist(self, other):
        """
        Return the distance between two points.

        >>> Vector(5, 5).dist(Vector(10, 10))
        7.0710678118654755
        """
        return math.sqrt(math.pow(self.x - other.x, 2) + math.pow(self.y - other.y, 2))

    def mid(self, other):
        """
        Return the mid-point between two points

        >>> mid = Vector(0, 0).mid(Vector(10, 10))
        >>> (mid.x, mid.y)
        (5.0, 5.0)
        """
        return Vector((self.x + other.x) / 2, (self.y + other.y) / 2)

    def dot(self, other):
        """
        Return the dot product of two vectors

        >>> Vector(0, 1).dot(Vector(1, 0))
        0
        """
        return self.x * other.x + self.y * other.y

    def norm(self):
        """
        Return the normalized dot product.

        >>> Vector(0, 1).norm()
        1.0
        """
        return self.dot(self) ** 0.5

    def normalized(self):
        """
        Return the normalized Vector

        >>> v = Vector(10, 0).normalized()
        >>> (v.x, v.y)
        (1.0, 0.0)
        """
        norm = self.norm()
        return Vector(self.x / norm, self.y / norm)

    def perp(self):
        """
        Return a perpendicular Vector

        >>> v = Vector(1, 1).perp()
        >>> (v.x, v.y)
        (1, -1.0)
        """
        return Vector(1, -self.x / (self.y or 1))


if __name__ == "__main__":
    import doctest

    doctest.testmod()
