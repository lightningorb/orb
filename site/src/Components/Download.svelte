<script>
	import { Modal, ModalBody, ModalHeader, Container, Row, Col } from 'sveltestrap';
	import { Card, CardBody, Button } from 'sveltestrap';
	import { FormGroup, Input, Label, Form } from 'sveltestrap';
	import { onMount } from 'svelte';
	import { Dropdown, DropdownItem, DropdownMenu, DropdownToggle } from 'sveltestrap';

	let is_ready = false;
	let radioGroup = '';
	let versions = null;
	$: latest = null;

	let host = 'https://lnorb.com';
	let url = 'https://lnorb.s3.us-east-2.amazonaws.com/customer_builds/';
	$: key =
		versions != null && radioGroup != ''
			? versions.builds[latest].filter((x) => x[0] == radioGroup)[0][1]
			: null;

	$: files = versions != null && latest != null ? versions.builds[latest] : [];
	$: dl_url = `${url}${files[radioGroup]}`;
	$: all_done = radioGroup !== '';
	$: os = files != null ? files.map((x) => x[0]) : [];

	async function dl_presigned_url() {
		let doc = {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({
				key: key
			})
		};
		const res = await fetch(`${host}/api/orb/versions/sign`, doc);
		const data = await res.json();
		if (data.url != null) {
			window.location.assign(data.url);
		}
	}
	async function get_versions() {
		const res = await fetch(`${host}/api/orb/versions/`, {
			method: 'GET'
		});
		const data = await res.json();
		if (data !== undefined && data.versions !== undefined) {
			versions = data;
			latest = versions.versions[0];
		}
	}
	onMount(() => {
		get_versions();
	});
</script>

<div>
	<section class="section bg-home vh-100 common-section" id="download">
		<div class="bg-overlay" />
		<div class="display-table">
			<div class="display-table-cell">
				<Container>
					<Row class="justify-content-center">
						<Col lg={12} class="text-white text-center">
							<h1 class="home-title">Download Orb</h1>
						</Col>
					</Row>
					<Row class="justify-content-center">
<!-- 						<Col lg={{ size: 3 }} class="text-white text-center">
							<a href="https://play.google.com/store/apps/details?id=com.lnorb.orb">
								<img
									style="width: 100px"
									src="https://lnorb.s3.us-east-2.amazonaws.com/images/android.png"
								/>
							</a>
						</Col> -->
						<Col lg={{ size: 3 }} class="text-white text-center">
							<a href="https://testflight.apple.com/join/i8wfm9TH">
								<img
									style="width: 50px;  position: relative; top: 8px;"
									src="https://lnorb.s3.us-east-2.amazonaws.com/images/testflight.png"
								/>
							</a>
							<p class="pt-3 home-desc mx-auto" />
						</Col>
					</Row>
					<br />
					<br />
					<Row class="justify-content-center">
						<Col lg={{ size: 3 }} class="text-white text-center">
							<p>We've moved the Android / Linux / Windows / OSX downloads to reproducible Github Releases:</p>
							<br />
							<a href="https://github.com/lightningorb/orb/releases">
								<img
									style="width: 200px;"
									src="https://github.githubassets.com/images/modules/logos_page/GitHub-Logo.png"
								/>
							</a>
							<p class="pt-3 home-desc mx-auto" />
						</Col>
					</Row>
					<br />
					{#if versions}
						<Row>
							<Col lg={{ size: 4, offset: 3 }}>
								<Form>
									<FormGroup>
										{#each os as o}
											<Input
												class="text-white"
												id={o}
												type="radio"
												bind:group={radioGroup}
												value={o}
												label={o}
											/>
										{/each}
									</FormGroup>
								</Form>
								<Dropdown>
									<DropdownToggle caret>{latest}</DropdownToggle>
									<DropdownMenu>
										<DropdownItem header>Versions</DropdownItem>
										{#each versions.versions as v}
											<DropdownItem on:click={() => (latest = v)}>{v}</DropdownItem>
										{/each}
									</DropdownMenu>
								</Dropdown>
							</Col>
							<Col lg={2} class="text-white text-center">
								<div class="nav-button ms-auto mx-auto text-center">
									<ul class="nav navbar-nav navbar-end">
										<li>
											{#if all_done}
												<Button
													class="btn btn-primary navbar-btn btn-rounded waves-effect waves-light"
													on:click={dl_presigned_url}>Download</Button
												>
											{:else}
												<Button
													disabled={true}
													class="btn btn-primary navbar-btn btn-rounded waves-effect waves-light"
													>Download</Button
												>
											{/if}
										</li>
									</ul>
								</div>
							</Col>
						</Row>
						<Row>
							<Col class="text-white mt-5" lg={{ size: 8, offset: 2 }}>
								<p>
									Once your download is complete, please read our <a
										href="https://lnorb.com/docs/installing.html">installation documentation</a
									>.
								</p>
							</Col>
						</Row>
					{/if}
				</Container>
			</div>
		</div>
	</section>
</div>
