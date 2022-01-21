# -*- mode: python ; coding: utf-8 -*-

from kivy import kivy_data_dir
from kivy.tools.packaging import pyinstaller_hooks as hooks
from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen, NoTransition
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.checkbox import CheckBox
from pathlib import Path

from pathlib import Path
kv = [(path.absolute().as_posix(), 'Resources') for path in Path('../orb').rglob('*.kv')]
settings = [(Path('../orb/misc/settings.json').absolute().as_posix(), 'misc')]
ini = [(Path('../orb.ini').absolute().as_posix(), 'core_ui') ]
context_menu_kv = [ ('../third_party/contextmenu/kivy_garden/contextmenu/context_menu.kv', 'kivy_garden/contextmenu/'),
                    ('../third_party/contextmenu/kivy_garden/contextmenu/context_menu.py', 'kivy_garden/contextmenu/'),
                    ('../third_party/contextmenu/kivy_garden/contextmenu/app_menu.kv', 'kivy_garden/contextmenu/'),
                    ('../third_party/contextmenu/kivy_garden/contextmenu/app_menu.py', 'kivy_garden/contextmenu/'),
                    ]
datas = kv + settings + ini + context_menu_kv
block_cipher = None

a = Analysis(['../main.py'],
             pathex=[],
             binaries=[],
             datas=datas,
             hiddenimports=['../orb/lnd/grpc_generated/invoices_pb2.py',
                            '../orb/lnd/grpc_generated/invoices_pb2_grpc.py',
                            '../third_party/contextmenu/kivy_garden/contextmenu/app_menu.py',
                            
                            ],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=['_tkinter', 'Tkinter', 'enchant', 'twisted'],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(pyz,
          a.scripts, 
          [],
          exclude_binaries=True,
          name='orb',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None )

coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas, 
               strip=False,
               upx=True,
               upx_exclude=[],
               name='orb')

app = BUNDLE(coll,
             name='orb.app',
             icon=None,
             bundle_identifier=None)
