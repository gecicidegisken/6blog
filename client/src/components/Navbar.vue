<template>
  <div class="nav">
    <h1>6 Blog</h1>
    <ul>
      <li><a href="/">Home</a></li>
      <li>
        <a href="/login">{{ userOption }}</a>
      </li>
      <li>
        <a href="/new-entry">{{ writingOption }}</a>
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
      userOption: "",
      writingOption: "",
    };
  },

  created() {
    if (access_token) {
      this.userOption = "Sign out";
      // sessionStorage.removeItem("token");
      this.writingOption = "Write a post";
    } else {
      this.userOption = "Sign in";
    }
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
</style>
