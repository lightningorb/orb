# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-01-14 06:37:53
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-01-14 07:18:01

import os

from invoke import task


@task
def create(c, env=dict(PATH=os.environ["PATH"])):
    tag_commits = c.run(
        "git log $(git describe --tags --abbrev=0)..HEAD --oneline", env=env, hide=True
    ).stdout

    notes = "\n".join(x[8:] for x in tag_commits.split("\n"))
    open("orb/dialogs/help_dialog/release_notes/release_notes.txt", "w").write(notes)
