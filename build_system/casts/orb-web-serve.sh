# @Author: lnorb.com
# @Date:   2022-09-06 15:08:11
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-09-06 17:18:02

orb web serve &> /dev/null

#$ sendcontrol z

bg

#$ wait 1000

curl localhost:8080/info | jq

#$ wait 1000

fg

#$ sendcontrol c