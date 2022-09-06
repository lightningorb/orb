# @Author: lnorb.com
# @Date:   2022-09-06 15:32:28
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-09-06 15:34:58

pk=$(orb peer list | head -n 1)

orb peer connect $pk