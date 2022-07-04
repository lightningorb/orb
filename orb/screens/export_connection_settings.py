# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-06-30 14:26:36
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-06-30 19:33:40

import os

from pathlib import Path
from tempfile import mkdtemp

from kivy.app import App
from kivy.config import ConfigParser
from kivymd.uix.screen import MDScreen

from orb.misc.utils import get_available_nodes
from orb.misc.macaroon_secure import MacaroonSecure
from orb.misc.certificate_secure import CertificateSecure
from orb.misc.device_id import device_id


class ExportConnectionSettings(MDScreen):

    pk = None

    lnd_settings_to_copy = [
        "rest_port",
        "tls_certificate",
        "network",
        "protocol",
        "macaroon_admin",
        "type",
        "identity_pubkey",
    ]

    def node_selected(self, pk_short):
        self.pk = next(
            iter([x for x in get_available_nodes() if x.startswith(pk_short)]), None
        )
        self.ids.export_button.disabled = False

    def on_enter(self, *args):
        super(ExportConnectionSettings, self).on_enter(*args)
        pks = [x[:10] for x in get_available_nodes()]
        self.ids.nodes.values = pks
        self.ids.device_id.text = device_id().decode()

    def export_node_settings(self):
        config = ConfigParser()
        source_config = ConfigParser()
        app = App.get_running_app()
        source_path = (
            Path(app._get_user_data_dir()).parent / f"orb_{self.pk}/orb_{self.pk}.ini"
        )
        assert source_path.exists()
        print(source_path)
        source_config.read(source_path.as_posix())
        source_config.filename = "/tmp/blah.ini"
        source_config.write()
        config.adddefaultsection("host")
        config.adddefaultsection("lnd")
        config.setdefaults("host", {k: source_config["host"][k] for k in ["hostname"]})
        config.setdefaults(
            "lnd",
            {k: source_config["lnd"].get(k, "") for k in self.lnd_settings_to_copy},
        )

        uid = self.ids.device_id.text.encode()

        cert_secure = CertificateSecure(
            source_config["lnd"]["tls_certificate"].encode()
        )
        plain_cert = cert_secure.as_plain_certificate().cert
        cert_new_uid = CertificateSecure.init_from_plain(plain_cert, uid=uid)
        config["lnd"]["tls_certificate"] = cert_new_uid.cert_secure.decode()

        mac_secure = MacaroonSecure(source_config["lnd"]["macaroon_admin"].encode())
        plain_mac = mac_secure.as_plain_macaroon().macaroon
        mac_new_uid = MacaroonSecure.init_from_plain(plain_mac, uid=uid)
        config["lnd"]["macaroon_admin"] = mac_new_uid.macaroon_secure.decode()

        d = mkdtemp()
        p = Path(d) / "orb.ini"
        config.filename = p.as_posix()
        config.write()
        with p.open() as f:
            self.ids.text_export.text = f.read()
        os.unlink(p.as_posix())
