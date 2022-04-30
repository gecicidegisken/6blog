<template>
  <div class="register">
    <navbar />
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
import axios from "axios";
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
      axios
        .post(path, {
          username: this.username,
          password: this.password,
          usertype: this.usertype,
        })
        .then(function (response) {
          console.log(response.data, "200");
          //   buradan anasayfaya git
        })
        .catch(function (error) {
          console.log(error);
        });
    },
  },
};
</script>
