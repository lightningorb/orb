<!-- Contact Component -->
<script>
  import { Col, Row, Container, FormGroup, Input } from "sveltestrap";
</script>

<!-- CONTACT FORM START-->
<section class="section common-section" id="contact">
  <Container>
    <Row>
      <Col lg={{ size: 8, offset: 2 }}>
        <h1 class="section-title text-center">Get In Touch</h1>
        <div class="section-title-border mt-3" />
        <p class="section-subtitle text-muted text-center font-secondary pt-4">
          We thrive when coming up with innovative ideas but also understand
          that a smart concept should be supported with faucibus sapien odio
          measurable results.
        </p>
      </Col>
    </Row>
    <Row>
      <Col lg="4">
        <div class="mt-4 pt-4">
          <p class="mt-4">
            <span class="h5">Office Address 1:</span><br />
            <span class="text-muted d-block mt-2"
              >4461 Cedar Street Moro, AR 72368</span
            >
          </p>
          <p class="mt-4">
            <span class="h5">Office Address 2:</span><br />
            <span class="text-muted d-block mt-2"
              >2467 Swick Hill Street <br />New Orleans, LA 70171</span
            >
          </p>
          <p class="mt-4">
            <span class="h5">Working Hours:</span><br />
            <span class="text-muted d-block mt-2">9:00AM To 6:00PM</span>
          </p>
        </div>
      </Col>
      <Col lg="8">
        <div class="custom-form mt-4 pt-4">
          <form method="post" name="myForm" onsubmit="return validateForm()">
            <p id="error-msg" />
            <div id="simple-msg" />
            <Row>
              <Col lg="6">
                <FormGroup class="mt-2">
                  <Input
                    name="name"
                    id="name"
                    type="text"
                    class="form-control"
                    placeholder="Your name*"
                  />
                </FormGroup>
              </Col>
              <Col lg="6">
                <FormGroup class="mt-2">
                  <Input
                    name="email"
                    id="email"
                    type="email"
                    class="form-control"
                    placeholder="Your email*"
                  />
                </FormGroup>
              </Col>
            </Row>
            <Row>
              <Col lg="12">
                <FormGroup class="mt-2">
                  <Input
                    type="text"
                    class="form-control"
                    id="subject"
                    name="subject"
                    placeholder="Your Subject.."
                  />
                </FormGroup>
              </Col>
            </Row>
            <Row>
              <Col lg="12">
                <FormGroup class="mt-2">
                  <Input
                    type="textarea"
                    name="comments"
                    id="comments"
                    rows="4"
                    class="form-control"
                    placeholder="Your message..."
                  />
                </FormGroup>
              </Col>
            </Row>
            <Row>
              <Col lg="12" class="text-end">
                <Input
                  type="submit"
                  id="submit"
                  name="send"
                  class="submitBnt btn btn-primary"
                  value="Send Message"
                />
              </Col>
            </Row>
          </form>
        </div>
      </Col>
    </Row>
  </Container>
</section>
<!-- CONTACT FORM END-->
