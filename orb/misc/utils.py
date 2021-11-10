from kivy.app import App


def prefs_col(name):
    app = App.get_running_app()
    section, key = name.split('.')
    col = app.config[section][key]
    if '#' in col:
        if len(col) == 7:
            col += 'ff'
        r, g, b, a = list(int(col[i : i + 2], base=16) / 255 for i in range(1, 8, 2))
        return r, g, b, a
    return eval(col)


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
        norm = self.norm() or 1
        return Vector(self.x / norm, self.y / norm)

    def perp(self):
        return Vector(1, -self.x / (self.y or 1))

    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)

    def __str__(self):
        return f'({self.x}, {self.y})'
