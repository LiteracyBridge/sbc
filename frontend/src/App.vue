<script setup>
// Importing required Vue and external libraries
import { onMounted, computed } from "vue";
import { RouterView } from "vue-router";
import { useLookupStore } from "./stores/lookups";
import NavBar from "@/components/Layout/NavBar.vue";
import LeftSideNav from "@/components/Layout/LeftSideNav.vue";
import "@aws-amplify/ui-vue/styles.css";
import { Amplify } from "aws-amplify";
import awsconfig from "./aws-exports";
import { useSideNavStore } from "@/stores/sideNav";
import { useUserStore } from '@/stores/user';

const userStore = useUserStore();

// Set ONLINE to true when connected to the internet or false when offline
const ONLINE = true;

// Initialize the lookup store and side navigation store
const lookupStore = useLookupStore();
const sideNavStore = useSideNavStore();

// Computed property for determining if the side navigation should be visible
const showSideNav = computed(() => sideNavStore.visible);

// Configure AWS Amplify with the provided configuration
// Amplify.configure(awsconfig);

// On component mount, download the lookup data if online
onMounted(() => {
  if (ONLINE) lookupStore.download();
});
</script>

<template>
  <div class="app-wrapper">
    <!-- Render the navigation bar -->
    <NavBar  v-if="userStore.loggedIn" />
    <div class="left-side-nav-container">
      <!-- Render the left side navigation if it should be visible -->
      <LeftSideNav v-if="showSideNav" v-model="showSideNav" />
      <div
        class="container is-max-desktop px-2 py-4 custom-container mt-6"
        :class="{ 'has-left-side-nav': showSideNav, 'main-content': !showSideNav }"
      >


        <!-- Render the router view using the current route's fullPath as a key -->
        <router-view :key="$route.fullPath"></router-view>
      </div>
    </div>
  </div>
</template>

<style>
/* Importing required CSS libraries */
@import "bulma/css/bulma.min.css";
@import "@creativebulma/bulma-tooltip";

/* Styling for the app wrapper */
.app-wrapper {
  display: flex;
  flex-direction: column;
}

/* Styling for the left-side-nav container */
.left-side-nav-container {
  display: flex;
  flex-grow: 1;
}

/* Styling for when left side navigation is visible */
.has-left-side-nav {
  margin-left: 240px;
  flex-grow: 1;
}

/* Styling for the main content when left side navigation is not visible */
.main-content {
  margin-left: 0px;
  flex-grow: 1;
}

/* Custom styling for the container */
.custom-container {
  max-width: 100%; /* Adjust this value to your desired width */
}
</style>
