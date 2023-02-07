<!-- <script>
  import { Link } from "svelte-routing";
  import { scrollto } from "svelte-scrollto";
  import { onMount } from "svelte";
  import { Button } from "sveltestrap";
  export let extraclass;
  const toggleMenu = () => {
    document.getElementById("navbarCollapse").classList.toggle("show");
  };
  onMount(() => {
    var section = document.querySelectorAll(".common-section");
    var sections = {};
    var i = 0;
    Array.prototype.forEach.call(section, function (e) {
      sections[e.id] = e.offsetTop;
    });
    window.onscroll = function () {
      var scrollPosition =
        document.documentElement.scrollTop || document.body.scrollTop;
      for (i in sections) {
        if (sections[i] <= scrollPosition) {
          const qs = document.querySelector(".active");
          if (qs != null)
            qs.setAttribute("class", " ");
          const qs2 = document.querySelector("a[href*=" + i + "]")
          if (qs2 != null)
            qs2.setAttribute("class", "active");
        }
      }
    };
  });
  const handleScroll = () => {
    var navbar = document.getElementById("navbar");
    if (
      document.body.scrollTop > 50 ||
      document.documentElement.scrollTop > 50
    ) {
      navbar.classList.add("is-sticky");
    } else {
      navbar.classList.remove("is-sticky");
    }
  };
  window.addEventListener("scroll", handleScroll, { passive: false });
</script>
<div id="navbar">
  <nav
    class="navbar navbar-expand-lg fixed-top navbar-custom sticky sticky-dark {extraclass}"
    id="navbar"
  >
    <div class="container">
      <Link class="navbar-brand logo text-uppercase" to="/"><i class="mdi mdi:circle-outline"></i> Orb </Link>
      <Button class="navbar-toggler" on:click={toggleMenu}>
        <i class="mdi mdi-menu" />
      </Button>
      <div class="collapse navbar-collapse" id="navbarCollapse">
        <div class="nav-button ms-auto">
          <ul class="nav navbar-nav navbar-end">
            <li>
              <a href={"/dev-license"}>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </nav>
</div>
 -->
