import { createPinia } from 'pinia';
import axios from 'axios';
import VueAxios from 'vue-axios';
import router from './router';
import { Amplify } from 'aws-amplify';
import awsconfig from './aws-exports';
import { createApp } from 'vue';
import App from './App.vue';

Amplify.configure(awsconfig);
    

const app = createApp(App)
    .use(createPinia())
    .use(router)
    .use(VueAxios, axios)
    // .use(AmplifyVue)

app.provide("axios", app.config.globalProperties.axios)
app.mount('#app')
