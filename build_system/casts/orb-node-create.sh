# @Author: lnorb.com
# @Date:   2022-09-06 15:08:11
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-09-07 06:35:34

orb node create \
    --hostname signet.lnd.lnorb.com \
    --protocol rest \
    --node-type lnd \
    --network signet \
    --rest-port 8080 \
    --mac-hex $MAC_HEX \
    --cert-hex $CERT_HEX

#$ expect created