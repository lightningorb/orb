from kivy.uix.screenmanager import Screen
from channels_widget import *
from data_manager import controllers


class ChannelsScreen(Screen):
    pass

    # built = False

    # def on_enter(self, *args):
    #     if not self.built:
    #         # print("ON ENTER")
    #         # controllers["channels_widget"].build()
    #         self.built = True
    #         self.ids.hud.build()
