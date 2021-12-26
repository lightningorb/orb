# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-15 07:15:28
# @Last Modified by:   lnorb.com
# @Last Modified time: 2021-12-25 04:17:07
import math


class Vector:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __str__(self):
        return f"Vector({self.x}, {self.y})"

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def dist(self, other):
        """
        Return the distance between two points
        """
        return math.sqrt(math.pow(self.x - other.x, 2) + math.pow(self.y - other.y, 2))

    def mid(self, other):
        """
        Return the mid-point between two points
        """
        return Vector((self.x + other.x) / 2, (self.y + other.y) / 2)

    def dot(self, other):
        """
        Return the dot product of two vectors
        """
        return self.x * other.x + self.y * other.y

    def norm(self):
        """
        Return the normalized dot product with self
        """
        return self.dot(self) ** 0.5

    def normalized(self):
        """
        Return the normalized Vector
        """
        norm = self.norm() or 1
        return Vector(self.x / norm, self.y / norm)

    def perp(self):
        """
        Return a perpendicular Vector
        """
        return Vector(1, -self.x / (self.y or 1))

    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)

    def __str__(self):
        return f"({self.x}, {self.y})"
