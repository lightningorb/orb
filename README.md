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

# Connecting your node

## step 1/

    get your node's IP address or domain name, as visible from the LAN / WAN

## step 2/

    set tlsextraip or tlsextradomain

## step 3/

    shut down LND

## step 4/ 

    $ mv ~/.lnd/tls.cert ~/.lnd/tls.cert.backup
    $ mv ~/.lnd/tls.key ~/.lnd/tls.key.backup

## step 5/

    start LND

## step 6/

    encode TLS CERT

    $ python3 -c 'import base64; print(base64.b64encode(open(".lnd/tls.cert").read().encode()).decode())'

## step 7/ 

    encode Macaroon

    $ python3 -c 'import codecs; print(codecs.encode(open(".lnd/data/chain/bitcoin/mainnet/admin.macaroon", "rb").read(), "hex").decode())'

## step 8/

    copy and paste those strings into Orb

## step 9/

    restart Orb


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