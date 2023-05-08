<script setup>
import { onMounted, ref, watch, computed } from "vue";
import { Multiselect } from 'vue-multiselect'
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

// Users list dropdown

const userEmails = computed(() => {
  return [
    { value: "test", label: "Test 1" },
    { value: "test1", label: "Test 2" },
    { value: "test2", label: "Test 3" },
    { value: "test3", label: "Test 4" }, { value: "test4", label: "Test 5" }, { value: "test5", label: "Test 6" }, { value: "test6", label: "Test 7" }, { value: "test7", label: "Test 8" }, { value: "test8", label: "Test 9" }, { value: "test9", label: "Test 10" }
  ];

  console.log(newUserEmail)
  if (newUserEmail.value === '') {
    return []
  }

  // let user_id = await api.getAll('users', 'email ILIKE ' + newUserEmail.value, true); // get from db if exists
  console.log('checking user id');
  // console.log(user_id)
  // if (!user_id) {
  //   // user doesn't exist, so insert user into db
  //   user_id = await api.insert('users', { name, email, last_project_id, address_as }); // otherwise insert and get it
  // }

  return ["country 1", "country 2"]
  let matches = 0

  return countries.filter(country => {
    if (
      country.name.toLowerCase().includes(searchTerm.value.toLowerCase())
      && matches < 10
    ) {
      matches++
      return country
    }
  })
});

async function searchUser() {
  // TODO: fetch users list
  // let searchTerm = ref('')

  return ["sdfsdf", "sdfsdf"]
  console.log(newUserEmail);


  return {
    searchTerm
  }
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
      <tr v-for="project in projectStore.projects()" class="has-text-weight-medium" :key="project.prj_id">
        <td>
          <input type="radio" v-model="projectSelection" id="selectedProject" name="selectedProject"
            :value="project.prj_id" />
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
                <option v-for="country in lookupStore.countries" :value="country.id" :key="country.id">
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
    <button class="button" :disabled="projectSelection == projectStore.prj_id"
      @click.prevent="changeProject(projectSelection)">
      <span>Open Project</span>
    </button>
    <button class="button mx-5" @click.prevent="draftNewProject">
      <span>Create Project</span>
    </button>
    <button class="button mx-5" :disabled="!projectSelection" @click.prevent="projectStore.archive(projectSelection)">
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
  <br />
  <br />


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
                <select :value="uip.access_id" @change="projectStore.updateAccess($event, uip.id)">
                  <option v-for="access in lookupStore.access_types" :value="access.id" :key="access.id">
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
          <td><input ref="newUserAddressAsRef" v-model="newUserAddressAs" type="text" /></td>
          <td>
            <!-- TODO: change this dropdown -->

            <Multiselect v-model="newUserEmail" :options="userEmails" :close-on-select="true" :clear-on-select="false"
              placeholder="Select one" label="label" track-by="label" />
            <!--
            <div class="field">
              <p class="control  has-icons-right">
                <input v-model="newUserEmail" class="input is-primary" type="text" placeholder="Search email here..."
                  list="user_emails" />

                <span class="icon is-small is-right">
                  <i class="fas fa-search"></i>
                </span>
              </p>

              <datalist id="user_emails" class="list">
                <option v-for="email in userEmails" :key="email" :value="email" class="list-item">
                </option>
              </datalist>
            </div> -->

          </td>

          <td>
            <div class="control">
              <div class="select">
                <select v-model="newUserAccessId">
                  <option v-for="access in projectStore.grantableAccess" :value="access.id" :key="access.id">
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
