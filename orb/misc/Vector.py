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
        return math.sqrt(math.pow(self.x - other.x, 2) + math.pow(self.y - other.y, 2))

    def mid(self, other):
        return Vector((self.x + other.x) / 2, (self.y + other.y) / 2)

    def dot(self, other):
        return self.x * other.x + self.y * other.y

    def norm(self):
        return self.dot(self) ** 0.5

    def normalized(self):
        norm = self.norm() or 1
        return Vector(self.x / norm, self.y / norm)

    def perp(self):
        return Vector(1, -self.x / (self.y or 1))

    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)

    def __str__(self):
        return f"({self.x}, {self.y})"
