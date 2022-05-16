<template>
  <div class="login">
    <navbar />
    <h3 class="login-title">Login to your account</h3>
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
          <input
            class="loginBtn"
            @click="postCredentials()"
            type="button"
            value="Login"
          />
        </div>
      </form>
    </div>
    <br />
    <div class="register">
      <p>Don't you have an account?</p>
      <a class="registerBtn" href="/register">Create one!</a>
    </div>
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
.login {
  display: flex;
  flex-direction: column;
}
.form-input {
  margin: 15px;
  background-color: white;
}
.form-input input {
  background-color: white !important;
  border-radius: 5px;
}

.login-title {
  color: var(--green) !important;
  margin: 0 auto;
}
.login-form {
  display: flex;
  flex-direction: column;
  margin: 0 auto;
}
.loginBtn {
  text-decoration: underline var(--yellow);
  border: none;
  /* border-bottom: 3px solid var(--yellow); */
  background-color: transparent;
  text-align: center;
  font-weight: 600;
  color: var(--pink);
  cursor: pointer;
  font-size: 1.3rem;
  margin: 0 auto;
  align-items: center !important;
}
.register {
  margin: 0 auto;
}
.registerBtn {
  color: var(--pink);
  font-weight: 600;
}
</style>
