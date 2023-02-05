<script>
    import Footer from '../Components/Footer.svelte';
    import { Button, Container, Row, Col, FormGroup, Input } from 'sveltestrap';
    import { onMount } from "svelte";
    import NavbarPlain from '../Components/NavbarPlain.svelte';
    import { v4 as uuidv4 } from "uuid";
    let license = null;
    let host = window.location.hostname == 'localhost' ? 'http://localhost:8000' : '';
    $: isShown = false;
    const urlParams = new URLSearchParams(window.location.search);
    const edition = urlParams.get('edition');
    $: rand_id = urlParams.get('rand_id');

    function download(filename, text) {
        var element = document.createElement('a');
        element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
        element.setAttribute('download', filename);
        element.style.display = 'none';
        document.body.appendChild(element);
        element.click();
        document.body.removeChild(element);
    }

    async function get_license_info () {
        if (rand_id != null){
            const res = await fetch(`${host}/api/orb/evaluate/get-license-details?&rand_id=${rand_id}`, {
                method: 'GET'
            })
            const data = await res.json();
            if (data !== undefined && data.key !== undefined) {
                license = data;
            }
        }
    }

    async function generate_license () {
        if (license === null){
            const res = await fetch(`${host}/api/orb/evaluate/generate-license`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    edition: edition
                })
            })
            const data = await res.json();
            if (data !== undefined && data.key !== undefined) {
                license = data;
                rand_id = license.rand_id
                urlParams.set('rand_id', rand_id);
                window.history.replaceState({}, 'rand_id', `${window.location.pathname}?${urlParams.toString()}`);
            }
        }
    }
    onMount(() => {
        get_license_info()
    });
</script>

<NavbarPlain extraclass="" />
<section class="section bg-home vh-100 common-section" id="home">
    <div class="bg-overlay" />
    <div class="display-table">
        <div class="display-table-cell">
            <Container>
                <Row class="justify-content-center">
                    <Col lg={6} class="text-white text-center">
                        <h1 class="home-title">Your Personal Evaluation License</h1>
                        {#if license == null}
                        <h4 class="home-small-title">Generate a free evaluation license, valid for 30 days.</h4>
                        <div class="mt-3 nav-button ms-auto mx-auto text-center">
                          <ul class="nav navbar-nav navbar-end">
                            <li>
                              <Button
                                class="btn btn-primary navbar-btn btn-rounded waves-effect waves-light"
                                on:click|once={generate_license}
                                >Generate License</Button>
                            </li>
                          </ul>
                        </div>
                        {/if}
                        {#if license != null}
                        <h4 class="home-small-title">Please store your license safely in a 'license.lic' file.</h4>
                          <Button
                            class="btn btn-primary navbar-btn btn-rounded waves-effect waves-light" on:click={() => download('license.lic', license.key)}
                            >Download license.lic</Button>
                            <div class="mt-5 nav-button ms-auto mx-auto text-center">
                              <ul class="nav navbar-nav navbar-end">
                                <li>
                                  <a href={'/download?rand_id=' + rand_id}>
                                      <Button
                                        class="btn btn-primary navbar-btn btn-rounded waves-effect waves-light"
                                        >Download Orb</Button>
                                  </a>
                                </li>
                              </ul>
                            </div>
                        {/if}
                    </Col>
                </Row>
            </Container>
        </div>
    </div>
</section>
<Footer />
