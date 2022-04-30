<template>
  <div class="home">
    <navbar />
    <entries />
  </div>
</template>

<script>
// @ is an alias to /src
// import HelloWorld from "@/components/HelloWorld.vue";

import Entries from "../components/Entries.vue";
import Navbar from "../components/Navbar.vue";

export default {
  name: "Home",
  components: {
    Entries,
    Navbar,
  },
};
</script>

<style>
.home {
  display: flex;
  flex-direction: column;
  justify-content: center;
}
</style>
