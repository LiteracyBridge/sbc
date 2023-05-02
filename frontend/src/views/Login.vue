<script setup>
// Importing required AWS Amplify libraries and components
import { Authenticator } from "@aws-amplify/ui-vue";
import "@aws-amplify/ui-vue/styles.css";
import { Amplify, Auth } from 'aws-amplify';
import awsconfig from '../aws-exports';
import { useUserStore } from '@/stores/user';

// Configure AWS Amplify with the provided configuration
Amplify.configure(awsconfig);

// Initialize the user store
const userStore = useUserStore();
  
// Logout function to clear user data from the store and sign out
function logout (ampSignOut) {
    userStore.setUser();
    ampSignOut();
}
</script>

<template>
  <!-- Display the AWS Amplify Authenticator component -->
  <authenticator>
    <!-- Slot for custom content inside the authenticator component -->
    <template v-slot="{ user, signOut }">
      <!-- Display sign out button and bind the signOut function -->
      <button @click="signOut">Sign Out</button>
    </template>
  </authenticator>
</template>
