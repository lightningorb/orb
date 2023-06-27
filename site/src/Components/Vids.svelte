<style>
  .video-player {
    width: 100%;
    height: 550px; /* adjust as needed */
    object-fit: cover; /* maintain aspect ratio */
  }

  @media (max-width: 768px) {
    .video-player {
      height: auto; /* reset to original video aspect ratio on smaller screens */
    }
  }
</style>

<script>
  import { Container, Row, Col, Styles } from 'sveltestrap';
    $: outerWidth = 0
    $: innerWidth = 0
    $: outerHeight = 0
    $: innerHeight = 0
</script>

<svelte:window bind:innerWidth bind:outerWidth bind:innerHeight bind:outerHeight />

<div class="main-container section bg common-section">
    <Container>
        <Row>
            <Col lg={{ size: 8, offset: 2 }}>
              <h1 class="home-title">See Orb's advanced rebalancing in action</h1>
              <br/>
              <br/>
            </Col>
        </Row>  
        <Row>
            <Col lg="6">
              <video class="video-player" controls loop>
                <source src="https://lnorb.com/vids/27_07_2022.mov" type="video/mp4">
                Your browser does not support the video tag.
              </video>
            </Col>
            <Col lg="6">
              <video class="video-player" controls loop>
                <source src="https://lnorb.com/vids/22_07_2022.mov" type="video/mp4">
                Your browser does not support the video tag.
              </video>
            </Col>
        </Row>
    </Container>
</div>
