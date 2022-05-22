import Vue from "vue";
import Vuex from "vuex";
import createPersistedState from "vuex-persistedstate";

Vue.use(Vuex);

const store = new Vuex.Store({
  state: {
    loggedin: 0,
    access_token: "",
    downvotes: 0,
    upvotes: 0,
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
    getVotes(state, vote) {
      state.upvotes = vote.up;
      state.downvotes = vote.down;
    },
    setVotes(state, vote) {
      if (vote == true) {
        state.upvotes += 1;
      } else if (vote == false) {
        state.downvotes += 1;
      }
    },
    updateVotes(state, vote) {
      if (vote == true) {
        state.upvotes += 1;
        state.downvotes -= 1;
      } else if (vote == false) {
        state.downvotes += 1;
        state.upvotes -= 1;
      }
    },
  },
  plugins: [createPersistedState()],
});

export default store;
