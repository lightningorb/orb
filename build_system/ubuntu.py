# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-01-28 05:50:01
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-01-28 05:51:24

from invoke import task


@task
def requirements(c):
    c.run(
        "sudo apt-get install ffmpeg libavcodec-dev libavdevice-dev libavfilter-dev libavformat-dev \
    libavutil-dev libswscale-dev libswresample-dev libpostproc-dev libsdl2-dev libsdl2-2.0-0 \
    libsdl2-mixer-2.0-0 libsdl2-mixer-dev python3-dev"
    )
    c.run("pip install --upgrade cython")
