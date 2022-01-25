# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-01-13 11:40:47
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-01-24 08:39:24

# build:
#     pyinstaller -y --clean --windowed orb.spec
#     cd dist && hdiutil create ./orb.dmg -srcfolder orb.app -ov
#     cp orb.ini dist/orb/

# spec:
#     pyinstaller -y --clean --windowed --name orb --exclude-module _tkinter --exclude-module Tkinter --exclude-module enchant   --exclude-module twisted main.py

from invoke import task


@task
def requirements(c, env=dict(PATH=os.environ["PATH"])):
    c.run("pip3 install Kivy==2.1.0.dev0", env=env)
    c.run("pip3 install google-api-python-client", env=env)
    c.run("pip3 install grpcio", env=env)
    c.run("pip3 install ffpyplayer==4.2.0", env=env)
    c.run("pip3 install kivymd==0.104.2", env=env)
    c.run("pip3 install peewee==3.14.8", env=env)
    c.run("pip3 install python-dateutil==2.8.2", env=env)
    c.run("pip3 install kivy_garden.graph==0.4.0", env=env)
    c.run("pip3 install PyYaml==6.0", env=env)
    c.run("pip3 install simplejson==3.17.6", env=env)
