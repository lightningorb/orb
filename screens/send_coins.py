from popup_drop_shadow import PopupDropShadow
from kivy.clock import Clock
import data_manager
import requests
from decorators import guarded
from ui_actions import console_output


class SendCoins(PopupDropShadow):
    def __init__(self, *args, **kwargs):
        super(SendCoins, self).__init__()
        self.schedule = Clock.schedule_interval(self.get_fees, 10)
        Clock.schedule_once(self.get_fees, 1)

    @guarded
    def get_fees(self, *args):
        fees = requests.get("https://mempool.space/api/v1/fees/recommended").json()
        text = f"""\
        Low priority: {fees["hourFee"]} sat/vB\n
        Medium priority: {fees["halfHourFee"]} sat/vB\n
        High priority: {fees["fastestFee"]} sat/vB
        """
        self.ids.fees.text = text

    def dismiss(self, *args):
        Clock.unschedule(self.schedule)
        super(SendCoins, self).dismiss()

    @guarded
    def send_coins(self, addr, amount, sat_per_vbyte):
        lnd = data_manager.data_man.lnd
        amount = int(amount)
        sat_per_vbyte = int(sat_per_vbyte)
        console_output(f"sending: {addr} {amount} {sat_per_vbyte}")
        out = lnd.send_coins(addr, amount, sat_per_vbyte)
        console_output(out)
