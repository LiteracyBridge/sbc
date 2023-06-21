<script setup>
import { onMounted, computed } from "vue";
import { useLookupStore } from "./stores/lookups";
import "@aws-amplify/ui-vue/styles.css";
import { useSideNavStore } from "@/stores/sideNav";
import { useUserStore } from '@/stores/user';
import { AppStore } from "./stores/app.store";
import AccessRequest from "@/views/AccessRequest.vue";

const userStore = useUserStore();
const appStore = AppStore()

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
  if (ONLINE) {
    lookupStore.download().then(() => appStore.setLoading(false))
  } else {
    appStore.setLoading(false)
  }
});
</script>

<template>
  <AccessRequest></AccessRequest>
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
  max-width: 100%;
  /* Adjust this value to your desired width */
}

#app-loader {
  position: fixed;
  top: 50%;
  left: 50%;
  /* bring your own prefixes */
  transform: translate(-50%, -50%);
}
</style>
