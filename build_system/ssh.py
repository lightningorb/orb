# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-07-10 07:23:54
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-07-10 07:29:44

from invoke import task
import os


@task
def mosh(c, env=os.environ):
    c.run(
        """mosh --ssh 'ssh -i lnorb_com.cer' --predict experimental --noinit ubuntu@lnorb.com """,
        env=env,
    )
