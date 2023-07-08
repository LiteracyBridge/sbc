<script lang="ts" setup>
import { onMounted, ref, reactive } from "vue";
import { useActivityStore } from "@/stores/activities";
import { useInterventionStore } from "@/stores/interventions";
import { useDriverStore } from "@/stores/drivers";
import { useLookupStore } from "@/stores/lookups";
import { useProjectStore } from "@/stores/projects";
import { Button, Space, Spin, Table, Tag, Typography } from "ant-design-vue";
import { formatDate } from "@/helpers";
import AddSubActivityModal from "./AddSubActivityModal.vue";
import SubActivitiesDrawer from "./SubActivitiesDrawer.vue";
import { Activity } from "@/types";

const lookupStore = useLookupStore();
const projectStore = useProjectStore();
const activityStore = useActivityStore();

const config = ref({
  selectedActivity: null,
  subActivityDrawer: { visible: false },
  modal: {
    activity: null as Activity,
    visible: false,
  },
});

function editActivity(activity: Activity) {
  config.value.modal.activity = activity;
  config.value.modal.visible = true;
}

onMounted(() => {
  activityStore.download();
});

const columns = [
  {
    title: "Name",
    dataIndex: "name",
    key: "name",
  },
  {
    title: "Status",
    dataIndex: "status",
    key: "status",
  },
  {
    title: "Owner",
    dataIndex: "Owner",
    key: "owner",
  },
  {
    title: "Duration",
    key: "duration",
  },
  {
    title: "Tasks",
    key: "tasks",
  },
  { title: "Action", key: "action" },
];
</script>

