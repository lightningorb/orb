from kivy.clock import mainthread
from kivy.uix.screenmanager import Screen
from channels_widget import *


class ChannelsScreen(Screen):
    """
    Sadly i'm not sure how to properly place these
    the channelswidget in the layout without it
    having some strang offset issues, so instead
    i'll let kivy sort it out by using the auto layout.
    This means no refreshing the channels widget for now.
    """

    pass
    # def __init__(self, *args, **kwargs):
    #     super(ChannelsScreen, self).__init__()
    #     self.channels_widget = None

    # def on_enter(self, *args):
    #     if not self.channels_widget:
    #         self.build()

    # def build(self):
    #     @mainthread
    #     def delayed():
    #         self.channels_widget = ChannelsWidget()
    #         self.ids.relative_layout.add_widget(self.channels_widget)
    #     delayed()

    # def refresh(self):
    #     if self.channels_widget:
    #         self.channels_widget.htlcs_thread.stop()
    #         self.ids.relative_layout.clear_widgets()
    #         self.build()
