<script>
	import NavbarPlain from '../../Components/NavbarPlain.svelte';
	import { Modal, ModalBody, ModalHeader, Container, Row, Col, Styles } from 'sveltestrap';
</script>

<Styles />

<NavbarPlain extraclass="" />

<section class="section vh-100 common-section text-black" id="priv">
	<div class="display-table">
		<div class="display-table-cell">
			<Container>
				<Row class="justify-content-center">
					<Col lg={8} class="text-center">
						<h1 class="home-title">Privacy Policy</h1>
						<h4 class="home-small-title">We literally don't know who you are.</h4>
						<p class="pt-3 text-black mx-auto">
							Our approach to handling privacy is to not store any customer information at all by
							default.
						</p>
						<h4 class="home-small-title">Cookies.</h4>
						<p class="pt-3 text-black mx-auto">
							We do not store cookies in your browser. This serves the dual purpose of ensuring your
							privacy and not having to display invasive cookie banners.
						</p>
						<h4 class="home-small-title">KYC.</h4>
						<p class="pt-3 text-black mx-auto">
							We are neither a financial company, nor a banking company. As such we have no
							requirements to keep any information about you. Hence, we don't.
						</p>
						<h4 class="home-small-title">IP Addresses.</h4>
						<p class="pt-3 text-black mx-auto">
							We do not track or store IP addresses. They do appear in our nginx and backend log
							files, but those are culled after some time, and we do not back them up. We do not
							store your IP address in any internal databases. Amazon S3 may also keep copies of
							your IP address for some time, but not in a way that is tied to you.
						</p>
						<h4 class="home-small-title">Node Pubkeys.</h4>
						<p class="pt-3 text-black mx-auto">
							Your node pubkey is currently being used to log in to the app store. We also plan on
							implementing a 'delete me' functionality, to enable you to delete your pubkey from our
							app-store authentication database.
						</p>
						<h4 class="home-small-title">Ads.</h4>
						<p class="pt-3 text-black mx-auto">
							We display ads in the free and trial versions of the Orb. These are ads that are
							relevant and curated to raise awareness about high quality products and services
							relating to the Lightning Network. We currently do not share any user information with
							advertisers, e.g advertisers do not have access to the public keys of users who saw
							their ads, or clicked on them. If this changes in the future, it will not be without
							first having a discussion with our users, and if deemed acceptable we'll update our
							terms and services, and include the change in our release notes and announcement areas
							on the site.
						</p>
						<h4 class="home-small-title">Your fidelity matters to us most.</h4>
						<p class="pt-3 text-black mx-auto">
							For Orb to succeed as a business, we need to foster customer fidelity. Our goal is to
							provide you with the highest quality software possible, not to partake in data
							brokerage activities. Your needs for privacy are in line with our incentives to make
							you happy, and converting you to a repeat customer for years to come. As such we have
							every reason to fight for your privacy needs and privacy rights.
						</p>
					</Col>
				</Row>
			</Container>
		</div>
	</div>
</section>
