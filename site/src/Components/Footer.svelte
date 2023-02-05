<!-- Footer Component -->
<script>
	import { Col, Row, Container } from 'sveltestrap';
</script>

<style type="text/css">
.link-unstyled, .link-unstyled:link, .link-unstyled:hover {
  color: red !important;
  text-decoration: inherit  !important;
}
</style>

<!--START FOOTER-->
<footer class="footer">
	<Container>
		<Row>
			<Col lg="3" class="mt-4">
				<h4>ORB</h4>
				<div class="text-muted mt-4">
					<ul class="list-unstyled footer-list">
						<li><a href={'/docs'}>Documentation</a></li>
						<li><a href={'/release-notes'}>Release Notes</a></li>
						<li><a href={'https://t.me/+8UbTaTxtHvcxYTZl'}>User Group</a></li>
					</ul>
				</div>
			</Col>
			<Col lg="3" class="mt-4">
				<h4>Information</h4>
				<div class="text-muted mt-4">
					<ul class="list-unstyled footer-list">
						<li><a href={'/privacy'}>Privacy Policy</a></li>
						<li><a href={'/terms-and-conditions'}>Terms and Conditions</a></li>
						<li><a href={'/security'}>Security</a></li>
					</ul>
				</div>
			</Col>
		</Row>
	</Container>
</footer>
<!--END FOOTER-->

<!--START FOOTER ALTER-->
<div class="footer-alt">
	<Container>
		<Row>
			<Col lg="12">
				<div class="float-start pull-none ">
					<p class="copy-rights text-muted mb-3 mb-sm-0">
						{new Date().getFullYear()}
						© lnorb.com - made with <a href='/love'>♥</a>
					</p>
				</div>
<!-- 				<div class="float-end pull-none ">
					<ul class="list-inline social m-0">
						<li class="list-inline-item">
							<a href={"#"} class="social-icon"><i class="mdi mdi-facebook" /></a>
						</li>
						<li class="list-inline-item">
							<a href={"#"} class="social-icon"><i class="mdi mdi-twitter" /></a>
						</li>
						<li class="list-inline-item">
							<a href={"#"} class="social-icon"><i class="mdi mdi-linkedin" /></a>
						</li>
						<li class="list-inline-item">
							<a href={"#"} class="social-icon"><i class="mdi mdi-google-plus" /></a>
						</li>
						<li class="list-inline-item">
							<a href={"#"} class="social-icon"><i class="mdi mdi-dribbble" /></a>
						</li>
					</ul>
				</div> -->
				<div class="clearfix" />
			</Col>
		</Row>
	</Container>
</div>
<!--START FOOTER ALTER-->
