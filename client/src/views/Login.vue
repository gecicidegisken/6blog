<template>
  <div class="login">
    <navbar />
    <div class="login-form">
      <form>
        <div class="form-input">
          <label for="username">Username </label>
          <input v-model="username" type="text" name="username" />
        </div>
        <div class="form-input">
          <label for="password">Password </label>
          <input v-model="password" type="password" name="password" />
        </div>
        <div class="form-input">
          <input @click="postCredentials()" type="button" value="Login" />
        </div>
      </form>
    </div>
    <br />
    <p>Don't you have an account?</p>
    <a href="/register">Create one!</a>
  </div>
</template>

<script>
import axios from "axios";
// import router from "vue-router";
import Navbar from "../components/Navbar.vue";
export default {
  name: "Login",
  components: {
    Navbar,
  },
  data() {
    return {
      username: "",
      password: "",
    };
  },
  methods: {
    postCredentials() {
      const path = "http://127.0.0.1:5000/login";
      // let self = this;
      axios
        .post(path, {
          username: this.username,
          password: this.password,
        })
        .then((response) => {
          /* burada anasayfaya git */
          sessionStorage.setItem("access_token", response.data.access_token);
          console.log(response.data.access_token);
          // window.location.href = "/";
          this.$router.push({ name: "Home" });
        })
        .catch(function (error) {
          console.log(error.response.data);
          /* show error and refresh page */
        });
    },
  },
};
</script>

<style>
.form-input {
  margin: 15px;
}
</style>
