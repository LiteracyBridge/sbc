<script setup lang="ts">
import { computed, ref, watch } from "vue";
import { useProjectStore } from "@/stores/projects";
import { useSideNavStore } from "@/stores/sideNav";
import { useRouter } from "vue-router";
import {
  MenuItem,
  Image,
  LayoutSider,
  Menu,
  Divider,
  Typography,
  Avatar,
} from "ant-design-vue";
import { UserOutlined } from "@ant-design/icons-vue";
import LogoLarge from "@/assets/logo-color.png";

const router = useRouter();

const config = ref({
  activeMenu: null,
});
const isActive = (item) => {
  if (item.name) {
    return router.currentRoute.value.name === item.name;
  } else if (item.path) {
    return router.currentRoute.value.path === item.path;
  }
  return false;
};

const isExactActive = (item) => {
  if (item.params) {
    return (
      JSON.stringify(router.currentRoute.value.params) === JSON.stringify(item.params)
    );
  }
  return true;
};

const projectStore = useProjectStore();
const menuItems = [
  { label: "Dashboard", path: "/" },
  { label: "Project Info", path: "/project-info" },
  { label: "Background and context", name: "forms", params: { module: "background" } },
  {
    label: "Project Objectives",
    path: "/project-objectives",
  },
  { label: "Audiences", path: "/audiences" },
  { label: "Behavioral Drivers", path: "/drivers" },
  { label: "SBC Approaches", path: "/interventions" },
  { label: "Theory of Change", path: "/toc" },
  { label: "Communications and Messaging", path: "/communications-and-messaging" },
  { label: "Monitoring and Evaluation", path: "/monitoring-and-evaluation" },
  {
    label: "Project Management",
    path: "/project-management",
  },
  { label: "Project Documents", path: "/project-documents" },
];

const projectSelected = computed(
  () => projectStore.prj_id !== null && projectStore.prj_id !== undefined
);
const showSideNav = ref(projectSelected.value);
const store = useSideNavStore();
const toggleSideNav = () => {
  if (showSideNav.value) {
    store.hide();
  } else {
    store.show();
  }
  showSideNav.value = !showSideNav.value;
};

watch(projectSelected, (newVal) => {
  if (newVal) {
    showSideNav.value = true;
  } else {
    showSideNav.value = false;
  }
});
</script>

<!--
<template>
  <div>
    <aside
      class="menu is-hidden-mobile"
      v-show="showSideNav"
    >
      <p class="menu-label">
{{projectStore.projectName}}
      </p>
      <ul class="menu-list">
        <li v-for="(item, index) in menuItems" :key="index">
          <router-link v-if="item.name" :to="{ name: item.name, params: { module: item.params.module }}">
            {{item.label}}
          </router-link>
          <router-link v-if="item.path" :to="item.path">
            {{item.label}}
          </router-link>
        </li>
      </ul>
    </aside>
  </div>
</template>
-->

<template>
  <LayoutSider
    v-model:collapsed="store.visible"
    :trigger="null"
    collapsible
    :style="{ minHeight: '100vh', backgroundColor: 'white' }"
    breakpoint="lg"
    :collapsed-width="0"
    width="260px"
  >
    <div class="logo">
      <Image :src="LogoLarge">
        <!-- <template #icon><CompassOutlined /></template> -->
      </Image>

      <!-- <span> Amplio </span> -->
    </div>
    <Divider></Divider>

    <Menu v-model:selectedKeys="config.activeMenu" theme="light" mode="inline">
      <MenuItem v-for="(item, index) in menuItems" :key="index">
        <router-link v-if="item.name" :to="'/forms/' + item.params?.module">
          <span role="link">
            {{ item.label }}
          </span>
        </router-link>

        <router-link v-if="item.path" :to="item.path">
          <span role="link">
            {{ item.label }}
          </span>
        </router-link>
      </MenuItem>

      <!-- <Divider :style="{ 'background-color': 'white' }"></Divider> -->
    </Menu>
  </LayoutSider>
</template>

<style scoped>
.logo {
  height: 48px;
  display: inline-flex;
  /* background: rgba(255, 255, 255, 0.3); */
  margin: 20px;
  margin-bottom: 0px;
  /* margin-left: 40px; */
  /* padding-top: 8px; */
  /* color: white; */
  text-align: center;
  /* font-size: 30px; */
}

#logo-image {
  max-width: fit-content;
  max-height: fit-content;
  height: 50px;
  padding-right: 8px;
}
</style>
