<!-- Password-forget component -->
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
											><i class="mdi mdi-alien" />Hiric</Link
										>
									</h3>
									<p class="text-muted">Reset Password</p>
								</div>
								<div class="p-4">
									<div class="alert alert-warning  text-center" role="alert">
										Enter your email address and we'll send you an email with instructions to reset
										your password.
									</div>
									<Form>
										<FormGroup>
											<Label for="email">Email</Label>
											<Input
												type="password"
												class="form-control"
												id="email"
												placeholder="Enter Email"
											/>
										</FormGroup>

										<div class="d-grid mt-3">
											<Button type="submit" color="primary">Reset your Password</Button>
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