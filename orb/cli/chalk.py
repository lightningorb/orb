# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-08-14 11:28:12
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-08-14 11:33:39

import os


class chalk:
    def __getattr__(self, name):
        if os.environ.get("ORB_CLI_NO_COLOR"):
            return lambda x: x
        else:
            from simple_chalk import chalk

            return lambda x: getattr(chalk, name)(x)
