def lerp(a, b, t):
    return a + (b - a) * t


def lerp_2d(a, b, t):
    return (lerp(a[0], b[0], t), lerp(a[1], b[1], t))
