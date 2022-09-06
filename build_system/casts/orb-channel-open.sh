# @Author: lnorb.com
# @Date:   2022-09-06 15:28:25
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-09-06 17:04:50

export ORB_CLI_NO_COLOR=1

pk=`orb peer list | head -n 1`

orb channel open $pk 10_000_000 1