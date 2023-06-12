<script setup>
import { computed, ref, watch } from 'vue';
import { useProjectStore } from '@/stores/projects';
import { useSideNavStore } from "@/stores/sideNav";
import { useRouter } from 'vue-router';

const router = useRouter();

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
    return JSON.stringify(router.currentRoute.value.params) === JSON.stringify(item.params);
  }
  return true;
};


const projectStore = useProjectStore();
const menuItems = [
  { label: 'Project Info', name: 'forms', params: { module: 'basic' } },
  { label: 'Background and context', name: 'forms', params: { module: 'background' } },
  {
    label: 'Project Objectives',
    path: '/project-objectives'
  },
  { label: 'Audiences', name: 'forms', params: { module: 'audiences' } },
  { label: 'Behavioral Drivers', path: '/drivers' },
  { label: 'SBC Approaches', path: '/interventions' },
  { label: 'Theory of Change', path: '/toc' },
  { label: 'Communications and Messaging', name: 'forms', params: { module: 'communications' } },
  { label: 'Monitoring and Evaluation', path: '/monitoring-and-evaluation' },
  {
    label: 'Project Management',
    path: '/project-management'
  },
  { label: 'Project Documents', name: 'forms', params: { module: 'prjdocs' } },
];

const projectSelected = computed(() => projectStore.prj_id !== null && projectStore.prj_id !== undefined);
const showSideNav = ref(projectSelected.value);
const sideNavStore = useSideNavStore();
const toggleSideNav = () => {
  if (showSideNav.value) {
    sideNavStore.hide();
  } else {
    sideNavStore.show();
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
  <div>
    <aside class="menu is-hidden-mobile" v-show="showSideNav">
      <p class="menu-label">
        {{ projectStore.projectName }}
      </p>
      <ul class="menu-list">
        <li v-for="(item, index) in menuItems" :key="index">
          <router-link v-if="item.name && !(isActive(item) && isExactActive(item))"
            :to="{ name: item.name, params: { module: item.params.module } }">
            {{ item.label }}
          </router-link>
          <router-link v-if="item.path && !(isActive(item) && isExactActive(item))" :to="item.path">
            {{ item.label }}
          </router-link>
          <router-link to="item.path" v-if="isActive(item) && isExactActive(item)">
            <strong>
              {{ item.label }}
            </strong>
          </router-link>
        </li>
      </ul>
    </aside>
  </div>
</template>



<style scoped>
.menu {
  width: 240px;
  position: fixed;
  top: 3.25rem;
  /* Adjust this value based on the height of your NavBar */
  left: 0;
  height: calc(100% - 3.25rem);
  background-color: #f5f5f5;
  z-index: 100;
  padding: 1rem;
  overflow-y: auto;
}

.is-floating {
  border-radius: 50%;
  width: 2.5rem;
  height: 2.5rem;
  display: flex;
  justify-content: center;
  align-items: center;
  position: fixed;
  left: 1rem;
  top: calc(3.25rem + 5rem);
  /* Add 1rem margin to the existing top value */
  z-index: 100;
}
</style>
