<script lang="ts" setup>
// Importing required Vue libraries and modules
import { ref, onMounted } from "vue";
import { useUserStore } from "@/stores/user";
import { useRouter } from "vue-router";
import { Card, Col, Tag, Table, Divider, Row, Space, Statistic, TypographyTitle } from "ant-design-vue";
import { useProjectStore } from "@/stores/projects";
import dayjs from 'dayjs'
import { useActivityStore } from "@/stores/activities";
import { useTheoryOfChangeStore } from "@/stores/theory_of_change";
import { useProjectDataStore } from "@/stores/projectData";
import { DatabaseOutlined, DeploymentUnitOutlined, ProfileOutlined, TeamOutlined } from "@ant-design/icons-vue";
import { useLookupStore } from "@/stores/lookups";

// Initialize the user store and the router
const userStore = useUserStore(),
  projectStore = useProjectStore(),
  lookupStore = useLookupStore();

const router = useRouter();

// On component mount, redirect to the login page if the user is not logged in
onMounted(() => {
  if (!userStore.loggedIn) {
    router.push({ path: "/login" });
  }
});

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
]
</script>

<template>
  <section class="section">
    <Space direction="horizontal" style="width: 100%; justify-content: center; padding-bottom: 15px;">
      <TypographyTitle :level="3">Welcome, {{ userStore.address_as || userStore.name }}!</TypographyTitle>
    </Space>

    <Divider></Divider>
    <Space direction="horizontal" style="width: 100%; justify-content: space-between">
      <span> Current Project: <strong>{{ projectStore.current_project?.name }}</strong>
      </span>

      <span>Last modified by {{ projectStore.userName(projectStore.current_project?.editing_user_id) }} @ {{
        dayjs(projectStore.current_project.updated_at ?? (new Date().toISOString())).format('dddd MMMM M, YYYY') }}</span>
    </Space>

    <Divider></Divider>
    <Row :gutter="8" style="padding: 10px;">
      <Col :span="6">
      <Card>
        <Statistic title="Activities" :value="useActivityStore().topLevelActivities.length">
          <template #prefix>
            <ProfileOutlined />
          </template>
        </Statistic>
      </Card>
      </Col>

      <Col :span="6">
      <Card>
        <Statistic title="Tasks" :value="useActivityStore().totalSubActivities">
          <template #prefix>
            <DatabaseOutlined />
          </template>
        </Statistic>
      </Card>
      </Col>


      <Col :span="6">
      <Card>
        <Statistic title="Indicators" :value="useTheoryOfChangeStore().allTocIndicators.length">
          <template #prefix>
            <DeploymentUnitOutlined />
          </template>
        </Statistic>
      </Card>
      </Col>

      <Col :span="6">
      <Card>
        <Statistic title="Audiences" :value="useProjectDataStore().audiences.length">
          <template #prefix>
            <TeamOutlined />
          </template>
        </Statistic>
      </Card>
      </Col>
    </Row>

    <Divider orientation="left" style="padding-top: 50px;">My Projects</Divider>

    <Table :columns="columns" :data-source="projectStore.projects()" bordered size="small">

      <template #bodyCell="{ column, record: project }">
        <template v-if="column.key == 'name'">
          {{ project.name }}
          <Tag class="is-rounded" v-if="projectStore.prj_id == project.prj_id" :color="'green'">
            Currently Opened
          </Tag>

          <Tag class="is-rounded" color="red" v-if="project.archived">
            Archived
          </Tag>
        </template>

        <template v-if="column.key == 'duration'">
          <span v-if="project.start_date == null">N/A</span>
          <span v-else>
            {{ dayjs(project.start_date).format('MMMM D, YYYY') }} - {{ dayjs(project.end_date).format('MMMM D, YYYY') }}
          </span>
        </template>

        <template v-if="column.key == 'country'">
          {{ lookupStore.lookupNameById("countries", project.country_id) }}
        </template>

        <template v-if="column.key == 'role'">
          {{ lookupStore.lookupNameById("access_types", project.access_id) }}
        </template>

      </template>
    </Table>
  </section>
</template>

<style scoped>
/* Styling for vertical center alignment */
.vertical-center {
  margin: 2rem;
}

/* Styling to raise the welcome message to slightly above center */
.raised-title {
  margin-top: -20rem;
  /* Adjust this value to change the vertical position */
}
</style>