<template>
  <SubActivitiesDrawer
    :visible="config.subActivityDrawer.visible"
    @is-closed="
      config.selectedActivity = null;
      config.subActivityDrawer.visible = false;
    "
    :activity="config.selectedActivity"
  ></SubActivitiesDrawer>

  <AddSubActivityModal
    v-if="config.modal.visible"
    :parent-activity="config.modal.activity"
    :draft-activity="config.modal.activity"
    :visible="config.modal.visible"
    @closed="
      config.modal.visible = false;
      config.modal.activity = null;
    "
  >
  </AddSubActivityModal>

  <Table
    :columns="columns"
    :data-source="activityStore.topLevelActivities"
    bordered
    :loading="activityStore.isLoading"
  >
    <template #title> Project Activities </template>

    <template #bodyCell="{ column, record: activity }">
      <template v-if="column.key === 'name'">
        <Space>
          <!-- TODO: IMPLEMENT ACTIVITY -->
          <Button type="link" @click="editActivity(activity)">{{ activity.name }}</Button>
        </Space>
      </template>

      <template v-if="column.key === 'status'">
        {{ lookupStore.lookupNameById("activity_status", activity.status_id) }}
      </template>

      <template v-if="column.key === 'owner'">
        {{ projectStore.userName(activity.owner_id) }}
      </template>

      <template v-if="column.key === 'duration'">
        {{ formatDate(activity.start_date) || "" }} -
        {{ formatDate(activity.end_date) || "" }}
      </template>

      <template v-if="column.key === 'tasks'">
        <Button
          type="link"
          @click="
            config.selectedActivity = activity;
            config.subActivityDrawer.visible = true;
          "
        >
          View Tasks ({{ activityStore.subActivitiesByActivityId(activity.id).length }})
        </Button>
      </template>

      <template v-if="column.key === 'action'">
        <Space>
          <Button
            :ghost="true"
            type="primary"
            size="small"
            @click="editActivity(activity)"
            >Edit</Button
          >
          <!-- <Button type="link" @click="editActivity(activity)">Delete</Button> -->
        </Space>
      </template>
    </template>
  </Table>

  <!-- TODO: display sub activites in a modal -->
  <!-- <template v-if="expandActivity.includes(activity.id)">
      <tr v-for="subActivity in activityStore.subActivitiesByActivityId(activity.id)" class="has-text-weight-normal">
        <td></td>
        <td>{{ subActivity.id }}</td>
        <td><span class="mx-2"><a @click="editActivity(subActivity)">{{ subActivity.name }}</a></span></td>
        <td>{{ lookupStore.lookupNameById('activity_status', subActivity.status_id) }}</td>
        <td>{{ projectStore.userName(subActivity.owner_id) }}</td>
        <td>{{ activityStore.fromDate(subActivity.id) }}</td>
        <td>{{ activityStore.toDate(subActivity.id) }}</td>
        <td>{{ interventionStore.interventionNameById(subActivity.intervention_id) }}</td>
        <td v-if="subActivity.driver_ids && subActivity.driver_ids.length == 1">
          {{ driverStore.nameById(subActivity.driver_ids[0]) }}</td>
        <td v-else><i>{{ subActivity.driver_ids.length }} drivers</i></td>
      </tr>
    </template> -->

  <!-- <button class="button is-primary m-4" @click.prevent="showAddModal = true">
    <span v-if="!showAddModal">Add</span>
  </button> -->

  <!-- <button class="button" @click.prevent = "showEditModal = true">
    <span v-if="!showEditModal">Edit Activity</span>
  </button> -->

  <!-- <AddActivityModal v-if="showAddModal" :draft-activity="emptyActivity" v-model="showAddModal" /> -->

  <!-- TODO: fix this -->
  <!-- <AddActivityModal v-if="showEditModal" @update:model-value="showEditModal = $event" v-model="showEditModal"
    :draft-activity="emptyActivity" /> -->

  <!-- <table class="table">
    <thead>
      <tr>
        <th></th>
        <th>ID</th>
        <th>Name</th>
        <th>Status</th>
        <th>Owner</th>
        <th>From</th>
        <th>To</th>
        <th>Intervention</th>
        <th>Drivers</th>
      </tr>
    </thead>
    <tbody>
      <template v-for="activity in activityStore.topLevelActivities">
        <tr class="has-text-weight-medium">
          <td v-if="activityStore.subActivitiesByActivityId(activity.id).length == 0"></td>

          <td v-else-if="!expandActivity.includes(activity.id)">
            <a @click="expandActivity.push(activity.id)"></a>
          </td>

          <td v-else><a @click="expandActivity.splice(expandActivity.indexOf(activity.id), 1)">V</a></td>

          <td>{{ activity.id }}</td>

          <td><a @click="editActivity(activity)">{{ activity.name }}</a></td>

          <td>{{ lookupStore.lookupNameById('activity_status', activity.status_id) }}</td>

          <td>{{ projectStore.userName(activity.owner_id) }}</td>
          <td>{{ activityStore.fromDate(activity.id) }}</td>
          <td>{{ activityStore.toDate(activity.id) }}</td>
          <td>{{ interventionStore.interventionNameById(activity.intervention_id) }}</td>
          <td v-if="activity.driver_ids && activity.driver_ids.length == 1">{{
            driverStore.nameById(activity.driver_ids[0]) }}
          </td>
          <td v-else><i>{{ activity.driver_ids.length }} drivers</i></td>
        </tr>

        <template v-if="expandActivity.includes(activity.id)">
          <tr v-for="subActivity in activityStore.subActivitiesByActivityId(activity.id)" class="has-text-weight-normal">
            <td></td>
            <td>{{ subActivity.id }}</td>
            <td><span class="mx-2"><a @click="editActivity(subActivity)">{{ subActivity.name }}</a></span></td>
            <td>{{ lookupStore.lookupNameById('activity_status', subActivity.status_id) }}</td>
            <td>{{ projectStore.userName(subActivity.owner_id) }}</td>
            <td>{{ activityStore.fromDate(subActivity.id) }}</td>
            <td>{{ activityStore.toDate(subActivity.id) }}</td>
            <td>{{ interventionStore.interventionNameById(subActivity.intervention_id) }}</td>
            <td v-if="subActivity.driver_ids && subActivity.driver_ids.length == 1">
              {{ driverStore.nameById(subActivity.driver_ids[0]) }}</td>
            <td v-else><i>{{ subActivity.driver_ids.length }} drivers</i></td>
          </tr>
        </template>
      </template>
    </tbody>
  </table> -->
</template>

<style></style>
