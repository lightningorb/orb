<!-- Team component -->
<script>
  import { Col, Row, Container } from "sveltestrap";

  export let teamData = {};
  const { title, description, team_list } = teamData;
</script>

<!--START TEAM-->
<section class="section common-section" id="about">
  <Container>
    <Row>
      <Col lg={{ size: 8, offset: 2 }}>
        <h1 class="section-title text-center">{title}</h1>
        <div class="section-title-border mt-3" />
        <p class="section-subtitle text-muted text-center font-secondary pt-4">
          {description}
        </p>
      </Col>
    </Row>
    <Row class="mt-5">
      {#each team_list as list}
        <Col lg="3" sm="6">
          <div class="team-box text-center">
            <div class="team-wrapper">
              <div class="team-member">
                <img alt="" src={list.profile} class="img-fluid rounded" />
              </div>
            </div>
            <h4 class="team-name">{list.name}</h4>
            <p class="text-uppercase team-designation">{list.designation}</p>
          </div>
        </Col>
      {/each}
    </Row>
  </Container>
</section>
<!--END TEAM-->

