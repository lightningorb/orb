<script>
  import { Router, Route } from "svelte-routing";

  import Layout from "./routes/Layout.svelte";
  import Login from "./routes/login.svelte";
  import Signup from "./routes/signup.svelte";
  import Password_forgot from "./routes/password_forgot.svelte";
  import Dev_license from "./routes/dev_license.svelte";
  import Download from "./routes/download.svelte";
  import PrivacyPolicy from "./routes/PrivacyPolicy.svelte";
  import TermsAndConditions from "./routes/TermsAndConditions.svelte";
  import Buy from "./routes/Buy.svelte";
  import License from "./routes/License.svelte";
  import EvalLicense from "./routes/EvalLicense.svelte";
  import FOSS from "./routes/FOSS.svelte";
  import InvestorRelations from "./routes/investor_relations.svelte";
  import Security from "./routes/security.svelte";
  import Advertise from "./routes/advertise.svelte";
  import ReleaseNotes from "./routes/release_notes.svelte";
  import HireMe from "./routes/hireMe.svelte";
  import Love from "./routes/love.svelte";

  export let url = "";
</script>

<Router {url}>
  <div>
    <Route path="/"><Layout /></Route>
    <Route path="/login"><Login /></Route>
    <Route path="/signup"><Signup /></Route>
    <Route path="/password_forgot"><Password_forgot /></Route>
    <Route path="/dev-license"><Dev_license /></Route>
    <Route path="/download"><Download /></Route>
    <Route path="/privacy"><PrivacyPolicy /></Route>
    <Route path="/foss"><FOSS /></Route>
    <Route path="/terms-and-conditions"><TermsAndConditions /></Route>
    <Route path="/buy"><Buy /></Route>
    <Route path="/license"><License /></Route>
    <Route path="/evaluate"><EvalLicense /></Route>
    <Route path="/investor-relations"><InvestorRelations /></Route>
    <Route path="/security"><Security /></Route>
    <Route path="/advertise"><Advertise /></Route>
    <Route path="/release-notes"><ReleaseNotes /></Route>
    <Route path="/hire-me"><HireMe /></Route>
    <Route path="/love"><Love /></Route>
  </div>
</Router>

