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

# SSH Tunnel

You'll need to decide whether to access your node directly, or use an SSH tunnel. To tunnel:

```bash
ssh -L 10009:localhost:10009 -N <username>@<host_ip> -i <path_to_pem>
```

# Direct connection

If you want to connect to your node directly, without an SSH tunnel, you may need to add your node's IP to your lnd.conf, since by default, LND only serves requests on localhost.

tlsextraip=<your_node_ip>

(please note the `tlsextraip=` line may appear multiple times).

Then restart lnd.

# Firewall

If you've opted for a direct connection, then on your node you'll need to open up port `10009` (or `8080` for IOS users).

```
sudo ufw allow 10009
sudo ufw allow 8080
```

# cert and macaroon

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


