# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-01-28 05:50:01
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-01-29 04:33:17

from invoke import task


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
