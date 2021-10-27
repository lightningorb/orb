from kivy.config import Config

Config.set('graphics', 'window_state', 'maximized')

import kivy.weakmethod
import kivy.core.text.text_sdl2
import kivy.core.window.window_sdl2
import kivy.graphics.cgl_backend
import kivy.graphics.buffer
import kivymd.icon_definitions
from kivy.uix.widget import Widget
from kivy.uix.scatter import Scatter
import kivy_garden.contextmenu
from orb_app import OrbApp
from kivy.app import App

from attribute_editor import *
from channel_widget import *
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
from top_menu import *

if __name__ == "__main__":
    OrbApp().run()
