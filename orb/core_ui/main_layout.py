from kivy.properties import ObjectProperty
from kivy.clock import mainthread
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window, Keyboard
import data_manager


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
        self.shift = False

        @mainthread
        def delayed():
            app = App.get_running_app()
            app.root.ids.app_menu.populate_scripts()

        delayed()

    def on_menu_visible(self, *args):
        data_manager.menu_visible = self.menu_visible

    def _keyboard_released(self, window=None, key=None):
        if data_manager.data_man.disable_shortcuts:
            return
        if key:
            code, key = key
            if key == "shift":
                self.shift = False

    def _keyboard_on_key_down(self, window, key, text, super):
        if data_manager.data_man.disable_shortcuts:
            return
        code, key = key
        if key == "shift":
            self.shift = True
            return False
        if self.shift and key == "c":
            data_manager.data_man.show_chords = not data_manager.data_man.show_chords
            return False
        if key == "j":
            data_manager.data_man.show_chord += 1
        if key == "k":
            data_manager.data_man.show_chord -= 1
        return False
