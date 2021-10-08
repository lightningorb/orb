from kivy.properties import NumericProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
import data_manager
from kivymd.uix.slider import MDSlider
from kivy.uix.widget import Widget


class FeeRateSlider(Widget):
    channel = ObjectProperty(None)
    slider_up_val = 0

    def set_max(self):
        if self.ids.slider.value >= self.ids.slider.max:
            self.ids.slider.max = self.ids.slider.value * 1.5

    def on_channel(self, inst, channel):
        if channel:
            self.ids.slider.value = data_manager.data_man.lnd.get_policy_to(
                channel.chan_id
            ).fee_rate_milli_msat
            self.set_max()
        else:
            self.ids.slider.value = 0

    def slider_up(self, value):
        if self.channel and value != self.slider_up_val:
            print(self)
            self.slider_up_val = value
            data_manager.data_man.lnd.update_channel_policy(
                channel=self.channel, fee_rate=int(value)
            )
            self.set_max()


class AttributeEditor(BoxLayout):
    selection_type = ObjectProperty("")
    selection = ObjectProperty("")
    channel = ObjectProperty(None)
