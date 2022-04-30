<template>
  <div class="nav">
    <h1>6 Blog</h1>
    <ul>
      <li>
        <router-link :to="{ name: 'Home' }">Home</router-link>
      </li>
      <li v-if="!signed">
        <router-link :to="{ name: 'Login' }">Sign in</router-link>
      </li>
      <li v-if="signed" @click="signOut()" id="sign-out-btn">Sign out</li>
      <li v-if="signed">
        <router-link :to="{ name: 'NewEntry' }">Write</router-link>
      </li>
    </ul>
  </div>
</template>
<script>
import axios from "axios";
let access_token = sessionStorage.getItem("access_token");
axios.defaults.headers.common["Authorization"] = `Bearer ${access_token}`;
export default {
  name: "Navbar",
  data() {
    return {
      signed: Boolean,
      writingOption: "",
    };
  },

  created() {
    if (access_token) {
      this.signed = true;
    } else {
      this.signed = false;
    }
  },
  methods: {
    signOut() {
      sessionStorage.removeItem("access_token");
      location.reload();
    },
  },
};
</script>
<style>
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
</style>
