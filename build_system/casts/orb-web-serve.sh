# @Author: lnorb.com
# @Date:   2022-09-06 15:08:11
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-09-07 12:23:07

#$ wait 2000

orb web serve &> /dev/null & disown

pid=$!

curl localhost:8080/info 2>/dev/null | jq

#$ expect channels

kill $pid