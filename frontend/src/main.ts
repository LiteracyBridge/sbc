// Importing required libraries and components
import { createApp } from "vue";
import App from "./App.vue";
import { createPinia } from "pinia";
import axios from "axios";
import VueAxios from "vue-axios";
import router from "./router";
import { Amplify } from "aws-amplify";
import awsconfig from "./aws-exports";
import { initializeApp } from "firebase/app";
import { getAnalytics, initializeAnalytics } from "firebase/analytics";

// import mermaidDirective from "./directives/mermaid";

// Ant Design imports
import { message } from "ant-design-vue";
import "./theme.less";
import { config } from "./models/constants";

// Configure AWS Amplify with the provided configuration
Amplify.configure({
  ...awsconfig,
});

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {};

// Initialize Firebase
initializeAnalytics(initializeApp(config.firebase));

// Create a new Vue app with the App component
const app = createApp(App);

app
  .use(createPinia()) // Use the Pinia store management library
  .use(VueAxios, axios) // Use axios for handling HTTP requests
  .use(router);

// Register the mermaid directive
// app.directive("mermaid", mermaidDirective);

// Provide axios instance globally
app.provide("axios", app.config.globalProperties.axios);

// Mount the app on the DOM element with the ID 'app'
app.mount("#app");

app.config.globalProperties.$message = message;
