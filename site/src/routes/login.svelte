<!-- Login component -->
<script>
	import { Link } from 'svelte-routing';
  import { Form, Input, Label, Container, Row, Col, Button, FormGroup } from 'sveltestrap';
</script>

<div class="account-home-btn d-none d-sm-block">
	<Link to="/" class="text-white"><i class="mdi mdi-home h1" /></Link>
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
											><i class="mdi mdi-alien" />Hiric</Link>
									</h3>
									<p class="text-muted">Sign in to continue to Hiric.</p>
								</div>
								<div class="p-4">
									<Form>
										<FormGroup>
											<Label for="username">Username</Label>
											<Input
												type="text"
												class="form-control"
												id="username"
												placeholder="Enter username"
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
											<Label class="form-check-label" for="flexCheckDefault"> Remember me </Label>
										</div>

										<div class="d-grid mt-3">
											<Button type="submit" color="primary">Log In</Button>
										</div>

										<div class="mt-4 mb-0 text-center">
											<Link to="/password_forget" class="text-dark"
												><i class="mdi mdi-lock" /> Forgot your password?
                        </Link>
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
