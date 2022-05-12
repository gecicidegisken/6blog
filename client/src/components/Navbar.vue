<template>
  <div class="nav">
    <h1>6 Blog</h1>
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
      let access_token = this.$store.state.access_token;
      const path = "http://127.0.0.1:5000/login";
      this.$http
        .delete(path, {
          headers: {
            Authorization: "Bearer " + access_token,
          },
        })
        .then((response) => {
          console.log(response);
          this.$store.commit("logout");
          this.$toasted.success("Successfully logged out");
          this.$router.push({ name: "Home" });
        })
        .catch((error) => {
          if (error.response) {
            console.log(error.response);
          }
        });
    },
    newEntry() {
      let access_token = this.$store.state.access_token;
      const path = "http://127.0.0.1:5000/newentry";

      this.$http
        .get(path, {
          headers: {
            Authorization: "Bearer " + access_token,
          },
        })
        .then((response) => {
          if (response.status == 200) {
            this.$router.push({ name: "NewEntry" });
          }
        })
        .catch((error) => {
          if (error.response) {
            let errCode = error.response.status;
            if (errCode == 401 || errCode == 422) {
              this.$toasted.error("You must login to write");
              console.log(error.response.data);
            } else if (errCode == 403) {
              this.$toasted.error("Your usertype is not allowed to write");
            } else if (errCode == 405) {
              console.log("Session timed out. Login again");
            }
          }
          /* show error and refresh page */
        });
    },
  },
};
</script>
<style>
a {
  color: black;
}
ul {
  display: flex;
  justify-content: center;
  list-style-type: none;
  border-bottom: 2px solid;
  padding-left: 0;
}
li {
  margin: 15px;
}
a {
  text-decoration: none;
}
#sign-out-btn {
  cursor: pointer;
}
.writeBtn {
  cursor: pointer;
}
</style>
