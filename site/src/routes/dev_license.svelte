<script>
    import NavbarPlain from '../Components/NavbarPlain.svelte';
    import Footer from '../Components/Footer.svelte';
    import DevLicense from './../Components/DevLicense.svelte';

    import data from '../Data/data';
    document.getElementById('color-opt').href = '/css/colors/red.css';
</script>

<NavbarPlain extraclass="" />
<DevLicense />
<Footer />