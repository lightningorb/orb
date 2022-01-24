SECURITY.md
===========

Orb is currently considered secure; there are however some further improvements that can be made; they're covered at the end of this document.

Responsibilities that fall on the user
--------------------------------------

LND and bitcoind are extremely secure and thoroughly tested pieces of software. Since the end-user (You) is the one introducing third-party software (Orb), the risk-assessment and cost / benefit analysis are yours to take. The security onus is on the party (You) introducing new parts (Orb) to the finite software stack.

Allowing external connections to your LND node
----------------------------------------------

Whilst allowing external IPs to connect to your LND node may sound like a liability, it is only as risky / secure as TLS and LND's use of Macaroons are risky / secure.

Which leads us onto the next part.

TLS cert and Macaroon use
-------------------------

Orb does not require any specialized software installed on your LND node. It can connect to an LND node 'out of the box' (this is meant literally - you can create a testnet node on https://voltage.cloud/ and connect to it via Orb in under 2 minutes).

It does so via use of the TLS (Transport Layer Security) certificate, which is the internet-wide / global standard cryptographic protocol for securely communicating over a network.

It also makes use of the read-only or admin macaroon, which is the LND standard for securely granting access rights to your node.

Thus there are no security risks or liabilities associated with anything **node-related** (intrinsic to your node, as opposed to extrinsic -- the risks associated with the use of Orb are solely extrinsic).

As far as communication with the node is concerned, the onus is your node's existing setup, and on LND, and LND follows strict industry standards.

Third Party Libraries
---------------------

When it comes to the use of third-party libraries, *Orb is the party introducing them to the system, thus the onus is on Orb*.

Here are the principles followed by Orb regarding the intrduction and use of third-party libraries:

1. Orb tries to minimize the use of external libraries. IF functionality can be implemented within a reasonable amount of time, versus the use of a third-party library, then the former is preferred.

1. Orb prefers integrating third-party libraries into its codebase over pulling them in via the use of a pypi, pip and requirements.txt. Integrated third-party libraries can be found in the `third_party` directory in the source code, and include:
    
    1. third_party/arrow
    1. third_party/bezier
    1. third_party/colour
    1. third_party/contextmenu
    1. third_party/currency-symbols
    1. third_party/python-forex
    1. third_party/python-qrcode

1. Third-party libraries that still need integrating into Orb's codebase are:

    1. google-api-python-client
    1. kivy
    1. grpcio
    1. kivymd
    1. peewee
    1. kivy_garden.graph
    1. PyYaml
    1. ffpyplayer
    1. simplejson
    1. (probably some more)

1. Orb aims to audit the third-party code it introduces into its stack. This lofty goal is unfortunately very difficult to attain since the volume of code currently exceeds the time-constraints of Orb's development team.

1. Orb does not intend on upgrading third-party libraries often, and prefers the use of old library versions that enjoy a lindy effect over pulling in the library versions whenever they become available.

An issue has been logged for integrating the remaining third-party libraries:

move remaining third party python modules into the code repo and audit them #153

Macaroon copy
-------------

Currently the macaroon is saved in ascii form in orb.ini. This is an area that needs improving, and has been logged under issue:

encrypt tls cert and macroon in orb.ini file #152

Ideally the macaroon ought to be encrypted using the device's mac address and some entropy, for example.

Cert copy
---------

Currently the tls certificate is saved in ascii form in orb.ini, as well as in its own tls.cert file in Orb's app-data folder. This is an area that needs improvement, and has been logged under issues:

save tls.cert into a temp file, not main data directory #151
encrypt tls cert and macroon in orb.ini file #152


App-Store
---------

Orb features an app-store. The app-store introduces a very significant risk, since it allows any node-running Orb user to publish apps that may be downloaded by other Orb users.

There is currently a plan to:

1. add a review process before apps are made available to other users, this process may be sat-incentivized.
1. sign all commits with the author's private key, and verify those signatures during app installs.

Issues have be logged:

add a review process and audit trail for apps published in the store #155

sign app publishes with the node's private key, and verify signatures during installation #156



