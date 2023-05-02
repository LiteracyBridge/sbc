<script setup>
import { onMounted, ref, watch } from "vue";
import { useLookupStore } from "@/stores/lookups";
import { useProjectStore } from "@/stores/projects";
import { useUserStore } from "@/stores/user";
import { useRouter } from "vue-router";
import * as api from "@/apis/lambda";

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
  projectStore.addUser(newUserName.value, newUserEmail.value, newUserAccessId.value, newUserAddressAs.value);
}

// Save new project and reset draftingNewProject flag
function saveNewProject() {
  draftingNewProject.value = false;
  projectStore.add(newPrjName.value, newPrjCountryId.value);
}

// Redirect to login if user is not logged in
onMounted(() => (userStore.loggedIn ? null : useRouter().push({ path: "/login" })));

// Change the current project and navigate to the basic forms page
function changeProject(prjId) {
  projectStore.setPrj(prjId);
  router.push('/forms/basic');
}
</script>

<template>
  <!-- Check if the user has an ID and no name, prompt for name -->
  <div v-if="userStore.id && userStore.name === null">
    We need to get you a name!
  </div>
  <hr />

  <!-- Display the user's projects -->
  <div class="is-size-5 is-bold">Your projects:</div>

  <table class="table">
    <thead>
      <tr>
        <th></th>
        <th>Project</th>
        <th>Country</th>
        <th>Your Role</th>
      </tr>
    </thead>
    <tbody>
      <!-- List projects and related data -->
      <tr
        v-for="project in projectStore.projects()"
        class="has-text-weight-medium"
        :key="project.prj_id"
      >
        <td>
          <input
            type="radio"
            v-model="projectSelection"
            id="selectedProject"
            name="selectedProject"
            :value="project.prj_id"
      	/>
    </td>
    <td>{{ project.name }}</td>
    <td>{{ lookupStore.lookupNameById("countries", project.country_id) }}</td>
    <td>{{ lookupStore.lookupNameById("access_types", project.access_id) }}</td>
  </tr>
  <!-- Show new project input fields when draftingNewProject is true -->
  <tr v-if="draftingNewProject">
    <td></td>
    <td><input ref="newPrjNameRef" v-model="newPrjName" type="text" /></td>
    <td>
      <div class="control">
        <div class="select">
          <select v-model="newPrjCountryId">
            <option
              v-for="country in lookupStore.countries"
              :value="country.id"
              :key="country.id"
            >
              {{ country.name }}
            </option>
          </select>
        </div>
      </div>
    </td>
  </tr>
</tbody>
</table>
  <!-- Display buttons for opening, creating, and archiving projects -->
  <div v-if="!draftingNewProject">
    <button
      class="button"
      :disabled="projectSelection == projectStore.prj_id"
      @click.prevent="changeProject(projectSelection)"
    >
      <span>Open Project</span>
    </button>
    <button class="button mx-5" @click.prevent="draftNewProject">
      <span>Create Project</span>
    </button>
    <button
      class="button mx-5"
      :disabled="!projectSelection"
      @click.prevent="projectStore.archive(projectSelection)"
    >
      <span>Archive Project</span>
    </button>
  </div>
  <!-- Show cancel and save buttons when drafting a new project -->
  <div v-else>
    <button class="button" @click.prevent="draftingNewProject = false">
      <span>Cancel</span>
    </button>
    <button class="button" @click.prevent="saveNewProject">
      <span>Save</span>
    </button>
  </div>
  <br/>
  <br/>
  <!-- Display users with access to the selected project -->
  <div v-if="projectStore.prj_id">    
    Users with access to {{ projectStore.projectName }}:
    <table class="table">
      <thead>
        <tr>
          <th>Name</th>
          <th>Address As</th>
          <th>Email</th>
          <th>Role</th>
        </tr>
      </thead>
      <tbody>
        <!-- List users and their access information -->
        <tr v-for="uip in projectStore.users_in_project" :key="uip.key">
          <td>{{ uip.name }}</td>
          <td>{{ uip.address_as }}</td>
          <td>{{ uip.email }}</td>
          <td v-if="projectStore.userById(userStore.id).access_id == 0">
            <div class="control">
              <div class="select">
                <select
                  :value="uip.access_id"
                  @change="projectStore.updateAccess($event, uip.id)"
                >
                  <option
                    v-for="access in lookupStore.access_types"
                    :value="access.id"
                    :key="access.id"
                  >
                    {{ access.name }}
                  </option>
                </select>
              </div>
            </div>
          </td>
          <td v-else>{{ lookupStore.lookupNameById("access_types", uip.access_id) }}</td>
        </tr>
            <!-- Show new user input fields when draftingNewUser is true -->
        <tr v-if="draftingNewUser">
          <td><input ref="newUserNameRef" v-model="newUserName" type="text" /></td>
          <td><input ref="newUserAddressAsRef" v-model="newUserAddressAs" type="text"/></td>
          <td><input v-model="newUserEmail" type="text" /></td>
          <td>
            <div class="control">
              <div class="select">
                <select v-model="newUserAccessId">
                  <option
                                  v-for="access in projectStore.grantableAccess"
                                  :value="access.id"
                                  :key="access.id"
                                >
                    {{ access.name }}
                  </option>
                </select>
              </div>
            </div>
          </td>
        </tr>
      </tbody>
    </table>
    <!-- Display buttons for adding users -->
    <div v-if="!draftingNewUser">
      <button class="button" @click.prevent="draftNewUser">
        <span>Add User</span>
      </button>
    </div>
    <!-- Show cancel and save buttons when drafting a new user -->
    <div v-else>
      <button class="button" @click.prevent="draftingNewUser = false">
        <span>Cancel</span>
      </button>
      <button class="button" @click.prevent="saveNewUser">
        <span>Save</span>
      </button>
    </div>
  </div>
</template>
<style>
.vertical-center {
  margin: 2rem;
}
</style>
