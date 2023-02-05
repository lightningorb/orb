<!-- signup component -->
<script>
	import { Link } from 'svelte-routing';
	import { Form, Input, Label, Container, Row, Col, Button, FormGroup } from 'sveltestrap';
</script>

<div class="account-home-btn d-none d-sm-block">
	<a href="/" class="text-white"><i class="mdi mdi-home h1" /></a>
</div>

<section class="vh-100">
	<div class="display-table">
		<div class="display-table-cell">
			<Container>
				<Row class="justify-content-center">
					<Col lg={5}>
						<div class="card account-card">
							<div class="card-body">
								<div class="text-center mt-3">
									<h3 class="fw-bold">
										<Link to="/" class="text-dark text-uppercase account-pages-logo"
											><i class="mdi mdi-alien" />Hiric</Link
										>
									</h3>
									<p class="text-muted">Sign up for a new Account</p>
								</div>
								<div class="p-4">
									<Form>
										<FormGroup>
											<Label for="firstname">First Name</Label>
											<Input
												type="text"
												class="form-control"
												id="firstname"
												placeholder="First Name"
											/>
										</FormGroup>

										<FormGroup>
											<Label for="email">Email</Label>
											<Input
												type="password"
												class="form-control"
												id="email"
												placeholder="Enter Email"
											/>
										</FormGroup>

										<FormGroup>
											<Label for="userpassword">Password</Label>
											<Input
												type="password"
												class="form-control"
												id="userpassword"
												placeholder="Enter password"
											/>
										</FormGroup>

										<div class="form-check">
											<Input
												class="form-check-input"
												type="checkbox"
												value=""
												id="flexCheckDefault"
											/>
											<Label class="form-check-label" for="flexCheckDefault">Remember me</Label>
										</div>

										<div class="d-grid mt-3">
											<Button type="submit" color="primary">Sign in</Button>
										</div>

										<div class="mt-4 mb-0 text-center">
											<p class="mb-0">
												Don't have an account ? <a href="login" class="text-danger">Sign in</a>
											</p>
										</div>
									</Form>
								</div>
							</div>
						</div>
						<!-- end card -->
					</Col>
					<!-- end col -->
				</Row>
				<!-- end row -->
			</Container>
		</div>
	</div>
</section>
