<script setup>
import { Authenticator } from "@aws-amplify/ui-vue";
import "@aws-amplify/ui-vue/styles.css";
import { Amplify, Auth } from 'aws-amplify';
import awsconfig from '../aws-exports';
import { onMounted } from 'vue';
import { useUserStore } from '@/stores/user'

Amplify.configure(awsconfig);
const userStore = useUserStore();
  
// async function isUserSignedIn() {
//     try {
//         const userObj = await Auth.currentAuthenticatedUser();
//         userStore.setUser(userObj['attributes']['email'],userObj['signInUserSession']['accessToken']['jwtToken']);
//         // this.$router.push({ path: '/drivers'})
//         }
//     catch (err) {
//         userStore.setUser();
//         console.log(err);
//     }
// };

// onMounted(() => isUserSignedIn());

function logout (ampSignOut) {
    userStore.setUser();
    ampSignOut();
}
</script>

<template>
  <!-- <authenticator :social-providers="['amazon', 'apple', 'facebook', 'google']"> -->
  <authenticator>
    <template v-slot="{ user, signOut }">
      <button @click="signOut">Sign Out</button>
    </template>
  </authenticator>
</template>
<!--
<h1>Hello {{ user.attributes.email }} {{user.signInUserSession.accessToken.jwtToken}}</h1>
-->