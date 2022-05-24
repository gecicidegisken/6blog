import axios from "axios";
import store from "../store";

const mainaxios = axios.create({
  baseURL: "http://127.0.0.1:5000/",
  timeout: 10000,
});

mainaxios.interceptors.request.use(function (config) {
  let access_token = store.getters.getAccessToken;

  if (access_token) {
    config.headers.Authorization = `Bearer ${access_token}`;
  }
  return config;
});

export { mainaxios };
