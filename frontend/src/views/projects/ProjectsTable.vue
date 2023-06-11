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
  message
} from "ant-design-vue";
import { FolderOpenOutlined, FolderOutlined, PlusCircleOutlined } from "@ant-design/icons-vue";

const router = useRouter();
const lookupStore = useLookupStore();
const projectStore = useProjectStore();


const config = ref({
  loading: false,
  projectModal: {
    visible: false,
    form: {
      name: "",
      country_id: null,
    }
  }
});
const projectFormRef = ref<FormInstance>();


// Change the current project and navigate to the basic forms page
function changeProject(prjId: number) {
  projectStore.setPrj(prjId);

  const project = projectStore.user_projects.find(prj => prj.prj_id == prjId);

  message.success(`Switched to project ${project?.name}`);
  router.push('/forms/basic');
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

function closeProjectModal() {
  projectFormRef.value.resetFields();
  config.value.projectModal.visible = false;
}

function createProject() {
  projectFormRef.value.validateFields().then((_) => {
    const form = config.value.projectModal.form;
    projectStore.add(form.name, form.country_id);

    closeProjectModal();
  });
}

function filterCountry(input: string, option: any) {
  return option.name.toLowerCase().indexOf(input.toLowerCase()) >= 0;
}
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
          <Button type="primary" @click="config.projectModal.visible = true;">
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
          <Tag class="is-rounded" v-if="projectStore.prj_id == project.prj_id" :color="'green'">
            Currently Opened
          </Tag>

          <Tag class="is-rounded" :color="project.archived ? 'red' : 'green'">
            {{ project.archived ? 'Archived' : 'Active' }}
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
            <Button type="primary" :ghost="true" v-if="!project.archived" @click="changeProject(project.prj_id)">
              <template #icon>
                <FolderOpenOutlined />
              </template>
              Open
            </Button>

            <!-- TODO: show confirmation box for archiving -->
            <Button type="primary" :ghost="true" :danger="true" v-if="!project.archived"
              @click="projectStore.archive(project.prj_id)">
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


  <Modal v-model:visible="config.projectModal.visible" @cancel="closeProjectModal()" ok-text="Create Project"
    cancel-text="Cancel" :mask-closable="false" @ok="createProject()">
    <template #title>
      <span>Create New Project</span>
    </template>

    <Form name="activity-form" ref="projectFormRef" :model="config.projectModal.form" layout="vertical">

      <FormItem label="Project Name" name="name" :rules="[{ required: true, message: 'Please entity project name!' }]">
        <Input v-model:value="config.projectModal.form.name" />
      </FormItem>

      <FormItem name="country_id" label="Country" has-feedback
        :rules="[{ required: true, message: 'Please select a country!' }]">
        <Select v-model:value="config.projectModal.form.country_id" placeholder="Select country" :allow-clear="true"
          :options="lookupStore.countries" :field-names="{ label: 'name', value: 'id' }" :show-search="true"
          :filter-option="filterCountry">

        </Select>
      </FormItem>
    </Form>
  </Modal>
</template>
