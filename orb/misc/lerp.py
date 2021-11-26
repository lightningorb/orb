import math

def lerp(a, b, t):
    return a + (b - a) * t


def lerp_2d(a, b, t):
    return (lerp(a[0], b[0], t), lerp(a[1], b[1], t))


def lerp_vec(a, b, t):
    return (lerp(a.x, b.x, t), lerp(a.y, b.y, t))

def asymptote(f):
    return 2 / math.pi * math.atan(f)