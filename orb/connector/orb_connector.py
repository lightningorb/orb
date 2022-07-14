# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-06-29 12:03:56
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-06-30 14:43:18

from kivy.uix.screenmanager import ScreenManager
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App

from orb.dialogs.connection_wizard.connection_wizard import ConnectionWizard
from orb.dialogs.connection_settings import ConnectionSettings
from orb.screens.export_connection_settings import ExportConnectionSettings
from orb.screens.import_connection_settings import ImportConnectionSettings


class OrbConnector(BoxLayout):

    pass
