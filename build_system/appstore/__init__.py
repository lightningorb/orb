# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-01-20 08:46:25
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-01-20 08:49:29

from invoke import Collection

from . import local
from . import remote

namespace = Collection(local, remote)
