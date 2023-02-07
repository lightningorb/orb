<script>
  import { Router, Route } from "svelte-routing";

  import Layout from "./routes/Layout.svelte";
  import Login from "./routes/login.svelte";
  import Download from "./routes/download.svelte";
  import PrivacyPolicy from "./routes/PrivacyPolicy.svelte";
  import TermsAndConditions from "./routes/TermsAndConditions.svelte";
  import Security from "./routes/security.svelte";
  import ReleaseNotes from "./routes/release_notes.svelte";
  import Love from "./routes/love.svelte";

  export let url = "";
</script>

<Router {url}>
  <div>
    <Route path="/"><Layout /></Route>
    <Route path="/download"><Download /></Route>
    <Route path="/privacy"><PrivacyPolicy /></Route>
    <Route path="/terms-and-conditions"><TermsAndConditions /></Route>
    <Route path="/security"><Security /></Route>
    <Route path="/release-notes"><ReleaseNotes /></Route>
    <Route path="/love"><Love /></Route>
  </div>
</Router>

