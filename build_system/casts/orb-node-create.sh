# @Author: lnorb.com
# @Date:   2022-09-07 07:36:36
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-09-09 15:26:41

# does not work due to backslashes

orb node create \
     --hostname signet.lnd.lnorb.com \
     --node-type lnd \
     --protocol rest \
     --network signet \
     --rest-port 8080 \
     --mac-hex $MAC_HEX \
     --cert-hex $CERT_HEX