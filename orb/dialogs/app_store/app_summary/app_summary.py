from kivy.properties import ObjectProperty, NumericProperty
from kivy.uix.boxlayout import BoxLayout


class AppSummary(BoxLayout):
    """
    The AppSummary is the card that shows in both the installed
    and available apps.
    """

    app = ObjectProperty()
    selected = NumericProperty(0)

    def __init__(self, app, *args, **kwargs):
        self.app = app
        super(AppSummary, self).__init__(*args, **kwargs)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.selected += 1
        return super(AppSummary, self).on_touch_down(touch)