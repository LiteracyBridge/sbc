<script setup>
import { RouterLink, RouterView } from 'vue-router'
import { useLookupStore } from './stores/lookups.js'
import NavBar from '@/components/Layout/NavBar.vue'
import { onMounted } from 'vue'
import { Authenticator } from "@aws-amplify/ui-vue";
import "@aws-amplify/ui-vue/styles.css";
import { Amplify, Auth } from 'aws-amplify';
import awsconfig from './aws-exports';
import { useUserStore } from '@/stores/user'

Amplify.configure(awsconfig);
const lookupStore = useLookupStore();

// async function isUserSignedIn() {
//     try {
//         const userObj = await Auth.currentAuthenticatedUser();
//         useUserStore().setUser(userObj['attributes']['email'],userObj['signInUserSession']['accessToken']['jwtToken']);
//         // this.$router.push({ path: '/drivers'})
//         }
//     catch (err) {
//         useUserStore().setUser();
//         console.log(err);
//     }
// };

// onMounted(() => isUserSignedIn());


onMounted(() => {
  lookupStore.download();
  // isUserSignedIn();
})
</script>





<template>
  <NavBar />
  <!-- <authenticator>
    <template v-slot="{ user, signOut }">
      <h1>Hello {{ user.attributes.email }} {{user.signInUserSession.accessToken.jwtToken}}</h1>
      <button @click="signOut">Sign Out</button>
    </template>
  </authenticator> -->
  <div class="container is-max-desktop px-2 py-4">
    <RouterView />
  </div>
</template>




<!--


  <authenticator>
    <template v-slot="{ user, signOut }">
      <h1>Hello {{ user.username }}!</h1>
      <button @click="signOut">Sign Out</button>
    </template>
  </authenticator>





<template>
  <header>
    <div class="wrapper">
      <nav>
        <RouterLink to="/">Home</RouterLink>
      </nav>
    </div>
  </header>
</template>
-->

<style>
@import 'bulma/css/bulma.min.css';
@import 'bulma/css/bulma-tooltip.min.css'
</style>
