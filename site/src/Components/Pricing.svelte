<!-- pricing component -->
<script>
	import { Col, Row, Container } from 'sveltestrap';

	export let pricingData = {};
	const { title, description, pricing_list } = pricingData;
</script>

<!--START PRICING-->
<section class="section bg-light common-section" id="pricing">
	<Container>
		<Row>
			<Col lg={{ size: 8, offset: 2 }}>
				<h1 class="section-title text-center">{title}</h1>
				<div class="section-title-border mt-3" />
				<p class="section-subtitle font-secondary text-muted text-center pt-4">
					{description}
				</p>
			</Col>
		</Row>
		<div class="row mt-5">
			{#each pricing_list as list}
				<div class="col-lg-4">
					<div class="text-center pricing-box">
						<h4 class="text-uppercase">{list.title}</h4>
						<h1>{list.price}</h1>
						<h6 class="text-uppercase text-muted">{list.duration}</h6>
						<div class="plan-features mt-5">
							<p class='m-0 p-0'>Mobile: <b class="text-primary">{list.mobile}</b></p>
							<p class='m-0 p-0'>Desktop: <b class="text-primary">{list.desktop}</b></p>
							<p class='m-0 p-0'>Auto Rebalancing: <b class="text-primary">{list.auto_rebalancing}</b></p>
							<p class='m-0 p-0'>Auto Fees: <b class="text-primary">{list.auto_fees}</b></p>
							<p class='m-0 p-0'>Peer Recommendations: <b class="text-primary">{list.peer_recommendations}</b></p>
							<p class='m-0 p-0'>Bulk Payments: <b class="text-primary">{list.bulk_payments}</b></p>
							<p class='m-0 p-0'>Fee Profiles: <b class="text-primary">{list.fee_profiles}</b></p>
							<p class='m-0 p-0'>App Store Access: <b class="text-primary">{list.app_store}</b></p>
							<p class='m-0 p-0'>Script Editor: <b class="text-primary">{list.script_editor}</b></p>
							<p class='m-0 p-0'>Ads: <b class="text-primary">{list.ads}</b></p>
						</div>
						{#if list.eval_action != undefined}
							<a href={list.eval_url} class="btn btn-primary waves-effect waves-light mt-5" style='color: white !important; ' >{list.eval_action}</a>
							{/if}
						{#if !list.disabled}
							<a href={list.url} class="btn btn-primary waves-effect waves-light mt-5" style='color: white !important; ' >{list.action}</a>
						{/if}
						{#if list.disabled}
							<p class="btn btn-primary waves-effect waves-light mt-5" style='color: white !important; ' >{list.action}</p>
						{/if}
					</div>
				</div>
			{/each}
		</div>
	</Container>
</section>
<!--ENd PRICING-->
