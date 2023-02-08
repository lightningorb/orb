# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-01-06 17:51:07
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-08-21 09:18:08


def set_host_defaults(config, node_config):
    config.add_section("host")
    config.set("host", "type", node_config.get("host", "type", fallback=""))
    config.set("host", "hostname", node_config.get("host", "hostname", fallback=""))


def set_ln_defaults(config, node_config):
    config.add_section("ln")
    config.set(
        "ln", "identity_pubkey", node_config.get("ln", "identity_pubkey", fallback="")
    )
    config.set("ln", "version", node_config.get("ln", "version", fallback=""))
    config.set("ln", "rest_port", node_config.get("ln", "rest_port", fallback="8080"))
    config.set("ln", "grpc_port", node_config.get("ln", "grpc_port", fallback="10009"))
    config.set("ln", "protocol", node_config.get("ln", "protocol", fallback="mock"))
    config.set(
        "ln", "tls_certificate", node_config.get("ln", "tls_certificate", fallback="")
    )
    config.set("ln", "network", node_config.get("ln", "network", fallback="mainnet"))
    config.set(
        "ln",
        "macaroon_admin",
        node_config.get("ln", "macaroon_admin", fallback="mainnet"),
    )


def set_other_defaults(config, node_config):
    config.add_section("display")
    config.set("display", "channel_length", "1000")
    config.set("display", "inverted_channels", "0")
    config.set("display", "show_sent_received", "1")
    config.set("display", "channel_opacity", "0.3")
    config.set("display", "channels_background_color", "#000003")
    config.set("display", "channel_sort_criteria", "ratio")
    config.set("display", "1m_color", "#64ff64ff")
    config.set("display", "node_background_color", "#505050")
    config.set("display", "node_selected_background_color", "#969696")
    config.set("display", "node_width", "70")
    config.set("display", "node_height", "100")
    config.set("display", "node_alias_font_size", "80sp")
    config.set("display", "round_central_node", "False")
    config.set("display", "currency", "SAT")
    config.set("display", "primary_palette", "Red")
    config.add_section("c-lightning-events")
    config.set("c-lightning-events", "hostname", "")
    config.set("c-lightning-events", "protocol", "")
    config.set("c-lightning-events", "port", "")
    config.add_section("audio")
    config.set("audio", "volume", "0.2")
    config.add_section("debug")
    config.set("debug", "layouts", "0")
    config.set("debug", "htlcs", "True")
    config.add_section("shortcuts")
    config.set("shortcuts", "toggle_chords", "shift c")
    config.set("shortcuts", "next_chord", "j")
    config.set("shortcuts", "prev_chord", "k")
    config.add_section("path")
    config.set("path", "video", "videos")
    config.set("path", "db", "store/dbs")
    config.set("path", "yaml", "store/yaml")
    config.set("path", "app_conf", "store/apps_conf")
    config.set("path", "json", "store/json")
    config.set("path", "cert", "certs")
    config.set("path", "app", "apps")
    config.set("path", "export", "exports")
    config.set("path", "backup", "backups")
    config.set("path", "app_archive", "exports/archives")
    config.set("path", "trash", ".trash")
    config.set("path", "download", ".downloads")
    config.set("path", "PYTHONPATH", "")
    config.add_section("url")
    config.set("url", "appstore", "https://lnorb.com")
    config.add_section("system")
    config.set("system", "orb_version", "undefined")


def set_conf_defaults(config, node_config):
    set_host_defaults(config, node_config)
    set_ln_defaults(config, node_config)
    set_other_defaults(config, node_config)
