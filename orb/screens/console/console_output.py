from kivy.properties import StringProperty
from kivy.uix.textinput import TextInput

from orb.misc import data_manager


class ConsoleOutput(TextInput):
    output = StringProperty("")

    def on_touch_down(self, touch):

        if self.collide_point(*touch.pos):
            if data_manager.data_man.menu_visible:
                return False
        return super(ConsoleOutput, self).on_touch_down(touch)