<script>
	import Footer from '../../Components/Footer.svelte';
	import NavbarPlain from '../../Components/NavbarPlain.svelte';
	import { Styles, Modal, ModalBody, ModalHeader, Container, Row, Col } from 'sveltestrap';
	import SvelteMarkdown from 'svelte-markdown';

	const source = `


v0.21.13
========

Better docker support. Documentation.

v0.21.12
========

Stability & bug fixes. Documentation.

Better docker support.

v0.21.11
=======

Stability & bug fixes. Documentation.

v0.21.10
=======

Stability & bug fixes. Documentation.

v0.21.9
=======

UNSTABLE RELEASE. Feel free to download, read the docs, run the tests etc. but strongly recommend to use in read only mode for now, i.e do not open channels, make payments, rebalance etc. until patches have been released bringing Orb into stable mode again.

Release notes:

- Documentation.
- Circular rebalances now working in CLN.


v0.21.8
=======

UNSTABLE RELEASE. Feel free to download, read the docs, run the tests etc. but strongly recommend to use in read only mode for now, i.e do not open channels, make payments, rebalance etc. until patches have been released bringing Orb into stable mode again.

Release notes:

- Documentation.
- Fixed a crash in console editor when in Orb Connect App.
- Downgraded linux build to python 3.8.
- Added 'orb network get-route' CLI command.
- Attributes all showing again in the Attributes Editor.


v0.21.7
=======

UNSTABLE RELEASE. Feel free to download, read the docs, run the tests etc. but strongly recommend to use in read only mode for now, i.e do not open channels, make payments, rebalance etc. until patches have been released bringing Orb into stable mode again.

Release notes:

- Documentation.
- Orb CLN now gets the payment history.
- Orb CLN now displays spent / earned in UI.
- LNURL Pay now has a UI HUD.


v0.21.6
=======

UNSTABLE RELEASE. Feel free to download, read the docs, run the tests etc. but strongly recommend to use in read only mode for now, i.e do not open channels, make payments, rebalance etc. until patches have been released bringing Orb into stable mode again.

Release notes:

- Can now show on-chain funds with CLI
- Can now send all on-chain funds using CLI


v0.21.5
=======

UNSTABLE RELEASE. Feel free to download, read the docs, run the tests etc. but strongly recommend to use in read only mode for now, i.e do not open channels, make payments, rebalance etc. until patches have been released bringing Orb into stable mode again.

Release notes:

- Can now get fetch events for both LND and CLN (will not work on CLN until c-lightning-REST pull-request)
- Added orb channel list-forwards CLI command.
- Added a dockerfile to the docs.


v0.21.4
=======

UNSTABLE RELEASE. Feel free to download, read the docs, run the tests etc. but strongly recommend to use in read only mode for now, i.e do not open channels, make payments, rebalance etc. until patches have been released bringing Orb into stable mode again.

Release notes:

- Added a web interface (orb web serve --help).


v0.21.3
=======

UNSTABLE RELEASE. Feel free to download, read the docs, run the tests etc. but strongly recommend to use in read only mode for now, i.e do not open channels, make payments, rebalance etc. until patches have been released bringing Orb into stable mode again.

Release notes:

- Terminal coloring should now work in Windows.

v0.21.2
=======

UNSTABLE RELEASE. Feel free to download, read the docs, run the tests etc. but strongly recommend to use in read only mode for now, i.e do not open channels, make payments, rebalance etc. until patches have been released bringing Orb into stable mode again.

Release notes:

- Fixed currency converter app to work with Kivy 2.1.0.
- Moved CLI to Typer.

v0.21.1
=======

UNSTABLE RELEASE. Feel free to download, read the docs, run the tests etc. but strongly recommend to use in read only mode for now, i.e do not open channels, make payments, rebalance etc. until patches have been released bringing Orb into stable mode again.

Release notes:

- Tests can now be run from the main binary with <binary> test.run-all-tests

v0.21.0
=======

UNSTABLE RELEASE. Feel free to download, read the docs, run the tests etc. but strongly recommend to use in read only mode for now, i.e do not open channels, make payments, rebalance etc. until patches have been released bringing Orb into stable mode again.

The reason for this early (and unstable) release is that it put release testing pipeline in place.

Release notes:

- CLN (Core Lightning) support added.
- CLI (Command Line Interface) support added.


v0.20.2
=======

lnurl payments now work on Android.

v0.20.1
=======

Fixed an IOS crash due to the order of ui build being somewhat different to other platforms.


v0.20.0
=======

This is the most stable Orb release to date.

Memory leaks and async database connection issues were resolved in patches to v0.19.0.

Upgraded from kivy 2.0.0 to kivy 2.1.0. The upgrade revealed UI modifications being made on threads, which have now been moved to the main thread. This should help resolve visual artefacts and stability issues.

In REST mode the attribute editor was pulling in stale data. This should now be fixed, so liquidity should be properly displayed in the attribute editor after e.g rebalances.

When channels were receiving liquidity, there wasn't any proper logic to account for that, and instead Orb was relying on channel updates. Logic has now been put in place by listening to paid invoices. This does not cover every scenario (e.g keysends).

In REST mode, channels were the incorrect type (no event-dispatchers), and thus the rest of the app was not reacting to attribute changes as it does in GRPC mode. This is now fixed.

The 'Connector' app (the screens that help you connect to your node) and the main app are now launched in their own right, and the user no longer has the ability to go from one to the other. In practice this means when the user wants to connect to a node, they need to restart the app. Going from one app to another was not supported by Kivy, so the UX-level segregation is best practice and likely improves stability (some weakref crashes may have been related).

Deezy swap dialog was not working due to non-portable typing issues. This is now fixed.

Node rankings has been fixed (crashed due to db-related fixes in v0.19.0). Rebalancing gestures are now fixed after a bug was introduced with time_pref.


v0.19.3
=======

Memory leaks & database locking issues should now be fixed.

v0.19.2
=======

Fixed a typo in conf_defaults.

v0.19.1
=======

LNURL and Deezy.io dialogs now only generate the invoices, rather than carrying the payments.

v0.19.0
=======

Added on-chain swap service deezy.io

v0.18.0
=======

LNURL invoice payments now supported: Lightning > Pay > Pay LNURL.

Auto Update Max HTLC Msat app now has more policies and options.

Fixed an issue that broke aufo-fees on android.

Fee Widget now appears blue when max_htlc_msat < 1000 (this will likely change in a future release).

Channels should grey out / return correctly when they go inactive / active.

Channels can now also be sorted by alias.

v0.17.1
=======

Resolved a padding issue with the certificate in lnurlconnect decoding.

v0.17.0
=======

Added correct GRPC modules and explicit support for lnd 0.14.0, 0.14.1, 0.14.2, 0.14.3, 0.15.0.

Added ability to specify time_pref for path building, to specify whether cheap or expensive routes should be tried first.

Fixed an issue that broke the Ubuntu build. Improved ubuntu bootstrap script.

Auto-fees dialog has better support for mobile.

Better support when rotating device: the Orb replaces itself in the center after rotation.

Channels should grey out / return correctly when they go inactive / active.

v0.16.2
=======

Resolved an issue where the 'shift' key was sticky in the console input.

The 'close channel' dialog now force closes channels correctly over REST.

HTLC attempts and failure flashes now use bright colors in the UI.

v0.16.1
=======

Menus work better on mobile devices with small screens / resolutions.

Fixed an issue that broke the Ubuntu build. Improved ubuntu bootstrap script.

v0.16.0
========

Now builds and runs in Android >= 8.

When the app starts, the user is now presented with screens to help connect to nodes.

Face-lift of all dialogs, for better mobile experience.

'Ingest invoices' dialog now automatically pastes lightning invoices from clipboard.

'Lighting > Channels > Sort > ...' now changes channels sorting live.

Solved an issue where payment were still going through ignored channels.

v0.15.2
========

Added ability to export / import connection settings to / from other devices.


v0.15.1
========

Removed functionality and libraries that are problematic for the IOS App Store review. The Desktop version of Orb is unaffected by this release.

v0.15.0
========

This release makes it easier connecting Orb to your node.

Orb > Umbrel Node
-----------------

One click solution to connect to Umbrel and nodes supporting lndconnect URL.

Orb > Voltage Node
------------------

Fill out 3 fields to connect Orb to a Voltage node.

Orb > SSH Connection Wizard
---------------------------

This dialog enables Orb to SSH into your node, detect the setup (bare versus Docker), detect whether it is a mainnet / testnet / signet node, detect locations of important files, and copy encrypted TLS certificate and Macaroon.

Bug Fixes
---------

- Threads now properly capture output into the script editor's output section.

v0.14.13
========

Fixed a race condition sometimes leading to the Mock node being loaded instead of the real one.

v0.14.12
========

Fixed regression of 'plyer.platforms' module missing in windows.

v0.14.11
========

Increased canvas size to accommodate large nodes (comfortably up to 350 channels).

v0.14.10
========

Changed system's default desktop unique identifier library from uuid to plyer, as such, existing users need to either:

- go to Orb > Settings
- at the bottom, under 'system', change 'Device Identifier' from 'plyer' back to 'uuid'

or regenerate their TLS & Macaroon connection strings.

Fixed the 'about' dialog.

'Help > Release Notes' now points to the site.

Orb is now aware of its version, and displays it in the terminal, in the about dialog, and in orb.ini


v0.14.9
=======

Fixed the Umbrel connection string as it pointed to umbrel/.lnd instead of umbrel/lnd.

Fixed autofees to explicite set PPM as an integer instead of floating point, and reduced the number of calls to LND.

Orb can now launch even if unable to connect to the node.


v0.14.8
=======

Resolved an issue where the GUI locks up during bulk payments or rebalances.

v0.14.7
=======

Resolved an issue where bulk payment threads would stop early due to non-ascii characters in aliases.

v0.14.6
=======

Added an option in 'Connection Settings' for Umbrel users.

v0.14.5
=======

The Channel Editor now displays the Alias and Public Key of the peer (as opposed to our own).

Resolved issue with app store login being inconsistent when switching between REST and GRPC.

The Audio wave files are now properly bundled into the builds.

v0.14.4
=======

Fixing builds for all targets.

Better Linux installation documentation.

Added missing modules to Linux bootstrap script.

Added launch debug messages.

Start orb in Console (rather than Windowed) mode. This is to help with launch debugging.

Resolved [critial error] infinite rendering loop when opening the connection settings dialog.

v0.14.3
=======

Now providing macos 10.15 build.

Removed max budget field from auto-rebalancer.

v0.14.2
=======

Renamed 'Aim for Ratio' to 'Balanced Ratio' in Attributes Editor.

Fixed issue of being unable to exit the script editor in the free version.

Now shows ad banner in both the trial and free versions.

Disabled publishing apps to the app-store until review mechanism is put in place.

Updated privacy policy.

v0.14.1
=======

Licensing 'call home' will now quit Orb if the pubkey has been using an evaluation license for over 30 days.

Resolved an issue where zombie threads were occurring during bulk payments and bulk rebalances. The issue was resolved from no longer using a lock, and using a consumable queue.

Autobalance, autofees, and update max HTLCs apps now properly clean up their previous invocation when loaded through the apps menu.

Better handling of sys.path from settings.

v0.14.0
=======

In the attributes editor, can now clear the balanced ratio.

Improved output when closing a channel over REST.

Split up functionality based on edition.

v0.13.1
=======

Adverts now only count views / time when the user is actively using the app. i.e when Orb sits idle, those views are not counted.

Brought back rankings, which had been temporarily removed due to ongoing work with storing payments in the local db.

Batch opens were not working on REST (previous, it only worked over GRPC).

On mobile, in the console output section, disabled the ability to select text, as it brings up the keyboard, preventing the ability to scroll.
`;
</script>

<NavbarPlain extraclass="" />

<section class="section common-section text-black" id="priv">
	<div class="display-table">
		<div class="display-table-cell">
			<Container>
				<Row>
					<Col lg={{ size: 8, offset: 2 }}>
						<h1 class="home-title">Release Notes</h1>
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

<Styles/>

<Footer />
