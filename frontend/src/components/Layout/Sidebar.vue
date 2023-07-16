<script setup lang="ts">
import { computed, ref, watch } from "vue";
import { useProjectStore } from "@/stores/projects";
import { useSideNavStore } from "@/stores/sideNav";
import { useRouter } from "vue-router";
import { MenuItem, LayoutSider, Menu, Divider } from "ant-design-vue";

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
  { label: "Project Documents", name: "forms", params: { module: "prjdocs" } },
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
    :style="{ minHeight: '100vh' }"
    breakpoint="lg"
    :collapsed-width="0"
    width="250px"
  >
    <div class="logo">
      {{ projectStore.projectName }}
      <Divider></Divider>
    </div>

    <Menu v-model:selectedKeys="config.activeMenu" theme="dark" mode="inline">
      <MenuItem v-for="(item, index) in menuItems" :key="index">
        <router-link v-if="item.name" :to="'/forms/' + item.params?.module">
          <span>
            {{ item.label }}
          </span>
        </router-link>

        <router-link v-if="item.path" :to="item.path">
          <span>
            {{ item.label }}
          </span>
        </router-link>
      </MenuItem>

      <Divider :style="{ 'background-color': 'white' }"></Divider>
      <MenuItem key="3">
        <span>nav 1</span>
      </MenuItem>
    </Menu>
  </LayoutSider>
</template>

<style scoped></style>
