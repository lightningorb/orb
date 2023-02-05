<script>
    import NavbarPlain from '../Components/NavbarPlain.svelte';
    import Download from './../Components/Download.svelte';
    import Footer from '../Components/Footer.svelte';

    import data from '../Data/data';
    document.getElementById('color-opt').href = '/css/colors/red.css';
</script>

<NavbarPlain extraclass="" />
<Download />
<Footer />