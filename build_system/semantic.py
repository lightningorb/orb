# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-01-13 11:01:23
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-01-13 11:01:28

import semver

get_ver = lambda: semver.VersionInfo.parse(open("VERSION").read().strip())
save_ver = lambda ver: open("VERSION", "w").write(str(ver))
