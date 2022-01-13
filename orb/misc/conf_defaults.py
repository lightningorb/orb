# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-01-06 17:51:07
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-01-13 08:22:14


def set_conf_defaults(config):
    config.add_section("lnd")
    config.set("lnd", "hostname", "localhost")
    config.set("lnd", "rest_port", "8080")
    config.set("lnd", "grpc_port", "10009")
    config.set("lnd", "protocol", "mock")
    config.set("lnd", "tls_certificate", "")
    config.set("lnd", "network", "mainnet")
    config.set("lnd", "macaroon_admin", "")
    config.add_section("display")
    config.set("display", "channel_length", 1000)
    config.set("display", "inverted_channels", 0)
    config.set("display", "show_sent_received", 1)
    config.set("display", "channel_opacity", 0.3)
    config.set("display", "channels_background_color", "#000003")
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
    config.add_section("shortcuts")
    config.set("shortcuts", "toggle_chords", "shift c")
    config.set("shortcuts", "next_chord", "j")
    config.set("shortcuts", "prev_chord", "k")
