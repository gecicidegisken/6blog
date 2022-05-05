<template>
  <div class="new-entry">
    <navbar />
    <div class="entry-form">
      <form>
        <div class="form-input">
          <label for="title">Title </label>
          <input v-model="title" type="textarea" name="title" />
        </div>
        <div class="form-input">
          <label for="content">Content </label>
          <input v-model="content" type="textarea" name="content" />
        </div>
        <div class="form-input">
          <input @click="postEntry()" type="button" value="Post" />
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import Navbar from "../components/Navbar.vue";
let access_token = sessionStorage.getItem("access_token");
axios.defaults.headers.common["Authorization"] = `Bearer ${access_token}`;
export default {
  name: "NewEntry",
  components: {
    Navbar,
  },
  data() {
    return {
      title: "",
      content: "",
    };
  },
  methods: {
    postEntry() {
      const path = "http://127.0.0.1:5000/entries";

      axios
        .post(path, {
          title: this.title,
          content: this.content,
        })
        .then((response) => {
          if (response.status == 200) {
            /* burada yayınlandı mesajı verip anasayfaya git */
            console.log("yayinlandı");
            this.$router.push({ name: "Home" });
          }
        })
        .catch(function (error) {
          if (error.response.status == 401) {
            console.log("giriş yapılmalı");
          } else if (error.response.status == 403) {
            console.log("bu kullanıcı tipi yazı yazamaz");
          }
          /* show error and refresh page */
        });
    },
  },
};
</script>
