<template>
  <div class="register">
    <navbar />
    <h3 class="title">Register</h3>
    <div class="register-form">
      <div class="form-input">
        <label for="username">Username </label>
        <input v-model="username" type="text" name="username" />
      </div>
      <div class="form-input">
        <label for="password">Password </label>
        <input v-model="password" type="password" name="password" />
      </div>
      <div class="form-input">
        <label for="usertype">Usertype</label>
        <input
          v-model="usertype"
          type="radio"
          name="usertype"
          value="1"
          id="writer"
        />
        <label for="writer">Writer </label>
        <input
          v-model="usertype"
          type="radio"
          name="usertype"
          value="0"
          id="reader"
        />
        <label for="reader">Reader</label>
      </div>
      <div class="form-input">
        <input @click="postCredentials()" type="button" value="Sign up" />
      </div>
    </div>
    <br />
    <p>Do you already have an account?</p>
    <a href="/login">Sign in!</a>
  </div>
</template>

<script>
import Navbar from "../components/Navbar.vue";

export default {
  name: "Register",
  components: {
    Navbar,
  },
  data() {
    return {
      username: "",
      password: "",
      usertype: Boolean,
    };
  },
  methods: {
    postCredentials() {
      const path = "http://127.0.0.1:5000/register";
      this.$http
        .post(path, {
          username: this.username,
          password: this.password,
          usertype: this.usertype,
        })
        .then((response) => {
          console.log(response);
          this.$toasted.success("Successfully created an account!");
          this.$router.push({ name: "Login" });
        })
        .catch((error) => {
          if (error.response) {
            let errCode = error.response.status;
            if (errCode == 400) {
              this.$toasted.error("Username is not available");
            } else if (errCode == 405) {
              this.$toasted.error("Please fill out every blank in the form");
            }
          }

          console.log(error);
        });
    },
  },
};
</script>
