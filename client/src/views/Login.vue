<template>
  <div class="login">
    <navbar />
    <h3 class="title">Login</h3>
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
import Navbar from "../components/Navbar.vue";
// import store from "vuex";
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
      this.$http
        .post(path, {
          username: this.username,
          password: this.password,
        })
        .then((response) => {
          console.log(response.data.status);
          // localStorage.setItem("access_token", response.data.access_token);
          this.$store.commit("login", response.data.access_token);
          this.$toasted.success("Successfully logged in");
          this.$router.push({ name: "Home" });
        })
        .catch((error) => {
          if (error.response) {
            console.log(error.response.data);
            if (error.response.status == 400) {
              this.$toasted.error("Username/password incorrect.");
            }
          }
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
