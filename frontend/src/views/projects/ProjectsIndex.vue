<script lang="ts" setup>

import { onMounted, ref, watch, computed } from "vue";
import { Multiselect } from 'vue-multiselect'
import { useLookupStore } from "@/stores/lookups";
import { useProjectStore } from "@/stores/projects";
import { useUserStore } from "@/stores/user";
import { useRouter } from "vue-router";
import * as api from "@/apis/lambda";
import { UsersApi } from "@/apis/lambda";
import axios from "axios";
import { ApiRequest } from "@/apis/api";
import { User } from "@/types";

import ProjectsTable from './ProjectsTable.vue';
import { Divider } from "ant-design-vue";
import ProjectUsers from "./ProjectUsers.vue";

const router = useRouter();
const userStore = useUserStore();
const lookupStore = useLookupStore();
const projectStore = useProjectStore();

const projectSelection = ref(projectStore.prj_id);
const draftingNewProject = ref(false);
const newPrjName = ref("");
const newPrjCountryId = ref(null);
const newPrjNameRef = ref(null);
const draftingNewUser = ref(false);
const newUserNameRef = ref(null);
const newUserAddressAsRef = ref(null);
const newUserName = ref("");
const newUserAddressAs = ref("");
const newUserEmail = ref("");
const newUserAccessId = ref(null);

const allUsers = ref([]);

// GPT prompt
const prompt = ref("");
const promptResp = ref("nothing yet");

// Focus on the new project input field when it's rendered
watch(newPrjNameRef, async (newValue, oldValue) => {
  if (newValue != null) {
    newPrjNameRef.value.focus();
  }
});

// Set draftingNewProject flag to show new project input fields
function draftNewProject() {
  draftingNewProject.value = true;
}

// Set draftingNewUser flag to show new user input fields
function draftNewUser() {
  draftingNewUser.value = true;
}

// Save new user and reset draftingNewUser flag
function saveNewUser() {
  draftingNewUser.value = false;
  projectStore.addUser(newUserName.value, newUserEmail.value?.value, newUserAccessId.value, newUserAddressAs.value);
}

// Save new project and reset draftingNewProject flag
function saveNewProject() {
  draftingNewProject.value = false;
  projectStore.add(newPrjName.value, newPrjCountryId.value);
}

function fetchUsers() {
  ApiRequest.get<User>(`users/`, { email: userStore.email }).then((resp) => {
    console.log(resp);
    allUsers.value = resp;
  });

  // axios.get("/api/users").then((response) => {
  //   console.log(response.data);
  // });
}

onMounted(() => {
  console.log("sdfsdfsdf")

  // Redirect to login if user is not logged in
  if (userStore.loggedIn == false) {
    useRouter().push({ path: "/login" })
    return;
  }

  // Fetch the user's projects
  fetchUsers();
});

// Change the current project and navigate to the basic forms page
function changeProject(prjId) {
  projectStore.setPrj(prjId);
  router.push('/forms/basic');
}

// Users list dropdown

const usersDropdownOptions = computed(() => {
  return allUsers.value.map((user) => {
    return {
      value: user.email,
      label: user.name != '' ? `${user.name} (${user.email})` : user.email,
    };
  });
});

function onUserSelected(item, _) {
  const user = allUsers.value.find(user => user.email == item.value)

  // newUserEmail.value = user.email
  newUserName.value = user.name ?? 'N/A'
  newUserAddressAs.value = user.address_as
}

</script>

<template>
  <section class="section">

    <!-- Check if the user has an ID and no name, prompt for name -->
    <div v-if="userStore.id && userStore.name === null">
      We need to get you a name!
    </div>
    <hr />

    <!-- Projects table component -->
    <ProjectsTable></ProjectsTable>

    <Divider></Divider>

    <ProjectUsers></ProjectUsers>

  </section>
</template>

<style>
.vertical-center {
  margin: 2rem;
}
</style>
