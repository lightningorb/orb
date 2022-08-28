# -*- mode: python ; coding: utf-8 -*-

from kivy_deps import glew, sdl2
from pathlib import Path

block_cipher = None

a = Analysis(
    ["main.py"],
    pathex=[
        "third_party/arrow",
        "third_party/bezier",
        "third_party/colour",
        "third_party/contextmenu",
        "third_party/currency-symbols",
        "third_party/forex-python",
        "third_party/python-qrcode",
        "third_party/deezy-py",
        "dist\\obf\\temp",
    ],
    binaries=[],
    datas=[
        ("orb/audio/link_fail_event.wav", "orb/audio/"),
        ("orb/audio/forward_settle.wav", "orb/audio/"),
        ("orb/audio/send_settle.wav", "orb/audio/"),
        ("orb/lnd/grpc_generated", "orb/lnd/grpc_generated"),
        ("tests", "tests"),
        ("orb/images/shadow_inverted.png", "orb/images/"),
        ("orb/misc/settings.json", "orb/misc/"),
        ("orb/apps/auto_fees/autofees.py", "orb/apps/auto_fees/"),
        ("orb/apps/auto_fees/autofees.kv", "orb/apps/auto_fees/"),
        ("orb/apps/auto_fees/autofees.png", "orb/apps/auto_fees/"),
        ("orb/apps/auto_fees/appinfo.yaml", "orb/apps/auto_fees/"),
        ("orb/apps/auto_rebalance/autobalance.py", "orb/apps/auto_rebalance/"),
        ("orb/apps/auto_rebalance/autobalance.kv", "orb/apps/auto_rebalance/"),
        ("orb/apps/auto_rebalance/autobalance.png", "orb/apps/auto_rebalance/"),
        ("orb/apps/auto_rebalance/appinfo.yaml", "orb/apps/auto_rebalance/"),
        ("orb/apps/auto_max_htlcs/update_max_htlc.py", "orb/apps/auto_max_htlcs/"),
        ("orb/apps/auto_max_htlcs/update_max_htlcs.png", "orb/apps/auto_max_htlcs/"),
        ("orb/apps/auto_max_htlcs/appinfo.yaml", "orb/apps/auto_max_htlcs/"),
        ("images/ln.png", "images/"),
        ("VERSION", "."),
    ],
    hiddenimports=[
        "orb.core_ui.kvs",
        "orb.misc",
        "kivymd.effects.stiffscroll.StiffScrollEffect",
        "pkg_resources",
        "plyer.platforms.win.notification",
        "plyer.platforms.win.uniqueid",
        "pytransform",
    ],  # 'pandas.plotting._matplotlib',
    hookspath=["dist\\obf\\temp"],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# Patched by PyArmor
_src = "D:\\a\\orb\\orb"
for i in range(len(a.scripts)):
    if a.scripts[i][1].startswith(_src):
        x = a.scripts[i][1].replace(_src, r"D:\a\orb\orb\dist\obf")
        if os.path.exists(x):
            a.scripts[i] = a.scripts[i][0], x, a.scripts[i][2]
for i in range(len(a.pure)):
    if a.pure[i][1].startswith(_src):
        x = a.pure[i][1].replace(_src, r"D:\a\orb\orb\dist\obf")
        if os.path.exists(x):
            if hasattr(a.pure, "_code_cache"):
                with open(x) as f:
                    a.pure._code_cache[a.pure[i][0]] = compile(
                        f.read(), a.pure[i][1], "exec"
                    )
            a.pure[i] = a.pure[i][0], x, a.pure[i][2]
# Patch end.

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="lnorb",
    debug=True,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],
    strip=False,
    upx=True,
    upx_exclude=[],
    name="lnorb"
)
