<script>
    import { browser } from '$app/environment';
    import { Container, Row, Col } from 'sveltestrap';
    import { onMount, afterUpdate } from 'svelte';
    import { page } from '$app/stores';
    import './CourseStyle.css';
    import Player from './Player.svelte';

    $: outerWidth = 0
    $: innerWidth = 0
    $: outerHeight = 0
    $: innerHeight = 0

    const resolutions = ['1440p', '1080p', '720p', '480p', '360p'];
    let videos = [
        'what_is_the_lightning_network',
        "blockstream_green_testnet_wallet",
        "bitcoin_testnet_faucets",
        "installing_orb_on_ios",
        "installing_orb_on_android",
        "installing_orb_on_osx",
        "creating_a_node_on_voltage",
        "opening_channels",
        "inbound_liquidity",
        "liquidity_and_ppm",
        "circular_rebalancing",
        "batch_opening_channels",
        "submarine_swaps",
        "automated_channel_rebalancing",
    ];
    
    let selectedVideo = 'what_is_the_lightning_network';
    let large = false;

    const searchParams = browser && $page.url.searchParams;

    if (!searchParams) {
        selectedVideo = 'automated_channel_rebalancing';
        large = true;
    } else {
        selectedVideo = searchParams.get('video') || videos[0];
        large = searchParams.get('large') == 'true';
    }

    let getSources = (video) => resolutions.map(resolution => ({
        src: `https://lnorb.com/course/intro/${video}/${video}_${resolution}.mp4`,
        type: 'video/mp4',
        label: resolution,
        res: parseInt(resolution),
    }));

    let videoElement;
    let player;

    onMount(async () => {
        const script = document.createElement('script');
        script.src = 'https://vjs.zencdn.net/7.8.4/video.js';
        script.async = true;
        document.body.appendChild(script);
    
        script.onload = () => {
            videoElement.setAttribute('data-setup', JSON.stringify({
                plugins: {
                    videoJsResolutionSwitcher: {
                        default: "high"
                    }
                }
            }));
            videoElement.controls = true;
            videoElement.preload = 'auto';
            const res = document.createElement('script');
            res.src = 'https://cdnjs.cloudflare.com/ajax/libs/videojs-resolution-switcher/0.4.2/videojs-resolution-switcher.js';
            res.async = true;
            document.body.appendChild(res);
            res.onload = () => {
                const videojs = window.videojs;
                player = videojs('my-video', {height: Math.min(innerHeight-30, 320), width: Math.min(innerWidth-30, 490)});
                player.controlBar.fullscreenToggle.on = function() {
                    console.log("fullscreen");
                }
                player.updateSrc(getSources(selectedVideo));
            };
        };
    });

    afterUpdate(() => {
        if(player) {
            player.updateSrc(getSources(selectedVideo));
            window.history.pushState({}, '', `?video=${selectedVideo}&large=${large}`);
        }
    });

</script>

<svelte:window bind:innerWidth bind:outerWidth bind:innerHeight bind:outerHeight />

<style>
:global(.vjs-resolution-button) {
    top: -30px;
}

:global(.vjs-menu-button-popup .vjs-menu) {
    top: 6em;
}
</style>

{#if large}
    <select bind:value={selectedVideo}>
        {#each videos as video (video)}
            <option>{video}</option>
        {/each}
    </select>
    <Player width={innerWidth + 'px'} height={innerHeight + 'px'} bind:videoElement={videoElement}></Player>
{:else}
    <div class="main-container section bg-light common-section">
        <Container>
            <Row>
                <Col lg={{ size: 8, offset: 2 }}>
                <h1 class="home-title">Intro to LN</h1>
                <h4 class="home-small-title">Discover the Lightning Network with our hands-on Orb tutorials.</h4>
                {#if innerWidth < 500}
                <Player width={'490px'} height={'320px'} bind:videoElement={videoElement}></Player>
                {:else}
                <div class="laptop-frame">
                    <Player width={'490px'} height={'320px'} bind:videoElement={videoElement}></Player>
                </div>
                {/if}
                <select bind:value={selectedVideo}>
                    {#each videos as video (video)}
                        <option>{video}</option>
                    {/each}
                </select>
                </Col>
            </Row>
        </Container>
    </div>
{/if}