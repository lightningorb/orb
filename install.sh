# @Author: w
# @Date:   2022-09-03 21:24:13
# @Last Modified by:   w
# @Last Modified time: 2022-09-03 23:45:03
# Determine OS platform

cd

UNAME=$(uname | tr "[:upper:]" "[:lower:]")
if [ "$UNAME" == "linux" ]; then
    if [ -f /etc/lsb-release -o -d /etc/lsb-release.d ]; then
        export DISTRO=$(lsb_release -i | cut -d: -f2 | sed s/'^\t'//)
    else
        export DISTRO=$(ls -d /etc/[A-Za-z]*[_-][rv]e[lr]* | grep -v "lsb" | cut -d'/' -f3 | cut -d'-' -f1 | cut -d'_' -f1)
    fi
fi
[ "$DISTRO" == "" ] && export DISTRO=$UNAME
unset UNAME

if [[ $DISTRO == 'Ubuntu' ]]; then
    RELEASE=$(cat /etc/lsb-release | grep DISTRIB_RELEASE | cut -d = -f 2)
    if [[ $RELEASE == '20.04' ]]; then
        curl https://lnorb.s3.us-east-2.amazonaws.com/customer_builds/orb-0.21.7-ubuntu-20.04-x86_64.tar.gz | tar xvz;
        sudo apt-get install curl tar python3.8-venv;
        cd orb;
        python3 -m venv venv;
        source venv/bin/activate;
        bash bootstrap_ubuntu_20_04.sh;
        ALIAS_CMD="alias orb='~/orb/venv/bin/python ~/orb/main.py ${*}'"
        eval $ALIAS_CMD
        if ! grep -q 'alias orb' ~/.bashrc; then
            echo $ALIAS_CMD >> ~/.bashrc;
        fi
        echo "Orb successfully installed"
        echo "LAUNCH A NEW TERMINAL, THEN:"
        echo "To launch the UI, run: orb"
        echo "To explore the CLI, run orb --help"
        echo "To read the docs, head over to https://lnorb.com/docs"
    fi
fi

if [[ $DISTRO == 'darwin' ]]; then
    cd /tmp/
    OSX_MAJOR_VERSION=$(sw_vers | grep ProductVersion | cut -d : -f 2 | xargs | cut -d . -f 1)
    DMG="orb-0.21.7-macos-${OSX_MAJOR_VERSION}-x86_64.dmg"
    curl https://lnorb.s3.us-east-2.amazonaws.com/customer_builds/${DMG} -o ${DMG}
    sudo hdiutil attach ${DMG}
    sudo rm -rf /Applications/lnorb.app
    sudo cp -r /Volumes/Orb/lnorb.app /Applications/
fi
