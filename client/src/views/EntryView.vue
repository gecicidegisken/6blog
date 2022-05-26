<template>
  <div class="entry-view">
    <navbar />
    <div class="entry">
      <h2 class="loading" v-if="!entry.title"></h2>

      <h2 class="entry-title">{{ entry.title }}</h2>
      <div class="entry-metadata">
        <p class="entry-date" v-if="entry.date">
          {{ convertDate(entry.date) }}&nbsp; • &nbsp;
        </p>
        <p class="entry-author" v-if="entry.author">
          by <span class="author-username">{{ entry.author.username }}</span>
        </p>
      </div>
      <p class="entry-content">{{ entry.content }}</p>
      <hr class="hr" />

      <div v-if="entry.date" class="voteButtons">
        <button class="voteBtn" @click="voteEntry(true)">
          {{ $store.state.upvotes }} ↑
        </button>
        <button class="voteBtn" @click="voteEntry(false)">
          {{ $store.state.downvotes }}↓
        </button>
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
            setTimeout(() => {
              this.$router.push({ name: "Home" });
            }, 2000);
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
      let entryid = this.$route.params.entryid;
      const path = "http://127.0.0.1:5000/entries/" + entryid;
      let voteData = { votetype: vote };

      this.$http
        .post(path, null, {
          params: voteData,
        })
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
            let isLoggedin = this.$store.state.loggedin;

            if (errCode == 403) {
              this.$toasted.error("You've already voted this content");
            } else if (errCode == 401 && isLoggedin) {
              this.$toasted.error("Session timed out. Please login again");
            } else if (errCode == 401 && !isLoggedin) {
              this.$toasted.error("You must login to write");
            }
          }
        });
    },
  },
};
</script>
<style>
button:disabled {
  color: gray;
  border: 1px solid gray;
  cursor: not-allowed;
}
hr.hr {
  border: 1px solid var(--yellow);
  width: 100%;
}
.loading {
  margin: 0 auto;
  border: 10px solid #f3f3f3;
  border-radius: 50%;
  border-top: 10px solid var(--pink);
  width: 50px;
  height: 50px;
  -webkit-animation: spin 2s linear infinite; /* Safari */
  animation: spin 2s linear infinite;
}
.entry-view .entry {
  width: 50%;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
}
.entry-view .entry .entry-title {
  color: var(--blue);
  margin-bottom: 0px;
}
.entry-view .entry-metadata {
  display: flex;
  font-size: 13px;
  margin-top: 0px;
}
.entry-metadata .author-username {
  color: var(--pink);
}
.voteButtons {
  margin: 0 auto;
}
.voteBtn {
  border-radius: 50%;
  background-color: transparent;
  border: 1px solid var(--green);
  padding: 10px;
  cursor: pointer;
  margin: 15px;
  font-weight: 500;
}

@media only screen and (max-width: 600px) {
  .entry-view .entry {
    width: 90%;
    margin: 0 auto;
  }
}
@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
</style>
