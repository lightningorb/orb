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
        if not self.channels_widget:
            Clock.schedule_once(self.build, 2)

    def build(self, *args):
        @mainthread
        def delayed():
            ae = AttributeEditor(
                size_hint=(0.2, 1), pos_hint={"center_x": 0.9, "center_y": 0.5}
            )
            self.channels_widget = ChannelsWidget(attribute_editor=ae)
            self.ids.relative_layout.add_widget(self.channels_widget)
            self.ids.relative_layout.add_widget(ae)

        delayed()

    def refresh(self):
        if self.channels_widget:
            self.channels_widget.htlcs_thread.stop()
            self.channels_widget.channels_thread.stop()
            self.ids.box_layout.clear_widgets()
            self.build()
