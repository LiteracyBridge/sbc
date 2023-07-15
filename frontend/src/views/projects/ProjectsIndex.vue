<script lang="ts" setup>
import { onMounted, ref } from "vue";
import { useUserStore } from "@/stores/user";
import { useRouter } from "vue-router";

import ProjectsTable from "./ProjectsTable.vue";
import { Divider, Tabs, TabPane } from "ant-design-vue";
import ProjectUsers from "./ProjectUsers.vue";
import ProjectStakeholders from "./ProjectStakeholders.vue";

const userStore = useUserStore();

const activeTab = ref("users");

onMounted(() => {
  // Redirect to login if user is not logged in
  if (userStore.loggedIn == false) {
    useRouter().push({ path: "/login" });
    return;
  }
});
</script>

<template>
  <section class="section">
    <!-- Projects table component -->
    <ProjectsTable></ProjectsTable>

    <Divider></Divider>

    <Tabs v-model:activeKey="activeTab" centered>
      <TabPane key="users" tab="Project Users">
        <ProjectUsers></ProjectUsers>
      </TabPane>

      <TabPane key="stakeholders" tab="Project Stakeholders">
        <ProjectStakeholders></ProjectStakeholders>
      </TabPane>
    </Tabs>
  </section>
</template>
