// Importing required libraries and components
import { createApp } from 'vue';
import App from './App.vue';
import { createPinia } from 'pinia';
import axios from 'axios';
import VueAxios from 'vue-axios';
import router from './router';
import { Amplify } from 'aws-amplify';
import awsconfig from './aws-exports';
import mermaidDirective from './directives/mermaid';

// Configure AWS Amplify with the provided configuration
Amplify.configure(awsconfig);

// Create a new Vue app with the App component
const app = createApp(App)
    .use(createPinia()) // Use the Pinia store management library
    .use(VueAxios, axios) // Use axios for handling HTTP requests
    .use(router); // Use the defined Vue router

// Register the mermaid directive
app.directive('mermaid', mermaidDirective);

// Provide axios instance globally
app.provide("axios", app.config.globalProperties.axios);

// Mount the app on the DOM element with the ID 'app'
app.mount('#app');
