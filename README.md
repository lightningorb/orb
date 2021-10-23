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

Encode your macaroon to hex, so you can paste it into the application:

```
python3 -c 'import codecs; print(codecs.encode(open(".lnd/data/chain/bitcoin/mainnet/admin.macaroon", "rb").read(), "hex").decode())'
```

Next cat your cert:

```
cat ~/.lnd/tls.cert
```

And paste that into orb.

Next change the protocol from mock to grpc.

In orb now press 'refresh' to see your channels. If this doesn't work, you may need to restart the application to pick up the new config.

# Example scripts

To write or execute scripts in Orb:

- open up the console (on the bottom left of the screen, click the SE button).
- double-click on the top part of the console to enable input
- Paste one of the following:

## Show alias and pubkey

```python
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput

info =  lnd.get_info()

popup = Popup(title='Node Info',
    content=TextInput(text=f'Alias:\n\n{info.alias}\n\nPublic Key: \n\n{info.identity_pubkey}'),
    size_hint=(None, None), size=(1200, 400))
popup.open()
```

## Fee report

```python
from kivy.uix.popup import Popup
from kivy.uix.label import Label

fr =  lnd.fee_report()

Popup(title='Fee Report',
    content=Label(text=f'Day: S{fr.day_fee_sum:,}\nWeek S{fr.week_fee_sum:,}\nMonth: S{fr.month_fee_sum:,}'),
    size_hint=(None, None), size=(400, 400)).open()

```

## REST API example

```python
import base64, codecs, json, requests
from kivy.app import App
import os
import json

app = App.get_running_app()
data_dir = app.user_data_dir
cert_path = os.path.join(data_dir, 'tls.cert')
hostname = app.config['lnd']['hostname']
rest_port = app.config['lnd']['rest_port']
macaroon = app.config['lnd']['macaroon_admin']
url = f"https://{hostname}:{rest_port}/v1/channels"
headers = {"Grpc-Metadata-macaroon": macaroon.encode()}
r = requests.get(url, headers=headers, verify=cert_path)
print(json.dumps(r.json(), indent=4))
```

## Mempool fee report

```python
import requests

fees = requests.get("https://mempool.space/api/v1/fees/recommended").json()

from kivy.uix.popup import Popup
from kivy.uix.label import Label

text = f"""\
Low priority: {fees["hourFee"]} sat/vB\n
Medium priority: {fees["halfHourFee"]} sat/vB\n
High priority: {fees["fastestFee"]} sat/vB
"""

popup = Popup(
 title='Fee Estimate',
    content=Label(text=text),
    size_hint=(None, None), size=(500, 400),
 background_color = (.6, .6, .8, .7),
 overlay_color = (0, 0, 0, 0)
)

popup.open()
```

## Toggle 'sent-received' overlay

```python
from kivy.app import App

app = App.get_running_app()
show = app.config["display"]["show_sent_received"]
app.config["display"]["show_sent_received"] = "10"[show == "1"]
app.root.ids.sm.get_screen("channels").refresh()
```

## Update fees

```python
from lerp import lerp

LOOP =  '021c97a90a411ff2b10dc2a8e32de2f29d2fa49d41bfbb52bd416e460db0747d0d'
channels = lnd.get_channels()
ratio = sum(c.local_balance for c in channels) / sum(c.capacity for c in channels)

for c in channels:
    if c.remote_pubkey == LOOP:
        fee_rate = (1000, 10000)[c.local_balance < 5e6]
    else:
        fee_rate = int(lerp(0, 1000, c.remote_balance / c.capacity))
    print(f"Updating {lnd.get_node_alias(c.remote_pubkey)}: {fee_rate}")
    lnd.update_channel_policy(channel=c, fee_rate=fee_rate/1e6, time_lock_delta=44)
```

## Get last payment

In this example, rather than using the `lnd` object that magically exists within our scope, we import the relevant functions from the `prefs` module.

This pattern should remain quite consistent, and make it very easy to copy and paste examples from the lighting api docs into the console, and get them working.

```python
import codecs, grpc, os
from grpc_generated import lightning_pb2 as lnrpc
from grpc_generated import lightning_pb2_grpc as lightningstub
from prefs import hostname, cert, macaroon, grpc_port

os.environ['GRPC_SSL_CIPHER_SUITES'] = 'HIGH+ECDSA'
ssl_creds = grpc.ssl_channel_credentials(cert())
channel = grpc.secure_channel(f'{hostname()}:{grpc_port()}', ssl_creds)
stub = lightningstub.LightningStub(channel)

request = lnrpc.ListPaymentsRequest(
        include_incomplete=True,
        index_offset=0,
        max_payments=1,
        reversed=True,
    )

response = stub.ListPayments(request, metadata=[('macaroon', macaroon())])

print(response)
```

------------------------------

You can run the script by either selecting the code (e.g with ctrl-a) and hitting Enter, or with `view > run`.

You can install a script via `view > install`. Name the script, and it will then appear in the `script` menu.

Please note that this internal API is currently subject to change.