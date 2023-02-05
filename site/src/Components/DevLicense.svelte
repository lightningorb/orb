<script>
    import { Modal, ModalBody, ModalHeader, Container, Row, Col } from 'sveltestrap';
    import { Card, CardBody, Button } from 'sveltestrap';
</script>

<div>
<section class="section bg-home vh-100 common-section" id="dev-license">
    <div class="bg-overlay" />
    <div class="display-table">
        <div class="display-table-cell">
            <Container>
                <Row class="justify-content-center">
                    <Col lg={8} class="text-white text-center">
                        <h1 class="pt-5 home-title">Dev License</h1>
                        <p class="pt-3 home-desc mx-auto">
                            The dev license grants developers a free copy of Orb, given that certain criteria are met. To attain a dev license, write to user <a target='_blank' href='https://t.me/lnorb'>@lnorb</a> on Telegram.
                        </p>
                        <p class="pt-3 home-desc mx-auto">
                            Include the following in your message: Link to Github (or equiv.) account.
                        </p>
                        <p class="pt-3 home-desc mx-auto">
                            Upon successful review, a developer license valid for 1 month is messaged back to you. The license can be used with a mainnet, signet and testnet node.
                        </p>
                    </Col>
                </Row>
            </Container>
        </div>
    </div>
</section>

<section class="section bg-light common-section" id="services">
    <Container>
        <Row>
            <Col lg={{ size: 8, offset: 2 }}>
                <h1 class="section-title text-center">Upon publishing your first app, you will be granted:</h1>
                <div class="section-title-border mt-3" />
                <p class="section-subtitle home-desc  text-center pt-4 font-secondary">
                    <Card style='background: #6755ffbb;'>
                      <CardBody style='color: #ffffff'>An extended developer license for 1 year. <br/>
                        Ability to convert your app to a paid app.</CardBody>
                    </Card>
                </p>
                <br/>
                <br/>
                <div class="nav-button ms-auto mx-auto text-center">
                  <ul class="nav navbar-nav navbar-end">
                    <li>
                      <a target='_blank' href={"https://t.me/lnorb"}>
                      <Button
                        class="btn btn-primary navbar-btn btn-rounded waves-effect waves-light"
                        >Join us on Telegram</Button
                      ></a>
                    </li>
                  </ul>
                </div>
                <br/>
                <br/>
                <div class="nav-button ms-auto mx-auto text-center">
                  <ul class="nav navbar-nav navbar-end">
                    <li>
                      <a href={"/download"}>
                      <Button
                        class="btn btn-primary navbar-btn btn-rounded waves-effect waves-light"
                        >Download</Button
                      ></a>
                    </li>
                  </ul>
                </div>
            </Col>
        </Row>
    </Container>
</section>

</div>