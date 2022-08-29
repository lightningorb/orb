<script>
    import { Styles } from 'sveltestrap';
	import { Progress } from 'sveltestrap';
    import { onMount } from "svelte";
    import { Col, Container, Row } from 'sveltestrap';
    export let id;
    let progress = {};
    let poller;
	let info;
	let channels;

	  import {
	    Button,
	    Card,
	    CardBody,
	    CardFooter,
	    CardHeader,
	    CardSubtitle,
	    CardText,
	    CardTitle
	  } from 'sveltestrap';

    async function get_info() {
		const res = await fetch(`../info`);
		info = await res.json();
    }

    async function get_channels() {
		const res = await fetch(`../channels`);
		channels = await res.json();
    }

    const setupPoller = (id) => {
        if (poller) {
            clearInterval(poller)
        }
        poller = setInterval(doPoll(id), 5000)
    }

    const doPoll = (id) => async () => {
        get_info();
        get_channels();
        progress[id] = await new Promise(resolve => setTimeout(() => {
            resolve((progress[id] || 0) + 1)
        }, 500))
    }

    $: setupPoller(id)

    onMount(() => {
        get_info();
        get_channels();
    });
</script>

<svelte:head>
	<title>Orb</title>
	<html lang="en" />
</svelte:head>

<main>
	{#if info}
		<h1>{info.alias}</h1>
		<p>Block height: {info.block_height}</p>
		<p>Pubkey: {info.identity_pubkey}</p>
		<p>Network: {info.network}</p>
		<p>Active Channels: {info.num_active_channels} ({info.num_inactive_channels} inactive)</p>
		<p>Peers: {info.num_peers}</p>
		<p>Version: {info.version}</p>
	{/if}
	{#if channels}
		<h2>Channels:</h2>
		{#each channels as channel}
		  	<Row>
		    <Col md={{ size: 6, offset: 3 }}>
				<Card class="mb-3">
				  <CardHeader>
				    <CardTitle>{channel.alias}</CardTitle>
				  </CardHeader>
				  <CardBody>
				    <CardSubtitle>Profit: {channel.profit.toLocaleString()} 丰</CardSubtitle>
				    <CardText>
						<Progress value={(channel.local_balance / channel.capacity)*100} />
						<div>Capacity: {channel.capacity.toLocaleString()}丰</div>
						<div>Local Balance: {channel.local_balance.toLocaleString()}丰</div>
				    </CardText>
				  </CardBody>
				</Card>
			</Col>
		  	</Row>
		{/each}
	{/if}
</main>

<style>
	main {
		text-align: center;
		padding: 1em;
		max-width: 240px;
		margin: 0 auto;
	}

	h1 {
		color: #ff3e00;
		text-transform: uppercase;
		font-size: 4em;
		font-weight: 100;
	}

	@media (min-width: 640px) {
		main {
			max-width: none;
		}
	}
</style>

<Styles />
