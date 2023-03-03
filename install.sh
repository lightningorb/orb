# @Author: w
# @Date:   2022-09-03 21:24:13
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-10-01 07:08:37
# Determine OS platform

set -e

function main() {
    cd # change to the user's home directory

    # Determine the Linux distribution being used
    UNAME=$(uname | tr "[:upper:]" "[:lower:]")
    if [ "$UNAME" == "linux" ]; then
        if [ -f /etc/lsb-release -o -d /etc/lsb-release.d ]; then
            export DISTRO=$(lsb_release -i | cut -d: -f2 | sed s/'^\t'//) # if /etc/lsb-release exists, use it to get the distro name
        else
            export DISTRO=$(ls -d /etc/[A-Za-z]*[_-][rv]e[lr]* | grep -v "lsb" | cut -d'/' -f3 | cut -d'-' -f1 | cut -d'_' -f1) # otherwise, try to guess the distro based on the contents of /etc/
        fi
    fi
    [ "$DISTRO" == "" ] && export DISTRO=$UNAME # if no distro is found, use the value of UNAME
    unset UNAME

    # Install Orb on Ubuntu
    if [[ $DISTRO == 'Ubuntu' ]]; then
        curl -L https://github.com/lightningorb/orb/releases/download/v<VERSION>/orb-<VERSION>-ubuntu-20.04-x86_64.tar.gz | tar xvz; # download and extract the Orb installation files
        sudo apt-get update; # update the package list
        sudo apt-get install python3.8-venv -y; # install the Python virtual environment package
        cd orb; # navigate to the extracted Orb directory
        python3 -m venv venv; # create a Python virtual environment
        source venv/bin/activate; # activate the virtual environment
        bash bootstrap_ubuntu_20_04.sh; # run the Ubuntu-specific bootstrap script
        sudo sh -c "echo '~/orb/venv/bin/python ~/orb/main.py \${*}' > /usr/local/bin/orb;" # create a symlink to the Orb executable in /usr/local/bin/
        sudo chmod 755 /usr/local/bin/orb; # make the symlink executable
        hash -r; # reset the shell's command cache
        print_success_message; # print a success message
    # Install Orb on macOS
    elif [[ $DISTRO == 'darwin' ]]; then
        cd /tmp/; # change to the /tmp directory
        # Query OS for OSX version. Only 10.15 and 11 and explicitly supported here 
        OSX_MAJOR_VERSION=$(sw_vers | grep ProductVersion | cut -d : -f 2 | xargs | cut -d . -f 1); # get the major version number of macOS
        OSX_VERSION=$OSX_MAJOR_VERSION
        # If the major version is 10, use 10.15
        if [ $OSX_MAJOR_VERSION == 10 ]; then
            OSX_VERSION="10.15";
        fi
        # For all other versions (11 and greater) use the 11 build
        if [ $OSX_MAJOR_VERSION -gt 11 ]; then
            OSX_VERSION=11;
        fi
        # The VERSION below must get substituted by the install script
        DMG="orb-<VERSION>-macos-${OSX_VERSION}-x86_64.dmg"; # construct the name of the Orb DMG file
        # Install Orb on macOS (continued)
        if [[ ! -f ${DMG} ]]; then # check if the DMG file has already been downloaded
            DMG_DL_PATH=https://github.com/lightningorb/orb/releases/download/v<VERSION>/${DMG}
            echo $DMG_DL_PATH
            curl -L $DMG_DL_PATH -o /tmp/orb_dl_tmp; # download the DMG file
            mv /tmp/orb_dl_tmp ${DMG}; # rename the downloaded file to the correct name
        fi
        if [[ -d /Volumes/Orb ]]; then # check if the Orb volume is already mounted
            sudo umount /Volumes/Orb; # unmount the Orb volume if it is already mounted
        fi
        sudo hdiutil attach ${DMG}; # mount the DMG file
        sudo rm -rf /Applications/lnorb; # remove any existing Orb installation
        sudo cp -r /Volumes/Orb/lnorb /Applications/; # copy the new Orb installation to the /Applications directory
        sudo echo '/Applications/lnorb/Contents/MacOS/lnorb' > /usr/local/bin/orb; # create a symlink to the Orb executable in /usr/local/bin/
        sudo chmod 755 /usr/local/bin/orb; # make the symlink executable
        hash -r; # reset the shell's command cache
        print_success_message; # print a success message
    else
        not_supported; # if the operating system is not Ubuntu or macOS, print a not supported message
    fi
}

# Define a set of colors for use in printing messages
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

# Print a message indicating that the current OS or distribution is not supported
function not_supported() {
    echo -e "The installer was never run on your OS / Distro - please drop by our ${LIGHTBLUE} tech support group ${NOCOLOR} 💻 so we can update this installer for your distro: https://t.me/+ItWJsyOBlDBjMmRl"
}

# Print a message indicating that the installation was successful
function print_success_message(){
    clear;
    echo -e "==========================="
    echo -e "Orb successfully installed."
    echo -e "===========================\n"
    echo -e "To launch the UI: ${LIGHTBLUE}orb${NOCOLOR}"
    echo -e "To explore the CLI: ${LIGHTBLUE}orb --help${NOCOLOR}"
    echo -e "To read the docs, head over to: ${LIGHTGREEN}https://lnorb.com/docs${NOCOLOR}"
}

# Define a set of colors to use in printing messages
declare_colors;

# Call the main function to start the installation process
main;
