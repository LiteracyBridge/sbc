<script lang="ts" setup>
import { onMounted, ref } from "vue";
import { useUserStore } from "@/stores/user";
import { useRouter } from "vue-router";

import ProjectsTable from "./ProjectsTable.vue";
import { Divider, Card, Tabs, TabPane, PageHeader } from "ant-design-vue";
import ProjectUsers from "./ProjectUsers.vue";
import ProjectStakeholders from "./ProjectStakeholders.vue";
import { useProjectStore } from "@/stores/projects";

const userStore = useUserStore();
const store = useProjectStore();

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
  <PageHeader
    style="border: 1px solid rgb(235, 237, 240)"
    :title="store.projectName"
    sub-title="Manage project users and stakeholders"
  />

  <Card :bordered="false">
    <!-- Projects table component -->
    <Tabs v-model:activeKey="activeTab" centered>
      <TabPane key="users" tab="Project Users">
        <ProjectUsers></ProjectUsers>
        <Divider></Divider>

        <ProjectsTable></ProjectsTable>
      </TabPane>

      <TabPane key="stakeholders" tab="Project Stakeholders">
        <ProjectStakeholders></ProjectStakeholders>
      </TabPane>
    </Tabs>
  </Card>
</template>
