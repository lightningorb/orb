<script>
  import NavbarPlain from './NavbarPlain.svelte';
  import { Button, Form, FormGroup, FormText, Input, Label } from 'sveltestrap';
  import { Modal, ModalBody, ModalHeader, Container, Row, Col, Styles } from 'sveltestrap';
  import { onMount } from 'svelte';
  import { browser } from "$app/environment";
    $: outerWidth = 0
    $: innerWidth = 0
    $: outerHeight = 0
    $: innerHeight = 0
</script>

<svelte:window bind:innerWidth bind:outerWidth bind:innerHeight bind:outerHeight />

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
    <Container>
        <Row>
            <Col lg={{ size: 8, offset: 2 }}>
            <h1 class="home-title">Intro to LN</h1>
            <h4 class="home-small-title">Discover the Lightning Network with our hands-on Orb tutorials.</h4>
            {#if innerWidth < 500}
            <iframe width="490" height="320" src="https://www.youtube.com/embed?listType=playlist&list=PL1xGN4d9nOKuCkUZQExTHsYzLPptQ28NM" frameborder="0" allowfullscreen></iframe>
            {:else}
            <div class="laptop-frame">
                <iframe width="490" height="320" src="https://www.youtube.com/embed?listType=playlist&list=PL1xGN4d9nOKuCkUZQExTHsYzLPptQ28NM" frameborder="0" allowfullscreen></iframe>
            </div>
            {/if}
            </Col>
        </Row>
    </Container>
</div>