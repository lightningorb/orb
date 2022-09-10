# @Author: lnorb.com
# @Date:   2022-09-06 15:47:00
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-09-06 15:50:56

orb node ssh-fetch-certs \
    --hostname regtest.cln.lnorb.com \
    --ssh-cert-path lnorb_com.cer \
    --ssh-port 22 \
    --ssh-user ubuntu \
    --ln-cert-path /home/ubuntu/dev/regtest-workbench/certificate.pem \
    --ln-macaroon-path /home/ubuntu/dev/regtest-workbench/access.macaroon