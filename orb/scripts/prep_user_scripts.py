# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-01-08 09:31:12
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-01-08 09:35:15

import json
from glob import glob


def comment_out(content):
    return "\n".join(f"# {l}" for l in content.split("\n"))


user_scripts = {}
for g in ["user/scripts/*.py", "fees.yaml", "autobalance.yaml"]:
    for f in glob(g):
        content = open(f).read()
        user_scripts[f] = comment_out(content) if ".yaml" in g else content

with open("user_scripts.json", "w") as f:
    f.write(json.dumps(user_scripts, indent=4))

print("user_scripts.json should be good")
