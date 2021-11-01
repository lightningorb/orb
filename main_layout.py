from kivy.properties import ObjectProperty
from kivy.clock import mainthread
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
import ui_actions


class MainLayout(BoxLayout):

    menu_visible = ObjectProperty()

    def __init__(self, *args, **kwargs):
        super(MainLayout, self).__init__(*args, **kwargs)
        self.children = self.children[::-1]

        @mainthread
        def delayed():
            app = App.get_running_app()
            app.root.ids.app_menu.populate_scripts()

        delayed()

    def on_menu_visible(self, *args):
        import data_manager

        data_manager.menu_visible = self.menu_visible
