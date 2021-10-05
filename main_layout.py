from kivy.uix.boxlayout import BoxLayout
import ui_actions


class MainLayout(BoxLayout):
    def __init__(self, *args, **kwargs):
        super(MainLayout, self).__init__(*args, **kwargs)
        ui_actions.populate_scripts()
