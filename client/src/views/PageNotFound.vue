<template>
  <div>
    <Navbar></Navbar>
    <p class="not-found">The page you're looking for is not found.</p>
  </div>
</template>
<script>
import Navbar from "../components/Navbar.vue";
export default {
  name: "PageNotFound",
  components: {
    Navbar,
  },
};
</script>
<style>
.not-found {
  text-align: center;
}
</style>
