# @Author: lnorb.com
# @Date:   2022-09-06 15:08:11
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-09-07 06:07:04

#$ delay 0

addr=tb1q8xf4zl65qtvlqrk6d8p4f46al3yzyqj7ypg5n7

#$ delay 30

orb chain send $addr 100_000 1

#$ expect txid

#$wait 2000

