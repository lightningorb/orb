# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-15 07:15:28
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-06-12 10:04:28


import base64
import binascii
from threading import Thread

from kivymd.uix.tab import MDTabsBase
from kivymd.uix.floatlayout import MDFloatLayout
from kivy.app import App
from kivy.core.clipboard import Clipboard
from kivy.properties import StringProperty
from kivy.uix.spinner import SpinnerOption

from orb.misc.decorators import guarded
from orb.components.popup_drop_shadow import PopupDropShadow
from orb.misc.utils import pref
from orb.misc.utils import mobile
from orb.misc.certificate import Certificate
from orb.misc.certificate_secure import CertificateSecure
from orb.misc.macaroon import Macaroon
from orb.misc.macaroon_secure import MacaroonSecure
from orb.misc.sec_rsa import get_sec_keys, get_cert_command, get_mac_command

from orb.dialogs.connection_wizard.tab import Tab
from orb.dialogs.connection_wizard.ssh_credentials import SSHCredentials
from orb.dialogs.connection_wizard.nodes_and_files import NodeAndFiles
from orb.dialogs.connection_wizard.lnd_conf import LNDConf
from orb.dialogs.connection_wizard.restart_lnd import RestartLND
from orb.dialogs.connection_wizard.copy_keys import CopyKeys

keep = lambda _: _
keep(SSHCredentials)
keep(NodeAndFiles)
keep(LNDConf)
keep(RestartLND)
keep(CopyKeys)


class ConnectionWizard(PopupDropShadow):
    def open(self, *args):
        self.config = App.get_running_app().config
        super(ConnectionWizard, self).open(self, *args)
        self.ids.ssh_credentials.cert_or_pass()

    def on_tab_switch(self, instance_tabs, instance_tab, instance_tab_label, tab_text):
        if tab_text == "Restart LND":
            self.ids.restart_lnd.stream_log()
