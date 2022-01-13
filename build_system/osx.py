# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-01-13 11:40:47
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-01-13 11:40:47

# build:
#     pyinstaller -y --clean --windowed orb.spec
#     cd dist && hdiutil create ./orb.dmg -srcfolder orb.app -ov
#     cp orb.ini dist/orb/

# spec:
#     pyinstaller -y --clean --windowed --name orb --exclude-module _tkinter --exclude-module Tkinter --exclude-module enchant   --exclude-module twisted main.py
