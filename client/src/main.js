import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import Toasted from "vue-toasted";
import axios from "axios";

Vue.config.productionTip = false;
Vue.use(Toasted, {
  duration: 1500,
  position: "bottom-center",
  theme: "bubble",
  iconPack: "fontawesome",
});

Vue.prototype.$http = axios;

new Vue({
  router,
  store,
  render: (h) => h(App),
}).$mount("#app");
