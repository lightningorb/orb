<script>
	import Footer from '../../Components/Footer.svelte';
	import NavbarPlain from '../../Components/NavbarPlain.svelte';
	import { Modal, ModalBody, ModalHeader, Container, Row, Col } from 'sveltestrap';
	import SvelteMarkdown from 'svelte-markdown';

	const source = `
SECURITY.md
===========

Orb takes significant steps to ensure safety for its users and their node, and is, as such, deemed secure; there are however some further improvements that can be made; they're covered at the end of this document.

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

1. Orb prefers integrating third-party libraries into its codebase over pulling them in via the use of a pypi, pip and requirements.txt. Integrated third-party libraries can be found in the third_party directory in the source code, and include:
    
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

Cert and Macaroon Encryption
----------------------------

Orb takes significant steps to store your TLS certificate and macaroon securely.

The TLS certificate, and Macaroon are encrypted (and stored in orb.ini) with an RSA key that is unique to your device. As such, in the highly unlikely event a bad actor were to acquire your orb.ini file, directly from your device, they would still be unable to decrypt your certificate and macaroon without the private key, which is internal to Orb, and not stored anywhere.

This however means a sophisticated bad actor with an intimate knowledge of Orb's source-code (which is available in the app via inspection) and of your device's hardware IDs would still be capable of generating the private key.

This makes attacks via app-store apps still, unfortunately, feasible. App store app attacks are covered later in this document.

Cert copy
---------

Unfortunately the python requests library requires the TLS certificate to be stored on disk. This is a known weakness / vulnerability with no clear or easy workaround.

Orb only creates the file at startup, and deletes it on exit. On mobile it creates it in a temporary folder that is only accessible by Orb.

On Desktop this tls.cert file is stored in the user's data directory/certs and is also deleted on exit.

App-Store
---------

Orb features an app-store. The app-store introduces a very significant risk, since it allows any node-running Orb user to publish apps that may be downloaded by other Orb users.

There is currently a plan to:

1. add a review process before apps are made available to other users, this process may be sat-incentivized.
1. sign all commits with the author's private key, and verify those signatures during app installs.
`;
</script>

<NavbarPlain extraclass="" />

<section class="section common-section text-black" id="priv">
	<div class="display-table">
		<div class="display-table-cell">
			<Container>
				<Row>
					<Col lg={{ size: 8, offset: 2 }}>
						<h1 class="home-title">Security</h1>
						<br />
						<div class="terms">
							<SvelteMarkdown {source} />
						</div>
					</Col>
				</Row>
			</Container>
		</div>
	</div>
</section>

<Footer />
