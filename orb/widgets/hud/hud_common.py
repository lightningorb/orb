from kivy.properties import NumericProperty
from kivy.uix.label import Label
from kivy.uix.widget import Widget


class Bordered(Widget):
    pass


class Hideable:
    alpha = NumericProperty(0)

    def show(self):
        self.alpha = 1


class BorderedLabel(Label, Hideable):
    pass