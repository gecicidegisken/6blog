<template>
  <div class="new-entry">
    <navbar />
    <h3 class="new-entry-title">Write a post</h3>
    <div class="entry-form">
      <form>
        <div class="form-input">
          <label for="title">Title </label>
          <input
            v-model="title"
            name="title"
            type="text"
            :maxlength="this.maxTitleLen"
            @input="titleEnter"
          />
        </div>
        <div class="form-input">
          <label for="content">Content </label>
          <textarea v-model="content" name="content" />
        </div>
        <div class="form-input">
          <input
            class="postBtn"
            @click="postEntry()"
            type="button"
            value="Post"
          />
        </div>
      </form>
    </div>
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
      maxTitleLen: 40,
    };
  },
  methods: {
    postEntry() {
      const path = "http://127.0.0.1:5000/entries";

      this.$http
        .post(
          path,
          {
            title: this.title,
            content: this.content,
          },
          {}
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
            if (errCode == 401) {
              this.$toasted.error("Session timed out. Login again to post");
            } else if (errCode == 403) {
              console.log("This usertype can't write");
            }
          }
        });
    },
    titleEnter(event) {
      const text = event.target.value;
      if (String(text).length >= this.maxTitleLen) {
        this.$toasted.success(
          `Title length cannot be more than ${this.maxTitleLen} charachters`
        );
      }
    },
  },
};
</script>
<style>
.new-entry {
  display: flex;
  flex-direction: column;
  margin: 0 auto;
}
.new-entry-title {
  color: var(--green);
  margin: 0 auto;
}
.entry-form {
  margin: 0 auto;
}
.postBtn {
  color: var(--pink);
  cursor: pointer;
  border: none !important;
  text-decoration: underline var(--yellow);
  font-size: 1.5rem;
  font-weight: 600;
}
.entry-form form {
  display: flex;
  flex-direction: column;
}
.entry-form .form-input {
  display: flex;
  flex-direction: column;
}
.entry-form .form-input textarea {
  width: 500px;
  height: 500px;
  border: 1px solid var(--green);
}
.entry-form .form-input input {
  height: 30px;
  border: 1px solid var(--green);
}
.entry-form .form-input label {
  color: var(--blue);
  margin-bottom: 10px;
}
</style>
