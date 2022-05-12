import Vue from "vue";
import Vuex from "vuex";
import createPersistedState from "vuex-persistedstate";

Vue.use(Vuex);

const store = new Vuex.Store({
  state: {
    loggedin: 0,
    access_token: "",
  },
  mutations: {
    login(state, access_token) {
      state.loggedin = 1;
      state.access_token = access_token;
    },
    logout(state) {
      state.loggedin = 0;
      state.access_token = "";
    },
  },
  plugins: [createPersistedState()],
});

export default store;
