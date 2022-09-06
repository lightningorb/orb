# @Author: lnorb.com
# @Date:   2022-09-06 15:41:49
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-09-06 15:57:12

orb node ssh-fetch-certs \
    --hostname regtest.cln.lnorb.com \
    --ssh-cert-path lnorb-com.cer \
    --ssh-port 22 \
    --ssh-user ubuntu \
    --ln-cert-path /home/ubuntu/dev/regtest-workbench/certificate.pem \
    --ln-macaroon-path /home/ubuntu/dev/regtest-workbench/access.macaroon

orb node create-from-cert-files \
    --hostname regtest.cln.lnorb.com \
    --node-type cln \
    --protocol rest \
    --network regtest \
    --rest-port 3001 \
    --mac-file-path access.macaroon \
    --cert-file-path certificate.pem

