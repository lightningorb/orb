# Installation

First create a github access token:

https://github.com/settings/tokens

Save it somehwere safe. Then:

```bash
git clone https://<github_username>@github.com/bc31164b-cfd5-4a63-8144-875100622b2d/orb.git

# enter token when prompted for password
git config --global credential.helper store
cd orb
pip3 install -r requirements.txt
sudo apt-get install -y xclip xsel # Linux users only
python3 main.py

```

# Build system

As orb needs to target multiple platforms, its build system is getting inevitably more complex. For this reason, orb is now using fabric.

```python3
pip3 install fabric
./build.py -l
```

The above command lists out the available build commands. At the time of writing these are:

    Available tasks:

      deploy-ios
      appstore.local.create-db
      appstore.local.start
      appstore.remote.certbot
      appstore.remote.clone
      appstore.remote.create-db
      appstore.remote.create-tables
      appstore.remote.create-user
      appstore.remote.drop-tables
      appstore.remote.install-nginx-conf
      appstore.remote.install-service
      appstore.remote.install-stack
      appstore.remote.requirements
      appstore.remote.start
      appstore.remote.start-dev
      documentation.build                  Build the docs. Requires sphinx.
      documentation.clean                  Delete the built docs. Useful when renaming modules etc.
      documentation.view                   View docs in the browser.
      host.ssh
      ios.create                           Create the xcode project.
      ios.toolchain
      ios.toolchain-build
      ios.toolchain-pip
      ios.update                           Update the xcode project with the latest changes.
      osx.dmg
      osx.gen-license
      osx.requirements
      osx.run
      osx.upload
      release-notes.create
      submodules.remove-all                Delete the relevant section from the .gitmodules file.
      tags.push
      tags.tag
      test.test                            Run the unit tests and doctests.
      third-party.clean                    Stub.
      third-party.clone                    Stub.
      ubuntu.requirements
      versioning.bump-build                Bump the build number using semver and store in VERSION.
      versioning.bump-major                Bump the major version using semver and store in VERSION.
      versioning.bump-minor                Bump the minor version using semver and store in VERSION.
      versioning.bump-patch                Bump the patch version using semver and store in VERSION.
      versioning.bump-pre                  Bump the pre-release using semver and store in VERSION.

## Building on Ubuntu

```bash

pip3 install fabric
python3 build.py ubuntu.requirements

```

# Connecting your node

https://lnorb.com/docs/installing.html

# Resolution

DPI, screen density and font scale can all be altered to match your preference.

Examples:

```
KIVY_DPI=320 KIVY_METRICS_DENSITY=2 python3 main.py
KIVY_DPI=240 KIVY_METRICS_DENSITY=1.5 python3 main.py
KIVY_METRICS_FONTSCALE=1.2 python3 main.py
```

# Building for IOS

The guides for building & running a Kivy app on IOS are actually pretty good, and the steps are 'somewhat' predictable.

Please make sure you have a recent version of XCode installed. Successful builds have taken place with:

IOS 11.6 (20G165)
XCODE 13.0 (13A233)

https://kivy.org/doc/stable/guide/packaging-ios.html

```
brew install autoconf automake libtool pkg-config
brew link libtool
pip3 install kivy-ios
toolchain build kivy
toolchain build pillow
```

When building the toolchain, if you get an error along the lines of:

```
xcrun: error: SDK "iphonesimulator" cannot be located
```

Then you may need to set the correct location for the XCode's SDK:

```
sudo xcode-select --switch /Applications/Xcode.app/Contents/Developer/
```

If you succeeded id building kivy with the IOS toolchain, then install all the requirements via toolchain:

```
toolchain pip3 install qrcode
toolchain pip3 install kivymd
toolchain pip3 install kivy_garden.contextmenu
toolchain pip3 install pygments
toolchain pip3 install peewee
toolchain pip3 install arrow
toolchain pip3 install kivy_garden.graph
toolchain pip3 install humanize
toolchain pip3 install currency-symbols
toolchain pip3 install forex-python
toolchain pip3 install colour
toolchain pip3 install PyYaml
toolchain pip3 install ffpyplayer
toolchain pip3 install openpyxl
```


You can now create the project:
```
./build.py ios.create
```

Please note this creates the xcode project in `./lnorb-ios`.

You can now open the IOS project with:

```
open orb-ios/orb.xcodeproj
```

You'll need to update the project after each `git pull` or local modification.

```
./build.py ios.update
```

In the XCode project, under 'signing capabilities' make sure to set your team, and a unique identifier.

Under 'Build Phases' you will also need to add the 'AVFAudio.framework' library, and set its status to 'optional'.

In XCode, make sure you add this to your info.plist:

Supports opening documents in place
Application supports iTunes file sharing
Privacy - Camera Usage Description     ->          [enter a reason]

Make sure to replace the icon set with a valid one.

You can now build & launch Kivy on your target IOS device.

To upload to apple connect, select build -> archive.


# SSL

In MacOSX if you get any issues relating to SSL, try installing Python's SSL certs.

/Applications/Python\ 3.10/Install\ Certificates.command
