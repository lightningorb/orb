# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-15 07:15:28
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-07-10 13:22:46

from kivy.app import App
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.screen import MDScreen
from kivy.core.clipboard import Clipboard
from kivy.properties import StringProperty
from kivy.uix.spinner import SpinnerOption
from kivymd.uix.floatlayout import MDFloatLayout

from orb.misc.utils import mobile
from orb.misc.decorators import guarded
from orb.misc.macaroon_secure import MacaroonSecure
from orb.misc.certificate_secure import CertificateSecure
from orb.misc.sec_rsa import get_sec_keys


class TypeSpinnerOption(SpinnerOption):
    pass


class Tab(MDFloatLayout, MDTabsBase):
    """Class implementing content for a tab."""


class ConnectionSettings(MDScreen):

    node_type = StringProperty("default")
    lnd_settings_to_copy = [
        "rest_port",
        "tls_certificate",
        "network",
        "protocol",
        "macaroon_admin",
        "type",
    ]

    def on_enter(self, *args):
        self.connected = False
        self.node_settings = App.get_running_app().node_settings
        self.ids.grpc.disabled = mobile
        super(ConnectionSettings, self).on_enter(self, *args)

    def node_type_selected(self, val):
        self.node_type = val

    def set_and_save(self, key, val):
        self.node_settings[key] = val

    def save_protocol(self, prot):
        self.set_and_save("lnd.protocol", prot)
        if prot == "mock" and self.ids.mock.active:
            self.ids.grpc.active = False
            self.ids.rest.active = False
        if prot == "rest" and self.ids.rest.active:
            self.ids.grpc.active = False
            self.ids.mock.active = False
        if prot == "grpc" and self.ids.grpc.active:
            self.ids.rest.active = False
            self.ids.mock.active = False

    def validate_cert(self, text):
        cert_secure = CertificateSecure.init_from_encrypted(text.encode())
        cert = cert_secure.as_plain_certificate()
        self.ids.feedback.text = cert.debug()

    def save_cert(self, text):
        key = "lnd.tls_certificate"
        cert_secure = CertificateSecure.init_from_encrypted(text.encode())
        cert = cert_secure.as_plain_certificate()
        if cert.is_well_formed():
            self.set_and_save(key, cert_secure.cert_secure.decode())
        else:
            self.ids.feedback.text = cert.debug()

    def save_macaroon(self, text):
        key = "lnd.macaroon_admin"
        mac_secure = MacaroonSecure.init_from_encrypted(text.encode())
        self.set_and_save(key, mac_secure.macaroon_secure.decode())

    def validate_macaroon(self, text):
        mac_secure = MacaroonSecure.init_from_encrypted(text.encode())
        mac = mac_secure.as_plain_macaroon()
        self.ids.mac_feedback.text = mac.debug()

    def copy_cert_encrypt_command(self):
        _, public_key = get_sec_keys()
        Clipboard.copy(get_cert_command(public_key))

    def copy_mac_encrypt_command(self):
        _, public_key = get_sec_keys()
        Clipboard.copy(get_mac_command(public_key))

    @guarded
    def connect(self):
        app = App.get_running_app()
        if self.connected:
            app.stop()
        error = ""
        try:
            from orb.lnd import Lnd

            lnd = Lnd(
                fallback_to_mock=False,
                cache=False,
                use_prefs=False,
                hostname=app.node_settings["host.hostname"],
                protocol=app.node_settings["lnd.protocol"],
                mac_secure=app.node_settings["lnd.macaroon_admin"],
                cert_secure=app.node_settings["lnd.tls_certificate"],
                rest_port=app.node_settings.get("lnd.rest_port") or "8080",
                grpc_port=app.node_settings.get("lnd.grpc_port") or "10009",
            )

            info = lnd.get_info()

            self.ids.connect.text = f"Launch Orb with: {info.identity_pubkey[:5]}..."
            self.connected = True
            app.node_settings["lnd.identity_pubkey"] = info.identity_pubkey
            self.ids.connect.md_bg_color = (0.2, 0.8, 0.2, 1)
        except Exception as e:
            print(e)
            error = "Error connecting to LND"

        if error:
            self.ids.connect.text = f"Error: {error}"
            self.ids.connect.md_bg_color = (0.8, 0.2, 0.2, 1)


def get_cert_command(public_key):
    cert_path = "~/.lnd/tls.cert"
    if pref("host.type") == "umbrel":
        cert_path = "~/umbrel/lnd/tls.cert"
    return f"""python3 -c "import rsa; import base64; import os; p = rsa.PublicKey.load_pkcs1({public_key}); c = open(os.path.expanduser('{cert_path}')).read(); print('\\n'.join([base64.b64encode(rsa.encrypt(c[i : i + 53].encode(), p)).decode() for i in range(0, len(c), 53)]))"  """


def get_mac_command(public_key):
    mac_path = "~/.lnd/data/chain/bitcoin/mainnet/admin.macaroon"
    if pref("host.type") == "umbrel":
        mac_path = "~/umbrel/lnd/data/chain/bitcoin/mainnet/admin.macaroon"
    return f"""python3 -c "import rsa; import os; import codecs; import base64; pub = rsa.PublicKey.load_pkcs1({public_key}); message = codecs.encode(open(os.path.expanduser('{mac_path}'), 'rb' ).read(), 'hex',).decode(); print('\\n'.join([base64.b64encode(rsa.encrypt(message[i : i + 53].encode('utf8'), pub)).decode() for i in range(0, len(message), 53)]))"  """
