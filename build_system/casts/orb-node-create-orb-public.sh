# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2022-09-06 14:55:53
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-09-09 15:45:16

orb node create-orb-public cln rest
#$ expect as default
orb node info
#$ expect num_inactive_channels
orb node delete
#$ expect deleted

orb node create-orb-public lnd rest
#$ expect as default
orb node info
#$ expect num_inactive_channels
orb node delete
#$ expect deleted

orb node create-orb-public lnd grpc
#$ expect as default
orb node info
#$ expect num_inactive_channels
orb node delete
#$ expect deleted
