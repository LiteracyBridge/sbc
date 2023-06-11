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
import { Table, Spin, Space, Col, Row, ButtonGroup, Button, Tag, Typography } from "ant-design-vue";
import { FolderOpenOutlined, FolderOutlined, PlusCircleOutlined } from "@ant-design/icons-vue";

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

const config = ref({
  loading: false
})

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

const columns = [
  {
    title: 'Project',
    key: 'name',
  },
  {
    title: 'Country',
    key: 'country',
  },
  {
    title: 'Role',
    dataIndex: 'role',
    key: 'role',
  },
  {
    title: '',
    key: 'actions',
  },
]
</script>

<template>
  <Spin :spinning="config.loading">
    <Table :columns="columns" :data-source="projectStore.projects()" bordered>
      <template #title>
        <Row justify="space-between">
          <Col :span="20">
          <Typography :level="2">My Projects</Typography>
          </Col>

          <Col :span="4">
          <!-- TODO: implement creating new project in a modal -->
          <Button type="primary">
            <template #icon>
              <PlusCircleOutlined />
            </template>
            Add Activity
          </Button>
          </Col>
        </Row>
      </template>

      <template #bodyCell="{ column, record: project }">
        <template v-if="column.key == 'name'">
          {{ project.name }}
          <Tag class="is-rounded" :color="project.archived ? 'red' : 'green'">
            {{ project.archived ? 'Archived': 'Active' }}
          </Tag>
        </template>

        <template v-if="column.key == 'country'">
          {{ lookupStore.lookupNameById("countries", project.country_id) }}
        </template>

        <template v-if="column.key == 'role'">
          {{ lookupStore.lookupNameById("access_types", project.access_id) }}
        </template>

        <template v-if="column.key === 'actions'">
          <Space>
            <!-- TODO: open modal for creating project -->
            <Button type="primary" :ghost="true" v-if="!project.archived">
              <template #icon>
                <FolderOpenOutlined />
              </template>
              Open
            </Button>

            <!-- TODO: show confirmation box for archiving -->
            <Button type="primary" :ghost="true" :danger="true" v-if="!project.archived">
              <template #icon>
                <FolderOutlined />
              </template>
              Archive
            </Button>

            <!-- TODO: Add unarchive button -->
          </Space>
        </template>

      </template>
    </Table>
  </Spin>

  <!-- Check if the user has an ID and no name, prompt for name -->
  <div v-if="userStore.id && userStore.name === null">
    We need to get you a name!
  </div>
  <hr />

  <!-- Display the user's projects -->
  <div class="is-size-5 is-bold">Your projects:</div>

  <table class="table is-fullwidth is-hoverable">
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
  <div v-else class="has-text-centered">
    <button class="button is-danger mr-5" @click.prevent="draftingNewProject = false">
      <span>Cancel</span>
    </button>
    <button class="button is-primary" @click.prevent="saveNewProject">
      <span>Save</span>
    </button>
  </div>
  <br />
  <br />


  <!-- Display users with access to the selected project -->
  <div v-if="projectStore.prj_id">
    Users with access to {{ projectStore.projectName }}:

    <table class="table is-fullwidth is-hoverable is-stripped">
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
          <td>
            <input ref="newUserNameRef" class="input" disabled v-model="newUserName" type="text" />
          </td>

          <td>
            <input ref="newUserAddressAsRef" v-model="newUserAddressAs" type="text" class="input" disabled />
          </td>

          <td>
            <!-- TODO: change this dropdown -->

            <Multiselect v-model="newUserEmail" :options="usersDropdownOptions" :close-on-select="true"
              :clear-on-select="false" placeholder="Select user" label="label" track-by="value"
              @select="onUserSelected" />
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
    <div v-if="!draftingNewUser" class="has-text-centered">
      <button class="button" @click.prevent="draftNewUser">
        <span>Add User</span>
      </button>
    </div>

    <!-- Show cancel and save buttons when drafting a new user -->
    <div v-else class="has-text-centered">
      <button class="button is-primary mr-5" @click.prevent="saveNewUser">
        <span>Save</span>
      </button>

      <button class="button is-danger" @click.prevent="draftingNewUser = false">
        <span>Cancel</span>
      </button>
    </div>
  </div>
</template>

<style>
.vertical-center {
  margin: 2rem;
}
</style>
