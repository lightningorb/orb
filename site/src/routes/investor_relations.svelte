<script>
    import Footer from '../Components/Footer.svelte';
    import NavbarPlain from '../Components/NavbarPlain.svelte';
    import { Modal, ModalBody, ModalHeader , Container, Row, Col } from 'sveltestrap';
  import SvelteMarkdown from 'svelte-markdown'

  const source = `

Picture tens of thousands of lightning node operators waking up in the morning, and opening Orb before any other app, to check what fees they made overnight, and to check the status of their channels. Orb's user experience is sticky because we spent a year listening to operators, and built an application suite they actually needed, from first principles.

Development started in October 2021 and is self-funded, so we have no liabilities. The market for advanced handcrafted lightning apps is currently still a greenfield with blue skies. Orb embodies the very best of our software craftsmanship, and is currently the most sophisticated and beautiful lightning end-user application available.

Orb has the potential to electrify the lightning network end-user application space. As such we are keen on talking with investors, as we truly believe that together we can speed up lightning network adoption, and push it into the mainstream.

If you are an investor and would be interested in this common persuit, please get in touch with us via our Telegram: [@lnorb](https://t.me/@lnorb).
`

</script>

<NavbarPlain extraclass="" />

<section class="section common-section text-black">
    <div class="display-table">
        <div class="display-table-cell">
            <Container>
                <Row>
                    <Col lg={{size: 8, offset: 2}}>
                        <h1 class="home-title">Investor Relations</h1>
                        <br/>
                        <div class='terms'>
                            <SvelteMarkdown {source} />
                        </div>
                    </Col>
                </Row>
            </Container>
        </div>
    </div>
</section>

<Footer />
