<!-- services component -->
<script>
	import { Col, Row, Container } from 'sveltestrap';

	export let serviceData = {};
	export let websiteData = {};
	const { heading, description, services_list } = serviceData;
	const { title, buttontext, text } = websiteData;
  const services_list_length = services_list.length;
  {services_list_length}
</script>

<!--START SERVICES-->
<section class="section bg-light common-section" id="services">
	<Container>
		<Row>
			<Col lg={{ size: 8, offset: 2 }}>
				<h1 class="section-title text-center">{heading}</h1>
				<div class="section-title-border mt-3" />
				<p class="section-subtitle text-muted text-center pt-4 font-secondary">
					{description}
				</p>
			</Col>
		</Row>
		<div class="row mt-5">
      {#each services_list as list}

			<div class="col-lg-4 mt-4">
				<div class="services-box">
					<div class="d-flex">
						<i class="{list.icon} text-primary" />
						<div class="ms-4">
							<h4>{list.label}</h4>
							<p class="pt-2 text-muted">
								{list.text}
							</p>
						</div>
					</div>
				</div>
			</div>
      
      {/each}
		</div>
	</Container>
</section>
<!--START SERVICES-->