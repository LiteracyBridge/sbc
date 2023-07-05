<script setup lang="ts">
// Importing required Vue and external libraries
import { onMounted, computed } from "vue";
import { RouterView, useRoute, useRouter } from "vue-router";
import { useLookupStore } from "./stores/lookups";
import NavBar from "@/components/Layout/NavBar.vue";
import LeftSideNav from "@/components/Layout/LeftSideNav.vue";
import "@aws-amplify/ui-vue/styles.css";
import { Amplify } from "aws-amplify";
import awsconfig from "./aws-exports";
import { useSideNavStore } from "@/stores/sideNav";
import { useUserStore } from '@/stores/user';
import { AppStore } from "./stores/app.store";
import GridLoader from "./components/spinners/GridLoader.vue";

const userStore = useUserStore();
const appStore = AppStore()
const route = useRoute(),
  router = useRouter()

// Set ONLINE to true when connected to the internet or false when offline
const ONLINE = true;

// Initialize the lookup store and side navigation store
// const lookupStore = useLookupStore();
const sideNavStore = useSideNavStore();

// Computed property for determining if the side navigation should be visible
const showSideNav = computed(() => sideNavStore.visible);

// Configure AWS Amplify with the provided configuration
// Amplify.configure(awsconfig);

// On component mount, download the lookup data if online
onMounted(async () => {
  // router.replace(route.name() || '/')
  // appStore.downloadObjects()

  console.warn(route.fullPath)
  if (router.hasRoute(route.name)) {
    await router.replace(router.currentRoute.value.fullPath)
  }

  // if (ONLINE) {
  //   lookupStore.download().then(() => appStore.setLoading(false))
  // } else {
  //   appStore.setLoading(false)
  // }
});

</script>

<template>
  <div v-if="appStore.isLoading" id="app-loader" style="margin-top: auto">
    <figure class="image is-128x128">
      <img src="@/assets/logo-color.png" />
    </figure>
    <!-- <GridLoader :loading="appStore.isLoading"></GridLoader> -->
  </div>

  <div class="app-wrapper" v-else>
    <!-- Render the navigation bar -->
    <NavBar v-if="userStore.loggedIn" />
    <div class="left-side-nav-container">
      <!-- Render the left side navigation if it should be visible -->
      <LeftSideNav v-if="showSideNav" v-model="showSideNav" />
      <div class="container is-max-desktop px-2 py-4 custom-container mt-6"
        :class="{ 'has-left-side-nav': showSideNav, 'main-content': !showSideNav }">


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
