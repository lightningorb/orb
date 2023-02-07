<script>
	import { Col, Row, Container } from 'sveltestrap';
</script>

<section class="section common-section" id="features">
	<Container>
		<Row class="align-items-center">
			<Col lg={2} class="order-2 order-lg-1">
				<div class="features-img mt-5 mt-lg-0">
					<img
						src="https://lnorb.s3.us-east-2.amazonaws.com/docs/orb_ipad.png"
						alt="macbook_image"
						class="img-fluid"
					/>
				</div>
			</Col>
			<Col lg={10} class="order-1 order-lg-2">
				<div class="features-box mx-auto me-lg-0">
					<h3>Orb makes lightning fun</h3>

					<p class="text-muted web-desc">
						Orb runs on your phone, and supports multi-touch gestures.
					</p>

					<p class="text-muted web-desc">
						Take your node wherever you go, and swipe channels to rebalance. Orb puts the power of a
						full Lightning Network node in the palms of your hands in a beautiful, portable and fun
						interface.
					</p>
				</div>
			</Col>
		</Row>
		<br />
		<br />
		<br />
		<Row class="align-items-center">
			<Col lg={9} class="order-2 order-lg-1">
				<div class="features-box mt-5 mt-lg-0">
					<h3>Orb is secure.</h3>

					<p class="text-muted web-desc">
						Convenience should never come at the cost of security. Orb runs on your end-user
						device–not on your node–and encrypts the certificate & macaroon with a unique personal
						RSA encryption key-set tied to your device.
					</p>
				</div>
			</Col>
			<Col lg={3} class="order-1 order-lg-2">
				<div class="features-img mx-auto me-lg-0">
					<img
						src="https://upload.wikimedia.org/wikipedia/commons/3/3b/RSA_logo_2008-to_present.jpg"
						alt="macbook_image"
						class="img-fluid"
					/>
				</div>
			</Col>
		</Row>
		<br />
		<br />
		<br />
		<Row class="align-items-center">
			<Col lg={2} class="order-2 order-lg-1">
				<div class="features-img mt-5 mt-lg-0">
					<img
						src="https://s3-us-east-2.amazonaws.com/lnorb/docs/Finding_Balance_Part_2_Examining_the_Shortcomings_of_Typical_Engine_Balancing_Techniques_-_OnAllCylinders_2022-01-31_10-05-19.p_2022-01-31_10-06-00.jpg"
						alt="macbook_image"
						class="img-fluid"
					/>
				</div>
			</Col>
			<Col lg={10} class="order-1 order-lg-2">
				<div class="features-box mx-auto me-lg-0">
					<h3>Orb automates your node.</h3>

					<p class="text-muted web-desc">
						Setting fees and balancing a node by hand is time consuming. Orb provides automated
						fee-setting and rebalancing engines.
					</p>
				</div>
			</Col>
		</Row>
		<br />
		<br />
		<br />
		<Row class="align-items-center">
			<Col lg={9} class="order-2 order-lg-1">
				<div class="features-box mt-5 mt-lg-0">
					<h3>Apps.</h3>

					<p class="text-muted web-desc">
						The Lightning Network is constantly evolving and growing; so should its tools. Orb’s API
						enables you to ‘scratch your own itch’, and the app store enables you to deploy tools
						securely and rapily.
					</p>
				</div>
			</Col>
			<Col lg={3} class="order-1 order-lg-2">
				<div class="features-img mx-auto me-lg-0">
					<img
						src="https://s3-us-east-2.amazonaws.com/lnorb/docs/Cross-Platform_Must_Have_Apps_For_The_College_Student_2022-01-31_10-11-48.png"
						alt="macbook_image"
						class="img-fluid"
					/>
				</div>
			</Col>
		</Row>
		<br />
		<br />
		<br />
		<Row class="align-items-center">
			<Col lg={2} class="order-2 order-lg-1">
				<div class="features-img mt-5 mt-lg-0">
					<img
						src="https://s3-us-east-2.amazonaws.com/lnorb/docs/Data_science_concepts_you_need_to_know_Part_1__by_Michael_Barber__Towards_Data_Science_2022-01-31_10-15-17.jpg"
						alt="macbook_image"
						class="img-fluid"
					/>
				</div>
			</Col>
			<Col lg={10} class="order-1 order-lg-2">
				<div class="features-box mx-auto me-lg-0">
					<h3>Data Science.</h3>

					<p class="text-muted web-desc">
						Orb caches transactions and payments locally, and provides you with the information you
						actually want, such as how much channels are earning, their fee profiles etc. it also
						exposes this data conveniently to libraries like Numpy, Pandas, TensorFlow etc. The
						Lightning Network should be data-driven. Orb makes this goal easy to attain.
					</p>
				</div>
			</Col>
		</Row>
		<br />
		<br />
		<br />
	</Container>
</section>
