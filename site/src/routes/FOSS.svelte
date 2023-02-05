<script>
    import Footer from '../Components/Footer.svelte';
    import NavbarPlain from '../Components/NavbarPlain.svelte';
    import { Modal, ModalBody, ModalHeader , Container, Row, Col } from 'sveltestrap';
  import SvelteMarkdown from 'svelte-markdown'

  const source = `
With the [FOSS](https://en.wikipedia.org/wiki/Free_and_open-source_software) topic being discussed so ardently across the internet and this space, we think it is important to address it up-front.

We started working on Orb in October 2021. For us, Orb is currently a net loss which is why we are closed source. We are investing our own time & funds into the development of Orb, and feel it would not benefit the project to simply open source it without a revenue model in place. Given the current model, we hope customer license purchases can fund future development.

However, we are very open to the FOSS movement, we are very strongly considering switching to FOSS, and are open to funding offers that would ensure Orb's future development, release and support roadmap under a FOSS model.

# Our reviewers

Our git repo is currently open to prominent technical members of the Bitcoin and Lightning space. While this is not an adequate substitute for FOSS, it does to some extent mitigate the possibility of us doing anything harmful or malicious since those community members would be the first to ring the alarm bells.

We are open to on-boarding more reviewers.

# FOSS projects need funding

High quality software development and engineering take decades of education and sustained focus. There is a very significant opportunity cost associated with FOSS development, and it cannot simply be ignored. We feel it is unreasonable to expect software to simply be free without a proper revenue model in place. Developers cannot be expected to simply invest their time and funds into projects without a proper incentive stucture in place.

To some extent, this is like expecting any other industry professional, such as a Doctor or a Lawyer to simply work for free, and the pro-foss arguments, taken to an extreme can be used to demand for unpaid labour, which is obviously an unreasonable expectation, and mis-understanding of the FOSS movement.

FOSS projects are predominently funded by companies that rely on closed source software as their source of income:

<img width='600px' style='display: block; margin-left: auto; margin-right: auto;' src='https://s3-us-east-2.amazonaws.com/lnorb/docs/Top_Companies_Contributing_to_Open_Source_-_20112021_-_Statistics_and_Data_2022-02-17_04-27-42.png'/>

This does depend on the [metric being used](https://statisticsanddata.org/data/top-companies-contributing-to-open-source-2011-2020/). However, regardless of the metric, one constant remains: companies that sell closed source software are very prominent FOSS contributors.

Like everything being discussed over the internet, the nuance tends to get lost. It is vital to understand the dynamics that make FOSS possible in the first place. Some projects are better off being closed source, and some are better off being open. Currently we believe being closed source offers the greatest likelihood of success for Orb, but we are open to offers that would enable us to be FOSS.

# We cannot ignore the pro-foss arguments

It's becoming impossible to ignore the pro-foss arguments. Bitcoin and lightning are both open source protocols and codebases, and simply holding Bitcoin has more than amply funded Orb's development.

# If we remain closed source

In the worst case scenario (from a FOSS standpoint) we intend on open-sourcing a lot of our UI and business logic code. We have already made many contributions to open source projects over the years, and hope to make a lot more for many years to come.

# Get in touch

If you believe Orb should be FOSS, and have suggestions on sensible incentives structures or funder offers, please reach out to us on Telegram: [@lnorb](https://t.me/@lnorb).
`

</script>

<NavbarPlain extraclass="" />

<section class="section common-section text-black">
    <div class="display-table">
        <div class="display-table-cell">
            <Container>
                <Row>
                    <Col lg={{size: 8, offset: 2}}>
                        <h1 class="home-title">FOSS</h1>
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
