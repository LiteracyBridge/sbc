<script lang="ts" setup>

import { computed, onMounted, ref } from "vue";
import { useLookupStore } from "@/stores/lookups";
import { useProjectStore } from "@/stores/projects";
import {
  Table, Spin, Space, Col, Row,
  Modal, Button, Tag,
  Typography, Form, type FormInstance, FormItem, Input,
  Select,
  SelectOption,
  message,
  Tooltip
} from "ant-design-vue";
import { DeleteOutlined, InfoCircleOutlined, PlusCircleOutlined } from "@ant-design/icons-vue";
import { useUserStore } from "@/stores/user";
import { ApiRequest } from "@/apis/api";
import { User } from "@/types";

const lookupStore = useLookupStore();
const projectStore = useProjectStore();
const userStore = useUserStore();

const allUsers = ref<User[]>([]);
const config = ref({
  loading: false,
    visible: false,
    form: {
      role_id: null,
      email: null,
    }
});
const projectUserFormRef = ref<FormInstance>();


const columns = [
  {
    title: 'Name',
    key: 'name',
  },
  {
    title: 'Address As',
    key: 'address_as',
  },
  {
    title: 'Email',
    key: 'email',
  },
  {
    title: 'Role',
    key: 'role',
  },
  {
    title: '',
    key: 'actions',
  },
]

function closeModal() {
  projectUserFormRef.value.resetFields();
  config.value.visible = false;
}

function saveNewUser() {
  projectUserFormRef.value.validateFields().then((_) => {
    const form = config.value.form;
    const user = allUsers.value.find(user => user.email == form.email)

    projectStore.addUser(user.name ?? 'N/A', form.email, form.role_id, user.address_as).then((_) => {
      message.success(`Added ${user.name} to project ${projectStore.projectName}`);
    })


    closeModal();
  });
}

function fetchUsers() {
  ApiRequest.get<User>(`users/organisation/${userStore.email}`).then((resp) => {
    console.log(resp);
    allUsers.value = resp;
  });
}

onMounted(() => {
  fetchUsers();
});

const usersDropdownOptions = computed(() => {
  return allUsers.value.map((user) => {
    return {
      value: user.email,
      label: user.name != '' ? `${user.name} (${user.email})` : user.email,
    };
  }).filter((u) => projectStore.users_in_project.find((p) => p.email == u.value) == undefined);
});

function filterUser(input: string, option: any) {
  return option.label.toLowerCase().indexOf(input.toLowerCase()) >= 0;
}
</script>

<template>
  <Table
    :columns="columns"
    :data-source="projectStore.users_in_project"
    bordered
    :loading="config.loading"
  >
    <template #title>
      <div class="full-width">
        <span>
          <Typography :level="3"
            >Users with access to {{ projectStore.projectName }}</Typography
          >
        </span>

        <!-- TODO: implement creating new project in a modal -->
        <Button
          type="primary"
          @click="config.visible = true"
          v-if="(projectStore.users_in_project || []).length > 0"
        >
          <template #icon>
            <PlusCircleOutlined />
          </template>
          Add User
        </Button>
      </div>
    </template>

    <template #bodyCell="{ column, record: user }">
      <template v-if="column.key == 'name'">
        {{ user.name }}
      </template>

      <template v-if="column.key == 'address_as'">
        {{ user.address_as }}
      </template>

      <template v-if="column.key == 'email'">
        {{ user.email }}
      </template>

      <template v-if="column.key == 'role'">
        <!-- <Select
          :value="user.access_id"
          @change="projectStore.updateAccess($event, user.id)"
          v-if="projectStore.userById(userStore.id).access_id == 0"
          style="width: 100%"
        >
          <SelectOption
            v-for="access in lookupStore.access_types"
            :value="access.id"
            :key="access.id"
          >
            {{ access.name }}
          </SelectOption>
        </Select> -->

        <span>
          {{ lookupStore.lookupNameById("access_types", user.access_id) }}
        </span>
      </template>

      <template v-if="column.key === 'actions'">
        <!-- <Button type="primary" :disabled="true" :ghost="true" :danger="true">
          <template #icon>
            <DeleteOutlined />
          </template>
          Remove
        </Button> -->
      </template>
    </template>
  </Table>

  <Modal
    v-model:open="config.visible"
    @cancel="closeModal()"
    title="New Project User"
    ok-text="Add User"
    cancel-text="Cancel"
    :mask-closable="false"
    @ok="saveNewUser()"
  >
    <Form
      name="new-user-form"
      ref="projectUserFormRef"
      :model="config.form"
      layout="vertical"
    >
      <FormItem
        name="email"
        label="Email"
        has-feedback
        :rules="[{ required: true, message: 'Please select a email!' }]"
      >
        <Select
          v-model:value="config.form.email"
          placeholder="Select email"
          :allow-clear="true"
          :options="usersDropdownOptions"
          :show-search="true"
          :filter-option="filterUser"
        >
        </Select>
      </FormItem>

      <FormItem
        name="role_id"
        label="Role"
        has-feedback
        :rules="[{ required: true, message: 'Please select a role!' }]"
      >
        <Select v-model:value="config.form.role_id" placeholder="Select role">
          <SelectOption v-for="access in projectStore.grantableAccess" :key="access.id">
            {{ access.name }}
          </SelectOption>
        </Select>
      </FormItem>
    </Form>
  </Modal>
</template>
