# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-01-28 05:50:01
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-01-28 14:04:27

from invoke import task

# sudo apt-get update
# sudo apt-get -y install python3-pip
# sudo apt update -y
# sudo apt install software-properties-common  -y
# sudo add-apt-repository ppa:deadsnakes/ppa  -y
# sudo apt install python3.9  -y
# curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
# sudo python3.9 get-pip.py
# pip3.9 install kivymd==0.104.2 --user;
# pip3.9 install peewee==3.14.8 --user;
# pip3.9 install python-dateutil==2.8.2 --user;
# pip3.9 install kivy_garden.graph==0.4.0 --user;
# pip3.9 install PyYaml==6.0 --user;
# pip3.9 install simplejson==3.17.6 --user;
# pip3.9 install Kivy==2.0.0 --user;
# pip3.9 install google-api-python-client --user;
# pip3.9 install grpcio --user;
# pip3.9 install ffpyplayer==4.2.0 --user;
# pip3.9 install python-dateutil==2.8.2 --user;
# pip3.9 install pyinstaller --user;
# pip3.9 install pyarmor==6.6.2 --user;
# pip3.9 install fabric --user;
# pip3.9 install plyer --user;
# pip3.9 install semver --user;


@task
def requirements(c):
    c.run("pip3 install --upgrade cython")
    c.run(
        "sudo apt-get install ffmpeg libavcodec-dev libavdevice-dev libavfilter-dev libavformat-dev \
    libavutil-dev libswscale-dev libswresample-dev libpostproc-dev libsdl2-dev libsdl2-2.0-0 \
    libsdl2-mixer-2.0-0 libsdl2-mixer-dev python3-dev"
    )


@task
def upload(c):
    c.run(
        "rsync -e 'ssh -i lnorb_com.cer' -azv --progress --partial tmp/orb.tar.gz ubuntu@lnorb.com:/home/ubuntu/lnorb_com/releases/orb-0.8.0-universal.tar.gz"
    )
