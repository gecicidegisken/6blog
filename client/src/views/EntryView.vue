<template>
  <div class="entry-view">
    <navbar />
    <div class="entry">
      <h2 class="entry-title">{{ e.title }}</h2>
      <p class="entry-content">{{ e.content }}</p>
    </div>
  </div>
</template>
<script>
import axios from "axios";
import Navbar from "../components/Navbar.vue";
export default {
  name: "EntryView",
  components: {
    Navbar,
  },
  data() {
    return {
      e: {},
    };
  },
  created() {
    let entryid = this.$route.params.entryid;

    const path = "http://127.0.0.1:5000/entries/" + entryid;
    axios
      .get(path)
      .then((res) => {
        this.e = res.data;
      })
      .catch((error) => {
        console.error(error);
      });
  },
};
</script>
