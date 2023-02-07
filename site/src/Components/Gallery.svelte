<script>
	import { Col, Row, Container } from 'sveltestrap';
	import { Image } from 'sveltestrap';
	import Fullscreen from 'svelte-fullscreen';

	export let galleryData = {};
	const { heading, description, gallery_list } = galleryData;
</script>

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
			{#each gallery_list as list}
				<div class="col-lg-4 mt-4 text-center">
					<a href={list.text} target="_blank">
						<Image draggable={false} thumbnail alt={list.label} src={list.thumbnail} />
					</a>
				</div>
			{/each}
		</div>
	</Container>
</section>
