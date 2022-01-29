# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-01-28 05:20:45
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-01-29 04:39:24

from invoke import task
import os


@task
def ssh(c):
    os.system("ssh -i lnorb_com.cer ubuntu@lnorb.com")
