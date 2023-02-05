<!-- Blog Component -->
<script>
	import { Col, Row, Container } from 'sveltestrap';

	export let blogData = {};
	const { title, description, blog_list } = blogData;
</script> 

<section class="section bg-light pt-5 common-section" id="blog">
	<Container>
		<Row>
			<Col lg={{ size: 8, offset: 2 }}>
				<h1 class="section-title text-center">{title}</h1>
				<div class="section-title-border mt-3" />
				<p class="section-subtitle text-muted text-center font-secondary pt-4">
					{description}
				</p>
			</Col>
		</Row>

		<Row class="mt-4">
			{#each blog_list as list}
				<Col lg="4">
					<div class="blog-box mt-4 hover-effect">
						<img src={list.image} class="img-fluid" alt="" />
						<div>
							<h5 class="mt-4 text-muted">{list.text}</h5>
							<h4 class="mt-3">
								<a href={'#'} class="blog-title"> {list.title} </a>
							</h4>
							<p class="text-muted">{list.subtext}</p>
							<div class="mt-3">
								<a href={'#'} class="read-btn">Read More <i class="mdi mdi-arrow-right" /></a>
							</div>
						</div>
					</div>
				</Col>
			{/each}
		</Row>
	</Container>
</section>
<!-- END BLOG -->
