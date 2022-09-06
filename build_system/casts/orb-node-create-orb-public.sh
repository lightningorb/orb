# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-09-06 14:55:53
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-09-06 15:13:09

orb node create-orb-public cln rest
#$ wait 1000
orb node info
#$ wait 1000
orb node delete
#$ wait 1000

orb node create-orb-public lnd rest
#$ wait 1000
orb node info
#$ wait 1000
orb node delete
#$ wait 1000

orb node create-orb-public lnd grpc
#$ wait 1000
orb node info
#$ wait 1000
orb node delete
#$ wait 1000
