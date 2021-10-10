from kivy.uix.label import Label
from kivy.properties import NumericProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ObjectProperty
import data_manager
from kivymd.uix.textfield import MDTextField
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.slider import MDSlider
from kivy.uix.widget import Widget
from decorators import guarded


class AEFees(Widget):
    channel = ObjectProperty(None)
    fee_rate_milli_msat = NumericProperty(0)
    time_lock_delta = NumericProperty(0)
    min_htlc = NumericProperty(0)
    max_htlc_msat = NumericProperty(0)
    fee_base_msat = NumericProperty(0)
    last_update = NumericProperty(0)

    def on_channel(self, inst, channel):
        if channel:
            policy_to = data_manager.data_man.lnd.get_policy_to(channel.chan_id)
            self.fee_rate_milli_msat = policy_to.fee_rate_milli_msat
            self.time_lock_delta = policy_to.time_lock_delta
            self.min_htlc = policy_to.min_htlc
            self.max_htlc_msat = policy_to.max_htlc_msat
            self.last_update = policy_to.last_update
            self.fee_base_msat = policy_to.fee_base_msat

    @guarded
    def fee_rate_milli_msat_changed(self, val):
        val = int(val)
        if val != self.fee_rate_milli_msat:
            data_manager.data_man.lnd.update_channel_policy(
                channel=self.channel,
                fee_rate=val / 1e6,
                base_fee_msat=self.fee_base_msat,
                time_lock_delta=self.time_lock_delta,
            )
            self.fee_rate_milli_msat = val

    @guarded
    def fee_base_msat_changed(self, val):
        val = int(val)
        if val != self.fee_base_msat:
            data_manager.data_man.lnd.update_channel_policy(
                channel=self.channel,
                fee_rate=self.fee_rate_milli_msat / 1e6,
                base_fee_msat=val,
                time_lock_delta=self.time_lock_delta,
            )
            self.fee_base_msat = val

    @guarded
    def min_htlc_changed(self, val):
        val = int(val)
        if val != self.min_htlc:
            data_manager.data_man.lnd.update_channel_policy(
                channel=self.channel,
                time_lock_delta=self.time_lock_delta,
                fee_rate=self.fee_rate_milli_msat / 1e6,
                base_fee_msat=self.fee_base_msat,
                min_htlc_msat=val,
                min_htlc_msat_specified=True,
            )
            self.min_htlc = val

    @guarded
    def max_htlc_msat_changed(self, val):
        val = int(val)
        if val != self.max_htlc_msat:
            data_manager.data_man.lnd.update_channel_policy(
                channel=self.channel,
                time_lock_delta=self.time_lock_delta,
                fee_rate=self.fee_rate_milli_msat / 1e6,
                base_fee_msat=self.fee_base_msat,
                max_htlc_msat=val,
            )
            self.max_htlc_msat = val

    @guarded
    def time_lock_delta_changed(self, val):
        val = int(val)
        if val != self.time_lock_delta:
            data_manager.data_man.lnd.update_channel_policy(
                channel=self.channel,
                time_lock_delta=val,
                fee_rate=self.fee_rate_milli_msat / 1e6,
                base_fee_msat=self.fee_base_msat,
            )
            self.time_lock_delta = val


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
            self.slider_up_val = value
            data_manager.data_man.lnd.update_channel_policy(
                channel=self.channel, fee_rate=int(value)
            )
            self.set_max()


class AttributeEditor(BoxLayout):
    selection_type = ObjectProperty("")
    selection = ObjectProperty("")
    channel = ObjectProperty(None)

    def __init__(self, *args, **kwargs):
        super(AttributeEditor, self).__init__(*args, **kwargs)
        self.bind(channel=self.on_selection_changed)

    def on_selection_changed(self, *args):
        self.ids.ae_scroll_view.clear_widgets()
        self.ids.ae_scroll_view.add_widget(
            AEChannel(
                channel=self.channel,
                pos=[self.pos[0], self.pos[1] + 50],
                size=[self.size[0], self.size[1] - 100],
            )
        )


class AEChannel(GridLayout):
    channel = ObjectProperty(None)

    def __init__(self, *args, **kwargs):
        super(AEChannel, self).__init__(*args, **kwargs)
        self.add_widget(Label(text="         "))
        for field in self.channel.ListFields():
            if field[0].type == 8:
                widget = BoxLayout(
                    orientation="horizontal", height=100, size_hint_y=None
                )
                widget.add_widget(Label(text=field[0].name))
                widget.add_widget(MDCheckbox(active=field[1]))
            elif field[0].type == 11:
                self.add_widget(Label(text="         "))
                self.add_widget(Label(text=field[0].name))
                for f in field[1].DESCRIPTOR.fields:
                    widget = MDTextField(
                        helper_text=f.name,
                        helper_text_mode="persistent",
                        text=str(getattr(field[1], f.name)),
                    )
                    self.add_widget(widget)
                    widget = None
            else:
                widget = MDTextField(
                    helper_text=field[0].name,
                    helper_text_mode="persistent",
                    text=str(field[1]),
                )
            if widget:
                self.add_widget(widget)
        self.add_widget(Label(text="         "))
