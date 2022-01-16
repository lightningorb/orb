# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-01-14 06:37:53
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-01-17 03:44:22

import os

from invoke import task


@task
def create(c, env=dict(PATH=os.environ["PATH"])):
    cmd = lambda x: c.run(x, env=env, hide=True).stdout
    tags = ([x for x in cmd("git tag").split("\n") if x] + ["HEAD"])[::-1]
    current_version = open("VERSION").read().strip()
    notes = ""
    for prev_tag, tag in zip(tags, tags[1:]):
        notes += f"{(prev_tag, current_version)[prev_tag == 'HEAD']:}\n{'-'*len(prev_tag)}\n\n"
        tag_commits = cmd(f"git log {tag}..{prev_tag} --oneline")
        notes += "\n".join(x[8:] for x in tag_commits.split("\n")) + "\n\n"
    open("orb/dialogs/help_dialog/release_notes/release_notes.txt", "w").write(notes)
