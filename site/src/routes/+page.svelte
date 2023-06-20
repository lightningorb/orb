<script>
	import Gallery from '../Components/Gallery.svelte';
	import Testimonial from './../Components/Testimonial.svelte';
	import Services from '../Components/Services.svelte';
	import AboutUs from '../Components/AboutUs.svelte';
	import Footer from '../Components/Footer.svelte';
	import Download from './../Components/Download.svelte';
	import Navbar from '../Components/Navbar.svelte';
	import Course from '../Components/Course.svelte';
	import { Styles } from 'sveltestrap';
	import { Modal, ModalBody, ModalHeader, Container, Row, Col } from 'sveltestrap';
	import { Button } from 'sveltestrap';
	import { Card, CardBody } from 'sveltestrap';
	import data from '../Data/data';
</script>

<Styles />
<Navbar extraclass="" />
<section class="section bg-home vh-100 common-section" id="home">
	<div class="bg-overlay" />
	<div class="display-table">
		<div class="display-table-cell">
			<Container>
				<Row class="justify-content-center">
					<Col lg={8} class="text-white text-center">
						<h1 class="home-title">Orb [beta]</h1>
						<h4 class="home-small-title">The lightning network just got way more fun.</h4>
						<Card body color="secondary" class="mb-3">curl https://install.lnorb.com | bash</Card>
						<p class="pt-3 home-desc mx-auto">
							Orb is a cross-platform (Mac / Windows / OSX / IOS / Android) application for managing
							an LND / CLN Lightning node. It features bulk payments, an editor, API, App Store,
							node automation engines and a lot more.
						</p>
						<br />
						<a href="#download" class="py-5">
							<Button class="btn download-btn btn-rounded waves-effect waves-light">Download</Button
							>
						</a>
					</Col>
				</Row>
			</Container>
		</div>
	</div>
</section>

<Course />
<AboutUs />
<Services serviceData={data.SERVICE_DATA} websiteData={data.WEBSITE_DESCRIPTION} />
<Gallery galleryData={data.GALLERY_DATA} />
<Download />
<Testimonial testimonialData={data.TESATIMONIAL_DATA} />
<Footer />
