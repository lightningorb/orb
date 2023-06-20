<script>
    import NavbarPlain from './NavbarPlain.svelte';
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


<style>
    .main-container {
        display: flex;
        flex-direction: column;
        align-items: center;
    }

    .laptop-frame {
        background-image: url('https://static.wixstatic.com/media/96674d_2fcf62dc94f24e5a96f7d341b006c492~mv2.png/v1/fill/w_1260,h_755,al_c,q_90,enc_auto/96674d_2fcf62dc94f24e5a96f7d341b006c492~mv2.png');
        background-size: cover;
        background-repeat: no-repeat;
        width: 640px;
        height: 400px;
        padding-top: 35px;
        padding-left: 27px;
        box-sizing: border-box;
        display: flex;
        justify-content: center;
    }

    .laptop-video {
        width: 486px;
        height: 300px;
    }
</style>

<div class="main-container section bg-light common-section">
    <h1 class="home-title">Intro to LN</h1>
    <h4 class="home-small-title">Discover the Lightning Network with our hands-on Orb tutorials.</h4>

    <div class="laptop-frame">
<!--         <video class="laptop-video" controls>
            <source src="https://lnorb.com/course/intro/intro.mov" type="video/mp4">
            Your browser does not support the video tag.
        </video> -->
        <iframe width="490" height="320" src="https://www.youtube.com/embed?listType=playlist&list=PL1xGN4d9nOKuCkUZQExTHsYzLPptQ28NM" frameborder="0" allowfullscreen></iframe>
    </div>

<!--     <form on:submit|preventDefault={submitEmail}>
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
    {/if} -->
</div>