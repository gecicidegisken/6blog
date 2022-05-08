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

      <div v-if="isLogin" class="voteButtons">
        <button @click="voteEntry(true)">Upvote</button>
        <button @click="voteEntry(false)">Downvote</button>
      </div>
      <p v-if="voteErr">{{ errorMsg }}</p>
    </div>
  </div>
</template>
<script>
import axios from "axios";
import Navbar from "../components/Navbar.vue";
let access_token = sessionStorage.getItem("access_token");
axios.defaults.headers.common["Authorization"] = `Bearer ${access_token}`;
export default {
  name: "EntryView",
  components: {
    Navbar,
  },
  data() {
    return {
      e: {},
      voteErr: false,
      errorMsg: "",
      isLogin: false,
    };
  },
  created() {
    if (access_token != null) {
      this.isLogin = true;
    } else {
      this.isLogin = false;
    }
    let entryid = this.$route.params.entryid;
    const path = "http://127.0.0.1:5000/entries/" + entryid;
    axios
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
      let entryid = this.$route.params.entryid;
      const path = "http://127.0.0.1:5000/entries/" + entryid;
      axios
        .put(path, { votetype: vote })
        .then((response) => {
          console.log(response.data);
          location.reload();
        })
        .catch((error) => {
          console.log(error.response.data);
          this.voteErr = true;
          if (error.response.status == 403) {
            this.errorMsg = "You already voted this content";
          } else if (error.response.status == 401) {
            this.errorMsg = "You must login to vote this content";
          }
        });
    },
  },
};
</script>
