<script lang="ts" setup>

import { ref } from "vue";
import { useLookupStore } from "@/stores/lookups";
import { useProjectStore } from "@/stores/projects";
import { useRouter } from "vue-router";
import {
  Table, Spin, Space, Col, Row,
  Modal, Button, Tag,
  Typography, Form, type FormInstance, FormItem, Input,
  Select,
  message,
  DatePicker
} from "ant-design-vue";
import { FolderOpenOutlined, FolderOutlined, PlusCircleOutlined } from "@ant-design/icons-vue";
import { Project } from "@/types";
import dayjs from 'dayjs';

const router = useRouter();
const lookupStore = useLookupStore();
const projectStore = useProjectStore();


const config = ref({
  loading: false,
  projectModal: {
    visible: false,
    form: new Project()
  }
});
const projectFormRef = ref<FormInstance>();


// Change the current project and navigate to the basic forms page
async function changeProject(prjId: number) {

  const project = projectStore.user_projects.find(prj => prj.prj_id == prjId);

  message.success(`Switching active project to ${project?.name}`);

  await projectStore.setPrj(prjId, true);
  window.location.reload()
  // router.push('/forms/basic');
}

const columns = [
  {
    title: 'Project',
    key: 'name',
  },
  {
    title: 'Duration',
    key: 'duration',
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

function closeProjectModal() {
  projectFormRef.value.resetFields();
  config.value.projectModal.visible = false;
}

function createProject() {
  projectFormRef.value.validateFields().then((_) => {
    const form = config.value.projectModal.form;
    console.log(form)
    // return
    projectStore.add(form.name, form.country_id, form.start_date.toISOString(), form.end_date.toISOString());

    closeProjectModal();
  });
}

function filterCountry(input: string, option: any) {
  return option.name.toLowerCase().indexOf(input.toLowerCase()) >= 0;
}
</script>

<template>
  <Table
    :columns="columns"
    :data-source="projectStore.projects()"
    bordered
    :loading="config.loading"
  >
    <template #title>
      <div class="full-width">
        <Typography :level="2">My Projects</Typography>

        <Button type="primary" @click="config.projectModal.visible = true">
          <template #icon>
            <PlusCircleOutlined />
          </template>
          Add Project
        </Button>
      </div>
    </template>

    <template #bodyCell="{ column, record: project }">
      <template v-if="column.key == 'name'">
        {{ project.name }}
        <Tag
          class="is-rounded"
          v-if="projectStore.prj_id == project.prj_id"
          :color="'green'"
        >
          Currently Opened
        </Tag>

        <Tag class="is-rounded" :color="project.archived ? 'red' : 'green'">
          {{ project.archived ? "Archived" : "Active" }}
        </Tag>
      </template>

      <template v-if="column.key == 'duration'">
        <span v-if="project.start_date == null">N/A</span>
        <span v-else>
          {{ dayjs(project.start_date).format("MMMM D, YYYY") }} -
          {{ dayjs(project.end_date).format("MMMM D, YYYY") }}
        </span>
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
          <Button
            type="primary"
            size="small"
            :ghost="true"
            v-if="!project.archived"
            @click="changeProject(project.prj_id)"
          >
            <template #icon>
              <FolderOpenOutlined />
            </template>
            Open
          </Button>

          <!-- TODO: show confirmation box for archiving -->
          <Button
            type="primary"
            size="small"
            :ghost="true"
            :danger="true"
            v-if="!project.archived"
            @click="projectStore.archive(project.prj_id)"
          >
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

  <Modal
    v-model:open="config.projectModal.visible"
    @cancel="closeProjectModal()"
    ok-text="Create Project"
    cancel-text="Cancel"
    :mask-closable="false"
    @ok="createProject()"
  >
    <template #title>
      <span>Create New Project</span>
    </template>

    <Form
      name="new-project-form"
      ref="projectFormRef"
      :model="config.projectModal.form"
      layout="vertical"
    >
      <FormItem
        label="Project Name"
        name="name"
        :rules="[{ required: true, message: 'Please enter project name!' }]"
      >
        <Input v-model:value="config.projectModal.form.name" />
      </FormItem>

      <FormItem
        name="country_id"
        label="Country"
        has-feedback
        :rules="[{ required: true, message: 'Please select a country!' }]"
      >
        <Select
          v-model:value="config.projectModal.form.country_id"
          placeholder="Select country"
          :allow-clear="true"
          :options="lookupStore.countries"
          :field-names="{ label: 'name', value: 'id' }"
          :show-search="true"
          :filter-option="filterCountry"
        >
        </Select>
      </FormItem>

      <Row :gutter="6">
        <Col :span="12">
          <FormItem
            name="start_date"
            label="Start Date"
            has-feedback
            :rules="[{ required: true, message: 'Please choose project start date!' }]"
          >
            <DatePicker v-model:value="config.projectModal.form.start_date" />
          </FormItem>
        </Col>

        <Col :span="12">
          <FormItem
            name="end_date"
            label="End Date"
            has-feedback
            :rules="[{ required: true, message: 'Please choose project end date!' }]"
          >
            <DatePicker v-model:value="config.projectModal.form.end_date" />
          </FormItem>
        </Col>
      </Row>
    </Form>
  </Modal>
</template>
