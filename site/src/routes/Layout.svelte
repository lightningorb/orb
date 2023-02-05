<script>
	import Navbar from '../Components/Navbar.svelte';
    import HomeSection from './HomeSection.svelte';
	import AboutUs from '../Components/AboutUs.svelte';
	import Services from '../Components/Services.svelte';
	import Gallery from '../Components/Gallery.svelte';
	import Pricing from '../Components/Pricing.svelte';
	import Footer from '../Components/Footer.svelte';
	import Download from './../Components/Download.svelte';
	import Testimonial from './../Components/Testimonial.svelte';

	import data from '../Data/data';
	document.getElementById('color-opt').href = '/css/colors/orange.css';
</script>

<Navbar extraclass="" />
<HomeSection />
<AboutUs />
<Services serviceData={data.SERVICE_DATA} websiteData={data.WEBSITE_DESCRIPTION} />
<Gallery galleryData={data.GALLERY_DATA}/>
<!-- <Pricing pricingData={data.PRICING_DATA} /> -->
<Download />
<Testimonial testimonialData={data.TESATIMONIAL_DATA} />
<Footer />