<template>
  <div class="new-entry">
    <navbar />
    <h3 class="title">Write a post</h3>
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
    <p v-if="$store.state.loggedin" class="errMsg">{{ errMsg }}</p>
  </div>
</template>

<script>
import Navbar from "../components/Navbar.vue";

export default {
  name: "NewEntry",
  components: {
    Navbar,
  },
  data() {
    return {
      title: "",
      content: "",
      errMsg: "",
    };
  },
  methods: {
    postEntry() {
      let access_token = this.$store.state.access_token;
      const path = "http://127.0.0.1:5000/entries";
      this.$http
        .post(
          path,
          {
            title: this.title,
            content: this.content,
          },
          {
            headers: {
              Authorization: "Bearer " + access_token,
            },
          }
        )
        .then((response) => {
          if (response.status == 200) {
            this.$toasted.success("Successfully posted");
            this.$router.push({ name: "Home" });
          }
        })
        .catch((error) => {
          if (error.response) {
            let errCode = error.response.status;
            if (errCode == 401 || errCode == 405) {
              this.errMsg =
                "Oturum süresi dolmuş, yazı yazmak için giriş yapmalısınız.";
            } else if (errCode == 403) {
              console.log("bu kullanıcı tipi yazı yazamaz");
            }
          }
          /* show error and refresh page */
        });
    },
  },
};
</script>
