<template>
  <nav class="nav">
    <div class="nav-title">
      <h1 class="blog-title">
        <router-link :to="{ name: 'Home' }">6 Blog</router-link>
      </h1>
    </div>
    <div class="nav-buttons">
      <ul>
        <li>
          <router-link :to="{ name: 'Home' }">Home</router-link>
        </li>
        <li class="writeBtn" @click="newEntry()">Write</li>
        <li v-if="!$store.state.loggedin">
          <router-link :to="{ name: 'Login' }">Sign in</router-link>
        </li>
        <li v-if="$store.state.loggedin" @click="signOut()" id="sign-out-btn">
          Sign out
        </li>
      </ul>
    </div>
  </nav>
</template>
<script>
export default {
  name: "Navbar",
  data() {
    return {};
  },

  created() {},
  methods: {
    signOut() {
      const path = "http://127.0.0.1:5000/login";
      this.$http
        .delete(path, {})
        .then((response) => {
          console.log(response);
          this.$store.commit("logout");
          this.$toasted.success("Successfully logged out");
          this.$router.push({ name: "Home" });
        })
        .catch((error) => {
          if (error.response) {
            if (error.response.status == 401 || error.response.status == 400) {
              this.$store.commit("logout");
              this.$toasted.show("Logged out");
              this.$router.push({ name: "Home" });
            }
            console.log(error.response);
          }
        });
    },
    newEntry() {
      const path = "http://127.0.0.1:5000/newentry";

      this.$http
        .get(path, {})
        .then((response) => {
          if (response.status == 200) {
            this.$router.push({ name: "NewEntry" });
          }
        })
        .catch((error) => {
          if (error.response) {
            let errCode = error.response.status;
            let isLoggedin = this.$store.state.loggedin;
            if (errCode == 422) {
              this.$toasted.error("You must login to write");
              console.log(error.response.data);
            } else if (errCode == 403) {
              this.$toasted.error("Your usertype is not allowed to write");
            } else if (errCode == 401 && isLoggedin) {
              this.$toasted.error("Session timed out. Please login again");
            } else if (errCode == 401 && !isLoggedin) {
              this.$toasted.error("You must login to write");
            }
          }
          /* show error and refresh page */
        });
    },
  },
};
</script>
<style>
nav {
  display: flex;
  width: 55%;
  justify-content: space-between;
  align-content: center;
  margin: 0 auto;
  margin-top: 5rem;
  margin-bottom: 2rem;
  border-bottom: 4px solid var(--yellow);
}
.nav-title,
.nav-buttons {
  margin: 0;
  padding: 0;
}
.nav-buttons ul,
.nav-buttons li > a {
  display: flex;
  list-style-type: none;
  color: var(--pink);
  margin: 0;
}
.nav-buttons li {
  margin: 15px;
  margin-top: 0;
}

.blog-title {
  margin: 0;
}
.blog-title a {
  color: var(--green);
}
#sign-out-btn,
.writeBtn {
  cursor: pointer;
}
@media only screen and (max-width: 600px) {
  nav {
    margin-top: 1rem;
    width: 90%;
  }
}
</style>
