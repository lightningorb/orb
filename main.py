from kivy.config import Config

Config.set("graphics", "width", "1400")
Config.set("graphics", "height", "800")

from kivy.uix.widget import Widget
from kivy.uix.scatter import Scatter
from orb_app import OrbApp
from kivy.app import App

from attribute_editor import *
from channel_widget import *
from screens.first_screen import *
from screens.channels_screen import *
from screens.pay_screen import *
from screens.mail_screen import *
from screens.open_channel_screen import *
from screens.new_address_screen import *
from screens.connect_screen import *
from screens.ingest_invoices_screen import *
from screens.console_screen import *
from screens.send_coins import *

from main_layout import *
from status_line import *

if __name__ == "__main__":
    OrbApp().run()
