from kivy.properties import ObjectProperty
from kivy.clock import mainthread
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window, Keyboard


class MainLayout(BoxLayout):

    menu_visible = ObjectProperty()

    def __init__(self, *args, **kwargs):
        super(MainLayout, self).__init__(*args, **kwargs)
        self.children = self.children[::-1]
        keyboard = Window.request_keyboard(self._keyboard_released, self)
        keyboard.bind(
            on_key_down=self._keyboard_on_key_down, on_key_up=self._keyboard_released
        )
        self.super = []

        @mainthread
        def delayed():
            app = App.get_running_app()
            app.root.ids.app_menu.populate_scripts()

        delayed()

    def on_menu_visible(self, *args):
        import data_manager

        data_manager.menu_visible = self.menu_visible

    def _keyboard_released(self, *args):
        self.super = []

    def _keyboard_on_key_down(self, window, keycode, text, super):
        if "lctrl" in self.super and keycode[1] == "s":
            print("saved")
            self.super = []
            return False
        elif "lctrl" not in self.super and keycode[1] in ["lctrl"]:
            self.super.append(keycode[1])
            return False
        elif keycode[1] == "]":
            print("next liq")
        elif keycode[1] == "[":
            print("prev liq")
        else:
            print(keycode)
            return False
