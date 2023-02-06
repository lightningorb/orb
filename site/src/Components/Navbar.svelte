<script>
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
    if (window)
    window.onscroll = function () {
      var scrollPosition =
        document.documentElement.scrollTop || document.body.scrollTop;
      for (i in sections) {
        if (sections[i] <= scrollPosition) {
          document.querySelector(".active").setAttribute("class", " ");
          document
            .querySelector("a[href*=" + i + "]")
            .setAttribute("class", "active");
        }
      }
    };
    if (window)
      window.addEventListener("scroll", handleScroll, { passive: false });
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
</script>
<div id="navbar">
  <nav
    class="navbar navbar-expand-lg fixed-top navbar-custom sticky sticky-dark {extraclass}"
    id="navbar"
  >
    <div class="container">
      <Button class="navbar-toggler" on:click={toggleMenu}>
        <i class="mdi mdi-menu" />
      </Button>
      <div class="collapse navbar-collapse" id="navbarCollapse">
        <ul class="navbar-nav navbar-center" id="navbar-navlist">
          <li class="nav-item">
            <a use:scrollto={"#home"} href={"#home"} class="nav-link active"
              >Home</a
            >
          </li>
          <li class="nav-item">
            <a use:scrollto={"#features"} href={"#features"} class="nav-link"
              >Features</a
            >
          </li>
          <li class="nav-item">
            <a use:scrollto={"#services"} href={"#services"} class="nav-link"
              >Who we are</a
            >
          </li>
          <li class="nav-item">
            <a use:scrollto={"#about"} href={"#about"} class="nav-link"
              >About</a>
          </li>
          <li class="nav-item">
            <a use:scrollto={"#download"} href={"#download"} class="nav-link">Download</a>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</div>