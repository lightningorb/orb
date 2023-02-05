<script>
    import NavbarPlain from '../Components/NavbarPlain.svelte';
    import Footer from '../Components/Footer.svelte';
    import HireMe from './../Components/HireMe.svelte';

    import data from '../Data/data';
    document.getElementById('color-opt').href = '/css/colors/red.css';
</script>

<NavbarPlain extraclass="" />
<HireMe />
<Footer />