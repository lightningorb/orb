#!/bin/bash
# @Author: lnorb.com
# @Date:   2022-09-25 15:56:17
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-09-28 09:09:53

if [ -n "$VNC_PASSWORD" ]; then
    echo -n "$VNC_PASSWORD" > /.password1
    x11vnc -storepasswd $(cat /.password1) /.password2
    chmod 400 /.password*
    sed -i 's/^command=x11vnc.*/& -rfbauth \/.password2/' /etc/supervisor/conf.d/supervisord.conf
    export VNC_PASSWORD=
fi

if [ -n "$X11VNC_ARGS" ]; then
    sed -i "s/^command=x11vnc.*/& ${X11VNC_ARGS}/" /etc/supervisor/conf.d/supervisord.conf
fi

if [ -n "$OPENBOX_ARGS" ]; then
    sed -i "s#^command=/usr/bin/openbox\$#& ${OPENBOX_ARGS}#" /etc/supervisor/conf.d/supervisord.conf
fi

if [ -n "$RESOLUTION" ]; then
    sed -i "s/1024x768/$RESOLUTION/" /usr/local/bin/xvfb.sh
fi

USER=${USER:-root}
HOME=/root
if [ "$USER" != "root" ]; then
    echo "* enable custom user: $USER"
    useradd --create-home --shell /bin/bash --user-group --groups adm,sudo $USER
    if [ -z "$PASSWORD" ]; then
        echo "  set default password to \"ubuntu\""
        PASSWORD=ubuntu
    fi
    HOME=/home/$USER
    echo "$USER:$PASSWORD" | chpasswd
    cp -r /root/{.config,.gtkrc-2.0,.asoundrc} ${HOME}
    chown -R $USER:$USER ${HOME}
    [ -d "/dev/snd" ] && chgrp -R adm /dev/snd
fi
sed -i -e "s|%USER%|$USER|" -e "s|%HOME%|$HOME|" /etc/supervisor/conf.d/supervisord.conf

# home folder
if [ ! -x "$HOME/.config/pcmanfm/LXDE/" ]; then
    mkdir -p $HOME/.config/pcmanfm/LXDE/
    ln -sf /usr/local/share/doro-lxde-wallpapers/desktop-items-0.conf $HOME/.config/pcmanfm/LXDE/
    sed -i 's/stretch/fit/g' $HOME/.config/pcmanfm/LXDE/desktop-items-0.conf
    chown -R $USER:$USER $HOME
fi

mkdir -p ${HOME}/Desktop/
cp /usr/share/applications/sublime_text.desktop ${HOME}/Desktop/
cp /usr/share/applications/lxterminal.desktop ${HOME}/Desktop/
mv /orb.desktop ${HOME}/Desktop/
mkdir -p ${HOME}/.config/pcmanfm/LXDE
mv /pcmanfm.conf ${HOME}/.config/pcmanfm/LXDE

cat <<EOT >> ${HOME}/.bashrc
echo "Welcome to Orb"
echo ""
echo "https://lnorb.com/docs/cli.html"
echo ""
echo "orb --help"
echo ""
orb chain balance
EOT

if [ -n "$HOSTNAME" ]; then
    echo 'mac file path'
    echo ${MAC_FILE_PATH}
    echo 'cert file path'
    echo ${CERT_FILE_PATH}
    ${HOME}/orb/venv/bin/python3 ${HOME}/orb/main.py node create-from-cert-files --hostname ${HOSTNAME} --node-type ${NODE_TYPE} --protocol ${PROTOCOL} --network ${NETWORK} --rest-port ${REST_PORT} --grpc-port ${GRPC_PORT} --mac-file-path ${MAC_FILE_PATH} --cert-file-path ${CERT_FILE_PATH}
fi

sudo chown -R $USER ${HOME}/.config/
sudo chown -R $USER ${HOME}/Desktop

# nginx workers
sed -i 's|worker_processes .*|worker_processes 1;|' /etc/nginx/nginx.conf

# nginx ssl
if [ -n "$SSL_PORT" ] && [ -e "/etc/nginx/ssl/nginx.key" ]; then
    echo "* enable SSL"
    sed -i 's|#_SSL_PORT_#\(.*\)443\(.*\)|\1'$SSL_PORT'\2|' /etc/nginx/sites-enabled/default
    sed -i 's|#_SSL_PORT_#||' /etc/nginx/sites-enabled/default
fi

# nginx http base authentication
if [ -n "$HTTP_PASSWORD" ]; then
    echo "* enable HTTP base authentication"
    htpasswd -bc /etc/nginx/.htpasswd $USER $HTTP_PASSWORD
    sed -i 's|#_HTTP_PASSWORD_#||' /etc/nginx/sites-enabled/default
fi

# dynamic prefix path renaming
if [ -n "$RELATIVE_URL_ROOT" ]; then
    echo "* enable RELATIVE_URL_ROOT: $RELATIVE_URL_ROOT"
    sed -i 's|#_RELATIVE_URL_ROOT_||' /etc/nginx/sites-enabled/default
    sed -i 's|_RELATIVE_URL_ROOT_|'$RELATIVE_URL_ROOT'|' /etc/nginx/sites-enabled/default
fi

# clearup
PASSWORD=
HTTP_PASSWORD=

exec /bin/tini -- supervisord -n -c /etc/supervisor/supervisord.conf

