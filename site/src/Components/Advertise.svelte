<script>
  import {
    Container,
    Row,
    Col,
    Table,
    FormGroup,
    Input,
    Label,
    Form
  } from "sveltestrap";
  import QrCode from "svelte-qrcode";
  import { onMount } from "svelte";
  let avatar, fileinput;
  $: ad_id = urlParams.get("ad_id");
  $: ad = null;
  $: creation_date = null;
  $: budget = 10000;
  $: run_for = 30;
  let host =
    window.location.hostname == "localhost" ? "http://localhost:8000" : "";
  const urlParams = new URLSearchParams(window.location.search);
  async function onFileSelected(e) {
    let image = e.target.files[0];
    let formData = new FormData();
    formData.append("file", image);
    const res = await fetch(`${host}/api/ads/upload_image`, {
      method: "POST",
      body: formData,
    });
    const data = await res.json();
    if (data != null && data.detail == "success") {
      urlParams.set("ad_id", data.ad_id);
      ad_id = data.ad_id;
      window.history.replaceState(
        {},
        "ad_id",
        `${window.location.pathname}?${urlParams.toString()}`
      );
    }
  }

  async function get_ad_details() {
    if (ad_id){
        const res = await fetch(`${host}/api/ads/?id=${ad_id}`, {
          method: "GET",
        });
        const data = await res.json();
        ad = data;
        const date = new Date(0);
        date.setUTCSeconds(ad.created);
        creation_date = date.toISOString();
    }
  }

  async function generate_invoice() {
    if (ad_id){
        const res = await fetch(`${host}/api/ads/generate-invoice?amount=${budget}&ad_id=${ad_id}&run_for=${run_for}`, {
          method: "GET",
        });
        const data = await res.json();
    }
  }

  export let id;

  let progress = {};
  let poller;

  const setupPoller = (id) => {
    if (poller) {
      clearInterval(poller);
    }
    poller = setInterval(doPoll(id), 1000);
  };

  const doPoll = (id) => async () => {
    get_ad_details();
    progress[id] = await new Promise((resolve) =>
      setTimeout(() => {
        resolve((progress[id] || 0) + 1);
      }, 500)
    );
  };

  $: setupPoller(id);
</script>

<div>
  <section class="section bg-home vh-100 common-section" id="dev-license">
    <div class="bg-overlay" />
    <div class="display-table">
      <div class="display-table-cell">
        <Container>
          <Row class="justify-content-center">
            <Col lg={8} class="text-white text-center">
              <h1 class="home-title">Advertise in-app</h1>
              <h4 class="home-small-title">
                Reach our network of free users, for 丰10K CPM.
              </h4>
              <p class="pt-3 mx-auto">1 view == 1 minute of display time.</p>
            </Col>
          </Row>
          <Row class="justify-content-center">
            <Col sm={5} class="text-white text-center">
              <Table class="text-white" responsive>
                <thead>
                  <tr>
                    <th />
                    <th>Viewing time:</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <th scope="row">丰10K</th>
                    <td>16h 40m</td>
                  </tr>
                  <tr>
                    <th scope="row">丰100K</th>
                    <td>~7 days</td>
                  </tr>
                  <tr>
                    <th scope="row">丰1M</th>
                    <td>~2 months</td>
                  </tr>
                </tbody>
              </Table>
            </Col>
          </Row>
        </Container>
      </div>
    </div>
  </section>

  <section class="section bg-light common-section" id="services">
    <Container>
      <Row>
        <Col class="justify-content-center" lg={{ size: 6, offset: 3 }}>
          {#if ad}
            <img class="avatar justify-content-center" src={`${host}/api/ads/image?id=${ad_id}`} alt="d" />
            <Table class="text-black" responsive>
              <thead>
                <tr>
                  <th>Stats</th>
                  <th />
                </tr>
              </thead>
              <tbody>
                <tr>
                  <th scope="row">created</th>
                  <td>{creation_date}</td>
                </tr>
                <tr>
                  <th scope="row">paid for</th>
                  <td>{ad.paid_for_minutes} minutes</td>
                </tr>
                <tr>
                  <th scope="row">displayed for</th>
                  <td>{Math.floor(ad.viewed_seconds / 60)} minutes {Math.round(60 * (ad.viewed_seconds / 60 - Math.floor(ad.viewed_seconds / 60)))} seconds</td>
                </tr>
<!--                 <tr>
                  <th scope="row">run for</th>
                  <td>{ad.run_for} days minimum</td>
                </tr> -->
                <tr>
                  <th scope="row">approved</th>
                  <td>{ad.approved}</td>
                </tr>
                <tr>
                  <th scope="row">active</th>
                  <td>{ad.current}</td>
                </tr>
<!--                 <tr>
                  <th scope="row">clicks</th>
                  <td>{ad.clicks}</td>
                </tr> -->
              </tbody>
            </Table>
          {:else}
            <img
              class="avatar justify-content-center"
              src="https://via.placeholder.com/500x100.png?text=Your%20500x100%20png"
              alt=""
            />
            <img
              class="upload"
              src="https://static.thenounproject.com/png/625182-200.png"
              alt=""
              on:click={() => {
                fileinput.click();
              }}
            />
            <input
              style="display:none"
              type="file"
              accept=".jpg, .jpeg, .png"
              on:change={(e) => onFileSelected(e)}
              bind:this={fileinput}
            />
          {/if}
        </Col>
      </Row>
      {#if ! (ad && ad.raw_invoice)}
          <hr style="color: black; opacity: 1;" />
          <Row>
            <Col class="justify-content-center" lg={{ size: 4, offset: 4 }}>
              <FormGroup>
                <Label for="exampleNumber">Budget (sats)</Label>
                <Input
                  type="number"
                  name="number"
                  bind:value={budget}
                  placeholder="1000000"
                />
              </FormGroup>
            </Col>
          </Row>
<!--           <Row>
            <Col class="justify-content-center" lg={{ size: 4, offset: 4 }}>
              <FormGroup>
                <Label for="exampleNumber">Run For (days)</Label>
                <Input
                  type="number"
                  name="number"
                  bind:value={run_for}
                  placeholder="30"
                />
              </FormGroup>
            </Col>
          </Row> -->
          <Row>
            <Col class="justify-content-center" lg={{ size: 2, offset: 5 }}>
              <p
                on:click={() => generate_invoice()}
                class="btn btn-primary waves-effect waves-light mt-3 mb-5"
                style="width: 100%; color: white !important; "
              >
                Generate Invoice
              </p>
            </Col>
          </Row>
      {/if}
      {#if ad && ad.raw_invoice && ad.paid_for_minutes == 0}
          <Row class="justify-content-center">
            <Col lg={4} class="text-white text-center">
              <QrCode
                value={ad.raw_invoice}
              />
              <!-- <p class="pt-3 home-desc mx-auto">By paying this invoice, you are agreeing to our <a href='/terms-and-conditions' target='_blank' style='color: #ee8156'>Terms and Conditions</a>.</p> -->
            </Col>
          </Row>
      {/if}
    </Container>
  </section>
</div>
