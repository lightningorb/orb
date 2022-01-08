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

## SSH Tunnel

You'll need to decide whether to access your node directly, or use an SSH tunnel. To tunnel:

```bash
ssh -L 10009:localhost:10009 -N <username>@<host_ip> -i <path_to_pem>
```

## Direct connection

If you want to connect to your node directly, without an SSH tunnel, you may need to add your node's IP to your lnd.conf, since by default, LND only serves requests on localhost.

tlsextraip=<your_node_ip>

(please note the `tlsextraip=` line may appear multiple times).

Then restart lnd.

## Firewall

If you've opted for a direct connection, then on your node you'll need to open up port `10009` (or `8080` for IOS users).

```
sudo ufw allow 10009
sudo ufw allow 8080
```

## cert and macaroon

Encode your macaroon to hex, by running this command in your node's terminal:

```
python3 -c 'import codecs; print(codecs.encode(open(".lnd/data/chain/bitcoin/mainnet/admin.macaroon", "rb").read(), "hex").decode())'
```

Next cat your cert:

```
cat ~/.lnd/tls.cert
```

And paste those into orb.

Next change the protocol from mock to grpc.

In orb now press 'refresh' to see your channels. If this doesn't work, you may need to restart the application to pick up the new config.

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
```


You can now create the project:
```
toolchain create orb lnorb
```

Now assuming this codebase is cloned in `~/dev/orb`

```
toolchain create Touchtracer ~/dev/orb
```

Please note this creates the xcode project in `./orb-ios`.

You can now open the IOS project with:

```
open orb-ios/orb.xcodeproj
```

You'll need to update the project after each `git pull`.

```
toolchain update touchtracer-ios
```

In the XCode project, under 'signing capabilities' make sure to set your team, and a unique identifier.

Under 'Build Phases' you will also need to add the 'AVFAudio.framework' library, and set its status to 'optional'.

In XCode, make sure you add this to your info.plist:

Supports opening documents in place
Application supports iTunes file sharing
Privacy - Camera Usage Description     ->          [enter a reason]

You can now build & launch Kivy on your target IOS device.
