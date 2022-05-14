<template>
  <div class="entry-view">
    <navbar />
    <div class="entry">
      <h2 v-if="!entry.title">LOADING</h2>
      <h2 class="entry-title">{{ entry.title }}</h2>
      <p class="entry-content">{{ entry.content }}</p>
      <p class="entry-author" v-if="entry.author">
        Author: {{ entry.author.username }}
      </p>
      <p class="entry-date" v-if="entry.date">
        Date: {{ convertDate(entry.date) }}
      </p>
      <div v-if="entry.date" class="vote">
        <p class="up">Upvotes: {{ $store.state.upvotes }}</p>
        <p class="down">Downvotes: {{ $store.state.downvotes }}</p>
      </div>
      <div v-if="entry.date && $store.state.loggedin" class="voteButtons">
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
      entry: {},
    };
  },
  created() {
    let entryid = this.$route.params.entryid;
    const path = "http://127.0.0.1:5000/entries/" + entryid;
    this.$http
      .get(path)
      .then((response) => {
        this.entry = response.data;
        let votes = {
          up: response.data.upvotes,
          down: response.data.downvotes,
        };

        this.$store.commit("getVotes", votes);
      })
      .catch((error) => {
        if (error.response) {
          if (error.response.status == 404) {
            this.$toasted.error("Entry is not found. It may be deleted.");
          } else {
            this.$toasted.error("Something went wrong");
          }
        }
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
          let resCode = response.status;
          if (resCode == 200) {
            this.$toasted.success("Successfully voted");
            this.$store.commit("setVotes", vote);
          } else if (resCode == 210) {
            this.$toasted.success("Successfully updated vote");
            this.$store.commit("updateVotes", vote);
          }
        })
        .catch((error) => {
          if (error.response) {
            let errCode = error.response.status;
            console.log(error.toJSON());

            if (errCode == 403) {
              this.$toasted.error("You've already voted this content");
            } else if (errCode == 401) {
              this.$toasted.error("Session timed out. Please login again");
            } else if (errCode == 422 || errCode == 405) {
              this.$toasted.error("You must login to vote this content");
            }
          }
        });
    },
  },
};
</script>
