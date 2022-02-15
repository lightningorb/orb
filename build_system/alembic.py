# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-02-13 13:32:06
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-02-15 07:22:00

from invoke import task
import os


@task
def revision(c, message, env=os.environ):
    with c.cd("server"):
        c.run(f'alembic revision -m "{message}" --autogenerate', env=env)


@task
def upgrade(c, env=os.environ):
    with c.cd("server"):
        c.run(f"alembic upgrade head", env=env)
