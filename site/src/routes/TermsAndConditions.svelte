<script>
    import NavbarPlain from '../Components/NavbarPlain.svelte';
    import { Modal, ModalBody, ModalHeader , Container, Row, Col } from 'sveltestrap';
  import SvelteMarkdown from 'svelte-markdown'

  const source = `
# Orb as a legal entity

Currenty Orb has no legal status as it is not a registered business. As such, Orb's creators make no guarantees whatsoever and strongly advise you against the use of Orb on mainnet nodes.

# Orb v.s LND

Before delving into the terms and conditions, it is important to make clear distinctions between the risks of running an LND node, and the risks of using Orb. The risks associated with running an LND node are clearly stated in LND's [security guidelines](https://github.com/lightningnetwork/lnd/blob/master/docs/safety.md):

>> "Allocating life-changing amounts of BTC to the lightning network is currently considered #reckless."

Likewise allocating life-changing amounts of BTC to an Orb-operated node is currently considered #reckless.

By agreeing to our terms
------------------------

By agreeing to our terms, you confirm that:

- You have read and understood LND's security guidelines.
- You are capable of running an LND node according to LND's guidelines.
- You clearly understand the distinction between LND, and Orb.
- Total and irreversable loss of funds while running a production node is **a very tangible possibility**, not a technical or hypothetical one.
- Running Orb with LND on a production (mainnet node, with mainet Bitcoin) can result in you **losing all your Bitcoin**.
- While Orb does everything it can for its software to be as safe as possible, and its software is used daily on very large and active production nodes, **you are to be held responsible for any loss of funds that may occur, as Orb in its current (legal) state is more suited for Testnet or Signet nodes rather than production nodes, and we strongly advise against its use on production nodes**.
- **Orb is not to be held responsible for loss of funds**, whether they be due to the operator, LND, or Orb.

# Start with a testnet node.

It is our <b>strong</b> recommendation you start using Orb with a testnet node. You can spawn a free testnet node over at [Voltage](https://valtage.cloud) and be up & running with Orb in a matter of minutes. Do plenty of testing with your testnet node before graduating on to something else.

# Graduate to the Signet.

Your next move should be to start a Signet node, and join the [Plebnet Playground](https://plebnet.wiki/wiki/Plebnet_Playground). The Plebnet Playground provides your node with a lot of routing activity, and is a much better approximation of a production environment than a testnet node.

The Plebnet Playground provides you with the ideal environment to really familiarize yourself with Orb's more in-depth functionality, such as, but not limited to, automated fees, and automated rebalancing.

# Production Use

We strongly advise against the use of Orb on the mainnet. By agreeing to our Terms and Conditions, you agree that such an endeavour, and its outcomes are entirely your responsibility, not ours.

# Node Profitability

Running a profitable node is hard, and requires a lot of skill. Automating node profitability is an extremely hard. Our current approach is providing our users with a set of powerful automation tools. Once we have released Orb into the world, we'll look forwards to getting feedback from our users, and fine-tuning our automation tools for automated profitability.
`

</script>

<NavbarPlain extraclass="" />

<section class="section vh-100 common-section text-black" id="priv">
    <div class="display-table">
        <div class="display-table-cell">
            <Container>
                <Row>
                    <Col lg={{size: 8, offset: 2}}>
                        <h1 class="home-title">Terms and Conditions</h1>
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
