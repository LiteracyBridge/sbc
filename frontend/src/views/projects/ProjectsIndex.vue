<script lang="ts" setup>

import { onMounted } from "vue";
import { useUserStore } from "@/stores/user";
import { useRouter } from "vue-router";

import ProjectsTable from './ProjectsTable.vue';
import { Divider } from "ant-design-vue";
import ProjectUsers from "./ProjectUsers.vue";

const userStore = useUserStore();


onMounted(() => {
  // Redirect to login if user is not logged in
  if (userStore.loggedIn == false) {
    useRouter().push({ path: "/login" })
    return;
  }

});

</script>

<template>
  <!-- <section class="section"> -->

  <div>
    <!-- Projects table component -->
    <ProjectsTable></ProjectsTable>

    <Divider></Divider>

    <ProjectUsers></ProjectUsers>
  </div>


  <!-- </section> -->
</template>
