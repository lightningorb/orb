# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-01-13 11:01:23
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-09-22 14:03:45

import semver

get_ver = lambda: semver.VersionInfo.parse(open("VERSION").read().strip())


def save_ver(ver):
    open("VERSION", "w").write(str(ver))
