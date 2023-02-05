<script>
    import Footer from '../Components/Footer.svelte';
    import { Modal, ModalBody, ModalHeader, Container, Row, Col } from 'sveltestrap';
    import { Card, CardBody, Button } from 'sveltestrap';
    import { FormGroup, Input, Label, Form } from 'sveltestrap';
    import { onMount } from "svelte";
    import * as animateScroll from "svelte-scrollto";
    import NavbarPlain from '../Components/NavbarPlain.svelte';
    import QrCode from "svelte-qrcode";
    import { v4 as uuidv4 } from "uuid";
    let license = null;
    let host = window.location.hostname == 'localhost' ? 'http://localhost:8000' : '';
    $: raw_invoice = urlParams.get('raw_invoice');
    const urlParams = new URLSearchParams(window.location.search);
    const edition = urlParams.get('edition');
    let done_scrolling = false;

    async function generate_invoice () {
        const res = await fetch(`${host}/api/orb/buy/generate-invoice?edition=${edition}`, {
            method: 'GET'
        })
        const data = await res.json();
        if (data.raw !== undefined){
            raw_invoice = data.raw;
            urlParams.set('raw_invoice', raw_invoice)
            window.history.replaceState({}, edition, `${window.location.pathname}?${urlParams.toString()}`)
        }
    }

    async function get_invoice_details() {
        const res = await fetch(`${host}/api/orb/buy/get-invoice-details?&raw_invoice=${raw_invoice}`, {
            method: 'GET'
        })
        const data = await res.json();
        if (data !== null && data.paid === true) {
            window.location.href = `/license?raw_invoice=${data.raw}&edition=${edition}`;
        }
    }

    export let id

    let progress = {}
    let poller

    const setupPoller = (id) => {
        if (poller) {
            clearInterval(poller)
        }
        poller = setInterval(doPoll(id), 1000)
    }

    const doPoll = (id) => async () => {
        get_invoice_details();
        progress[id] = await new Promise(resolve => setTimeout(() => {
            resolve((progress[id] || 0) + 1)
        }, 500))
    }

    $: setupPoller(id)

    onMount(() => {
        if (raw_invoice == null){
            generate_invoice()
        } else {
            get_invoice_details();
        }
    });
</script>

<NavbarPlain extraclass="" />
<section class="section bg-home vh-100 common-section" id="home">
    <div class="bg-overlay" />
    <div class="display-table">
        <div class="display-table-cell">
            <Container>
                <Row class="justify-content-center">
                    <Col lg={8} class="text-white text-center">
                        <h1 class="home-title">Buy</h1>
                        <h4 class="home-small-title">1 year {edition} edition license.</h4>
                        <p class="pt-3 home-desc mx-auto">
                        </p>
                    </Col>
                </Row>
                {#if raw_invoice !== null}
                <Row class="justify-content-center">
                    <Col lg={4} class="text-white text-center">
                        <QrCode value={raw_invoice} />
                        <p class="pt-3 home-desc mx-auto">By paying this invoice, you are agreeing to our <a href='/terms-and-conditions' target='_blank' style='color: #ee8156'>Terms and Conditions</a>.</p>
                    </Col>
                </Row>
                {:else}
                <Row class="justify-content-center">
                    <Col lg={8} class="text-white text-center">
                        <h4 class="home-small-title">Getting invoice. Please be patient.</h4>
                        <p class="pt-3 home-desc mx-auto">
                        </p>
                    </Col>
                </Row>
                {/if}
                {#if license === null}
                    {#if raw_invoice !== null}
                        <Row class="justify-content-center pt-3">
                            <Col lg={4} class="text-white text-center">
                                <h4 class="home-small-title">Once purchased, we'll process your licensing information.</h4>
                                <p class="pt-3 home-desc mx-auto">
                                </p>
                            </Col>
                        </Row>
                    {/if}
                {:else}
                    <Row class="justify-content-center pt-3">
                        <Col lg={4} class="text-white text-center">
                            <h4 class="home-small-title">Your license is ready. Please scroll down.</h4>
                        </Col>
                    </Row>
                {/if}
            </Container>
        </div>
    </div>
</section>
<Footer />
