import axios from "axios";
import store from "../store";

const mainaxios = axios.create({
  baseURL: "http://127.0.0.1:5000/",
});

mainaxios.interceptors.request.use(function (config) {
  let access_token = store.getters.getAccessToken;
  console.log(access_token);
  if (access_token) {
    config.headers.Authorization = `Bearer ${access_token}`;
  }
  return config;
});

export { mainaxios };
