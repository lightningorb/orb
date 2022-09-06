# @Author: lnorb.com
# @Date:   2022-09-06 15:36:57
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-09-06 15:38:53

orb node ssh-wizard \
    --hostname regtest.cln.lnorb.com \
    --node-type cln \
    --ssh-cert-path lnorb-com.cer \
    --network regtest \
    --rest-port 3001 \
    --ssh-port 22 \
    --ssh-user ubuntu \
    --protocol rest \
    --ln-cert-path /home/ubuntu/dev/regtest-workbench/certificate.pem \
    --ln-macaroon-path /home/ubuntu/dev/regtest-workbench/access.macaroon