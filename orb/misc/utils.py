from kivy.app import App


def prefs_col(name):
    app = App.get_running_app()
    section, key = name.split('.')
    return eval(app.config[section][key])


def pref(name):
    app = App.get_running_app()
    section, key = name.split('.')
    try:
        return float(app.config[section][key])
    except:
        return app.config[section][key]


class hashabledict(dict):
    def __hash__(self):
        return hash(tuple(sorted(self.items())))


class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def dot(self, other):
        return self.x * other.x + self.y * other.y

    def norm(self):
        return self.dot(self) ** 0.5

    def normalized(self):
        norm = self.norm()
        return Vector(self.x / norm, self.y / norm)

    def perp(self):
        return Vector(1, -self.x / self.y)

    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)

    def __str__(self):
        return f'({self.x}, {self.y})'


# A = Vector(0, 0)
# B = Vector(0, 30)

# AB = B - A
# AB_perp_normed = AB.perp().normalized()
# P1 = B + AB_perp_normed * 3
# P2 = B - AB_perp_normed * 3

# print(f'Point{P1}, and Point{P2}')