# @Author: w
# @Date:   2022-09-03 21:24:13
# @Last Modified by:   w
# @Last Modified time: 2022-09-06 08:54:34
# Determine OS platform

set -e
shopt -s expand_aliases

function main() {
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
            curl https://lnorb.s3.us-east-2.amazonaws.com/customer_builds/orb-<VERSION>-ubuntu-20.04-x86_64.tar.gz | tar xvz;
            sudo apt-get update;
            sudo apt-get install python3.8-venv -y;
            cd orb;
            python3 -m venv venv;
            source venv/bin/activate;
            bash bootstrap_ubuntu_20_04.sh;
            ALIAS_CMD="alias orb='~/orb/venv/bin/python ~/orb/main.py ${*}'"
            eval $ALIAS_CMD
            if ! grep -q 'alias orb' ~/.bashrc; then
                echo $ALIAS_CMD >> ~/.bashrc;
            fi
            print_success_message '~/.bashrc';
        else
            not_supported;
        fi
    elif [[ $DISTRO == 'darwin' ]]; then
        cd /tmp/;
        OSX_MAJOR_VERSION=$(sw_vers | grep ProductVersion | cut -d : -f 2 | xargs | cut -d . -f 1);
        if [ $OSX_MAJOR_VERSION -gt 11 ]; then
            OSX_MAJOR_VERSION=11;
        fi
        DMG="orb-<VERSION>-macos-${OSX_MAJOR_VERSION}-x86_64.dmg";
        curl https://lnorb.s3.us-east-2.amazonaws.com/customer_builds/${DMG} -o ${DMG};
        sudo hdiutil attach ${DMG};
        sudo rm -rf /Applications/lnorb.app;
        sudo cp -r /Volumes/Orb/lnorb.app /Applications/;
        ALIAS_CMD="alias orb='/Applications/lnorb.app/Contents/MacOS/lnorb'"
        eval $ALIAS_CMD
        if ! grep -q 'alias orb' ~/.bash_profile; then
            echo $ALIAS_CMD >> ~/.bash_profile;
        fi
        print_success_message '~/.bash_profile';
    else
        not_supported;
    fi

}

function declare_colors() {
    NOCOLOR='\033[0m'
    RED='\033[0;31m'
    GREEN='\033[0;32m'
    ORANGE='\033[0;33m'
    BLUE='\033[0;34m'
    PURPLE='\033[0;35m'
    CYAN='\033[0;36m'
    LIGHTGRAY='\033[0;37m'
    DARKGRAY='\033[1;30m'
    LIGHTRED='\033[1;31m'
    LIGHTGREEN='\033[1;32m'
    YELLOW='\033[1;33m'
    LIGHTBLUE='\033[1;34m'
    LIGHTPURPLE='\033[1;35m'
    LIGHTCYAN='\033[1;36m'
    WHITE='\033[1;37m'
}

function not_supported() {
    echo -e "The installer was never run on your OS / Distro - please drop by our ${LIGHTBLUE} tech support group ${NOCOLOR} 💻 so we can update this installer for your distro: https://t.me/+ItWJsyOBlDBjMmRl"
}

function print_success_message(){
    clear;
    echo -e "==========================="
    echo -e "Orb successfully installed."
    echo -e "===========================\n"
    echo -e "Please run ${LIGHTBLUE}source ${1};${NOCOLOR} or launch a NEW TERMINAL:\n"
    echo -e "To launch the UI: ${LIGHTBLUE}orb${NOCOLOR}"
    echo -e "To explore the CLI: ${LIGHTBLUE}orb --help${NOCOLOR}"
    echo -e "To read the docs, head over to: ${LIGHTGREEN}https://lnorb.com/docs${NOCOLOR}"
}

declare_colors;
main;
