<script>
    import Footer from '../Components/Footer.svelte';
    import NavbarPlain from '../Components/NavbarPlain.svelte';
    import { Modal, ModalBody, ModalHeader , Container, Row, Col } from 'sveltestrap';
  import SvelteMarkdown from 'svelte-markdown'

  const source = `
Love is patient, love is kind.

It does not envy, it does not boast, it is not proud.

It does not dishonor others, it is not self-seeking, it is not easily angered, it keeps no record of wrongs.

Love does not delight in evil but rejoices with the truth.

It always protects, always trusts, always hopes, always perseveres.
`

</script>

<NavbarPlain extraclass="" />

<section class="section common-section text-black">
    <div class="display-table">
        <div class="display-table-cell">
            <Container>
                <Row>
                    <Col lg={{size: 8, offset: 2}}>
                        <div class='love'>
                            <SvelteMarkdown {source} />
                        </div>
                    </Col>
                </Row>
            </Container>
        </div>
    </div>
</section>

<Footer />
