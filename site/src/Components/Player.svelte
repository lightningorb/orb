<script>
    export let videoElement;
    export let width = "500px";
    export let height = "300px";
</script>

<video bind:this={videoElement} id="my-video" class="video-js vjs-default-skin" 
       controls preload="auto" >
    <p class="vjs-no-js">
        To view this video please enable JavaScript, and consider upgrading to a web browser that
        <a href="https://videojs.com/html5-video-support/">supports HTML5 video</a>
    </p>
    <track kind='captions'/>
</video>
