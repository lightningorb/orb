# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-01-28 05:20:45
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-01-28 13:19:39

from invoke import task


@task
def ssh(c):
    c.run("ssh -i lnorb_com.cer ubuntu@lnorb.com")
