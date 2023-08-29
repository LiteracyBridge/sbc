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

const tasksDrawer = ref({ visible: false, activity: null as Activity });
const config = ref({
  modal: {
    activity: null as Activity,
    visible: false,
  },
});

function editActivity(id: number) {
  const activity = activityStore.topLevelActivities.find((a) => a.id == id);

  config.value.modal.visible = true;
  config.value.modal.activity = activity;
}

function showDrawer(id: number) {
  const activity = activityStore.topLevelActivities.find((a) => a.id == id);

  console.log(activity);
  tasksDrawer.value.activity = activity;
  tasksDrawer.value.visible = true;
  console.log("here");
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
    :visible="tasksDrawer.visible"
    @is-closed="tasksDrawer = { visible: false, activity: null }"
    :activity="tasksDrawer.activity"
  ></SubActivitiesDrawer>

  <div v-if="config.modal.activity != null">
    <AddSubActivityModal
      v-if="config.modal.visible"
      :parent-activity="config.modal.activity"
      :draft-activity="config.modal.activity"
      :visible="config.modal.visible"
      :is-activity="true"
      @closed="
        config.modal.visible = false;
        config.modal.activity = null;
      "
    >
    </AddSubActivityModal>
  </div>

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
          <Button type="link" @click="editActivity(activity.id)">{{
            activity.name
          }}</Button>
        </Space>
      </template>

      <template v-if="column.key === 'status'">
        {{ lookupStore.lookupNameById("activity_status", activity.status_id) }}
      </template>

      <template v-if="column.key === 'owner'">
        {{ projectStore.userName(activity.owner_id) }}
      </template>

      <template v-if="column.key === 'duration'">
        {{ formatDate(activity.start_date) || "N/A" }} -
        {{ formatDate(activity.end_date) || "N/A" }}
      </template>

      <template v-if="column.key === 'tasks'">
        <Button type="link" @click.prevent="showDrawer(activity.id)">
          View Tasks ({{ activityStore.subActivitiesByActivityId(activity.id).length }})
        </Button>
      </template>

      <template v-if="column.key === 'action'">
        <Space>
          <Button
            :ghost="true"
            type="primary"
            size="small"
            @click="editActivity(activity.id)"
            >Edit</Button
          >
          <!-- <Button type="link" @click="editActivity(activity)">Delete</Button> -->
        </Space>
      </template>
    </template>
  </Table>


</template>

<style></style>
