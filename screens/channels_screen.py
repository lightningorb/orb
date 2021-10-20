from kivy.app import App
from kivy.clock import Clock
from kivy.clock import mainthread
from kivy.uix.screenmanager import Screen
from channels_widget import ChannelsWidget
from attribute_editor import AttributeEditor


class ChannelsScreen(Screen):
    def __init__(self, *args, **kwargs):
        super(ChannelsScreen, self).__init__(*args, **kwargs)
        self.channels_widget = None

    def on_enter(self, *args):
        @mainthread
        def delayed():
            app = App.get_running_app()
            app.root.ids.app_menu.add_channels_menu()
        delayed()
        if not self.channels_widget:
            Clock.schedule_once(self.build, 2)

    def build(self, *args):
        @mainthread
        def delayed():
            ae = self.ids.attribute_editor
            self.channels_widget = ChannelsWidget(attribute_editor=ae)
            self.ids.cw_layout.add_widget(self.channels_widget)
        delayed()

    def refresh(self, *args, **kwargs):
        if self.channels_widget:
            self.channels_widget.htlcs_thread.stop()
            self.channels_widget.channels_thread.stop()
            self.ids.cw_layout.clear_widgets()
            self.build()
