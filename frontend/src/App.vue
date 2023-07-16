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
import { Layout, LayoutContent, LayoutFooter, LayoutHeader, LayoutSider, Space } from "ant-design-vue";

import Header from "./components/Layout/Header.vue";
import Sidebar from "./components/Layout/Sidebar.vue";
import { MenuUnfoldOutlined } from "@ant-design/icons-vue";

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



  <Layout v-else>
    <Sidebar></Sidebar>
    <!-- <LayoutSider>
      <LeftSideNav v-if="showSideNav" v-model="showSideNav" />
    </LayoutSider> -->

    <Layout>
      <LayoutHeader :has-sider="true" style="background: #fff; padding: 0px 16px 0px 0px;">
        <MenuUnfoldOutlined v-if="sideNavStore.visible" class="trigger"
          @click="() => (sideNavStore.visible = !sideNavStore.visible)" />
        <MenuUnfoldOutlined v-else class="trigger" @click="() => (sideNavStore.visible = !sideNavStore.visible)" />

        <!-- Place a dropdown at the end of the header -->

        <Header></Header>
      </LayoutHeader>

      <LayoutContent :style="{ margin: '24px 16px 0px 16px', padding: '24px', background: '#fff', minHeight: '280px' }">

        <router-view :key="$route.fullPath"></router-view>

      </LayoutContent>

      <LayoutFooter>Footer</LayoutFooter>
    </Layout>
  </Layout>
</template>

<style>
/* Importing required CSS libraries */
@import "bulma/css/bulma.min.css";
@import "@creativebulma/bulma-tooltip";

html {
  overflow-y: auto;
}

.trigger {
  font-size: 18px;
  line-height: 64px;
  padding: 0 24px;
  cursor: pointer;
  transition: color 0.3s;
}

.trigger:hover {
  color: #1890ff;
}

.logo {
  height: 32px;
  background: rgba(255, 255, 255, 0.3);
  margin: 16px;
}

.site-layout .site-layout-background {
  background: #fff;
}


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
