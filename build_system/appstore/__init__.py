# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-01-20 08:46:25
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-06-22 07:59:16

from invoke import Collection

from . import local_server
from . import remote_server
from . import local_site

namespace = Collection(local_server, remote_server, local_site)
