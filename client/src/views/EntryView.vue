<template>
  <div class="entry-view">
    <navbar />
    <div class="entry">
      <h2 class="entry-title">{{ e.title }}</h2>
      <p class="entry-content">{{ e.content }}</p>
      <p class="entry-author" v-if="e.author">
        Author: {{ e.author.username }}
      </p>
      <p class="entry-date" v-if="e.date">Date: {{ convertDate(e.date) }}</p>
      <p class="up">Upvotes: {{ e.upvotes }}</p>
      <p class="down">Downvotes: {{ e.downvotes }}</p>

      <div class="voteButtons">
        <button @click="voteEntry(true)">Upvote</button>
        <button @click="voteEntry(false)">Downvote</button>
      </div>
    </div>
  </div>
</template>
<script>
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
    this.$http
      .get(path)
      .then((res) => {
        this.e = res.data;
        console.log(res.data.upvotes);
        console.log(res.data.downvotes);
      })
      .catch((error) => {
        console.error(error);
      });
  },
  methods: {
    convertDate(seconds) {
      var date = new Date(seconds * 1000).toLocaleDateString("en-GB");
      return date;
    },

    voteEntry(vote) {
      let access_token = this.$store.state.access_token;
      let entryid = this.$route.params.entryid;
      const path = "http://127.0.0.1:5000/entries/" + entryid;
      this.$http
        .put(
          path,
          { votetype: vote },
          {
            headers: {
              Authorization: "Bearer " + access_token,
            },
          }
        )
        .then((response) => {
          console.log(response.data);
          location.reload();
        })
        .catch((error) => {
          let errCode = error.response.status;
          this.voteErr = true;
          if (errCode == 403) {
            this.$toasted.error("You've already voted this content");
          } else if (errCode == 401 || errCode == 405) {
            this.$toasted.error("You must login to vote this content");
          }
        });
    },
  },
};
</script>
