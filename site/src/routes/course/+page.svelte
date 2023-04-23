 <script>
    import NavbarPlain from '../../Components/NavbarPlain.svelte';
    import { Button, Form, FormGroup, FormText, Input, Label } from 'sveltestrap';
    import { Modal, ModalBody, ModalHeader, Container, Row, Col, Styles } from 'sveltestrap';
    import { onMount } from 'svelte';

    let email = '';
    let statusMessage = '';

    async function submitEmail() {
        try {
            const response = await fetch('https://4wuzfpyv54z7tykr5jo6nw2cfy0kfhog.lambda-url.us-east-2.on.aws/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ email })
            });

            if (response.ok) {
                console.log(await response.json());
                statusMessage = 'Thank you! Your interest has been registered.';
            } else {
                statusMessage = 'Oops! Something went wrong. Please try again later.';
            }
            console.log(response);
        } catch (error) {
            console.error('Error submitting email:', error);
            statusMessage = 'Oops! Something went wrong. Please try again later.';
        }
    }
</script>

<section class="section vh-100 common-section text-black" id="priv">
    <div class="display-table">
        <div class="display-table-cell">
            <Container>
                <Row class="justify-content-center">
                    <Col lg={8} class="text-center">
                        <h1 class="home-title">Intro to LN Course</h1>
                        <h4 class="home-small-title">Discover the Lightning Network and Orb in a simple and engaging way.</h4>
                        <p class="pt-3 text-black mx-auto">
                            Our "Intro to LN Course" aims to provide a comprehensive understanding of the Lightning Network, its core principles, and how Orb fits into this innovative ecosystem. This course is perfect for beginners looking to expand their knowledge in the world of Bitcoin & Lightning, as well as experienced users who want to stay up-to-date with the latest developments in the Lightning Network.
                        </p>
                        <p class="pt-3 text-black mx-auto">
                            Register your interest by entering your email address below, and we'll notify you when the course becomes available. Stay tuned and get ready to unlock the full potential of the Lightning Network!
                        </p>
                        <form on:submit|preventDefault={submitEmail}>
                            <div class="input-group mb-3">
                                <Input type="email" class="form-control" placeholder="Your Email Address" aria-label="Your Email Address" aria-describedby="basic-addon2" bind:value={email} required />
                                <div class="input-group-append">
                                    <Button class="btn btn-primary" on:click|once={submitEmail}>Register Interest</Button>
                                </div>
                            </div>
                        </form>
                        {#if statusMessage}
                            <p class="pt-3 text-black mx-auto">
                                {statusMessage}
                            </p>
                        {/if}
                    </Col>
                </Row>
            </Container>
        </div>
    </div>
</section>
