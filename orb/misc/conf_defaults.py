# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-01-06 17:51:07
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-06-17 08:37:41


def set_conf_defaults(config):
    config.add_section("host")
    config.set("host", "type", "default")
    config.set("host", "hostname", "localhost")
    config.set("host", "port", "22")
    config.set("host", "username", "umbrel")
    config.set("host", "auth_type", "password")
    config.set("host", "password", "")
    config.set("host", "certificate", "")
    config.add_section("lnd")
    config.set("lnd", "rest_port", "8080")
    config.set("lnd", "grpc_port", "10009")
    config.set("lnd", "protocol", "mock")
    config.set("lnd", "tls_certificate", "")
    config.set("lnd", "tls_certificate_path", "")
    config.set("lnd", "network", "mainnet")
    config.set("lnd", "macaroon_admin", "")
    config.set("lnd", "macaroon_admin_path", "")
    config.set("lnd", "path", "")
    config.set("lnd", "conf_path", "")
    config.set("lnd", "log_path", "")
    config.set("lnd", "channel_db_path", "")
    config.set("lnd", "stop_cmd", "")
    config.set("lnd", "start_cmd", "")
    config.add_section("display")
    config.set("display", "channel_length", 1000)
    config.set("display", "inverted_channels", 0)
    config.set("display", "show_sent_received", 1)
    config.set("display", "channel_opacity", 0.3)
    config.set("display", "channels_background_color", "#000003")
    config.set("display", "channel_sort_criteria", "ratio")
    config.set("display", "1m_color", "#64ff64ff")
    config.set("display", "node_background_color", "#505050")
    config.set("display", "node_selected_background_color", "#969696")
    config.set("display", "node_width", 70)
    config.set("display", "node_height", 100)
    config.set("display", "node_alias_font_size", "80sp")
    config.set("display", "round_central_node", False)
    config.set("display", "currency", "SAT")
    config.set("display", "primary_palette", "Red")
    config.add_section("audio")
    config.set("audio", "volume", 0.2)
    config.add_section("autobalance")
    config.set("autobalance", "enable", 0)
    config.add_section("debug")
    config.set("debug", "layouts", 0)
    config.set("debug", "htlcs", True)
    config.add_section("shortcuts")
    config.set("shortcuts", "toggle_chords", "shift c")
    config.set("shortcuts", "next_chord", "j")
    config.set("shortcuts", "prev_chord", "k")
    config.add_section("path")
    config.set("path", "video", "videos")
    config.set("path", "db", "store/dbs")
    config.set("path", "yaml", "store/yaml")
    config.set("path", "json", "store/json")
    config.set("path", "cert", "certs")
    config.set("path", "app", "apps")
    config.set("path", "export", "exports")
    config.set("path", "app_archive", "exports/archives")
    config.set("path", "trash", ".trash")
    config.set("path", "download", ".downloads")
    config.set("path", "PYTHONPATH", "")
    config.add_section("url")
    config.set("url", "appstore", "https://lnappstore.com")
    config.add_section("system")
    config.set("system", "identifier", "plyer")
    config.set("system", "orb_version", "undefined")
