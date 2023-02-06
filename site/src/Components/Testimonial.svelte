<!-- Testimonial component -->
<script>
	import { Col, Row, Container } from 'sveltestrap';

	export let testimonialData = {};
	const { title, description, testimonial_list } = testimonialData;

	export let startedData = {};
	const { newtitle, newtext, newbuttontext } = startedData;
</script>

<!--START TESTIMONIAL-->

<section class="section" id="testi">
	<Container>
		<Row>
			<Col lg={{ size: 8, offset: 2 }}>
				<h1 class="section-title text-center">{title}</h1>
				<!-- 				<div class="section-title-border mt-3" />
				<p class="section-subtitle text-muted text-center font-secondary pt-4">
					{description}
				</p> -->
			</Col>
		</Row>
		<Row class="mt-5">
			{#each testimonial_list as list}
				<Col lg={4}>
					<div class="testimonial-box mt-4">
						<div class="testimonial-decs p-4">
							<div class="testi-icon">
								<i class="mdi mdi-format-quote-open display-1" />
							</div>
							<!-- 							<img
								src={list.profile}
								alt=""
								class="img-fluid mx-auto d-block img-thumbnail rounded-circle mb-4"
							/> -->
							<div class="p-1">
								<a href={list.url}
									><h5 class="text-center text-uppercase mb-3">
										{list.name}
										<!-- <span class="text-muted text-capitalize">{list.text}</span> -->
									</h5></a
								>
								<p class="text-muted text-center mb-0">“{list.description}”</p>
							</div>
						</div>
					</div>
				</Col>
			{/each}
		</Row>
	</Container>
</section>
<!--END TESTIMONIAL-->

<!-- 
<section class="section section-lg bg-get-start">
    <div class="bg-overlay"></div>
    <Container>
        <Row>
            <Col lg={{size:8, offset: 2}} class="text-center">
                <h1 class="get-started-title text-white">{newtitle}</h1>
                <div class="section-title-border mt-4 bg-white"></div>
                <p class="section-subtitle font-secondary text-white text-center pt-4">{newtext}</p>
                <a href={"#"} class="btn btn-white waves-effect mt-4">{newbuttontext} <i class="mdi mdi-arrow-right"></i>
                </a>
            </Col>
        </Row>
    </Container>
</section>
 -->
