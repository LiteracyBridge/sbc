<script lang="ts" setup>
import { computed, onMounted, ref, watch } from "vue";
import { useActivityStore } from "@/stores/activities";
import { useLookupStore } from "@/stores/lookups";
import { useProjectStore } from "@/stores/projects";
import { Button, Tag, Drawer, Table } from "ant-design-vue";
import { Activity } from "@/types";
import { useUserStore } from "@/stores/user";

const columns = [
  {
    title: "Name",
    dataIndex: "name",
    key: "name",
  },
  {
    title: "Duration",
    dataIndex: "duration",
    key: "duration",
  },
];

const userStore = useUserStore();
const lookupStore = useLookupStore();
const projectStore = useProjectStore();

const activityStore = useActivityStore();

function getStatusColor(status_id: number) {
  const status = lookupStore.lookupNameById("activity_status", status_id);
  let color = "blue";

  switch (status) {
    case "planned":
      color = "blue";
      break;
    case "in progress":
      color = "brown";
      break;
    case "completed":
      color = "green";
      break;
    case "proposed":
      color = "orange";
      break;
    default:
      color = "ash";
  }

  return { color, status };
}

const myActivities = computed(() => {
  return (
    activityStore.activities.filter(
      (activity) => activity.owner_id === userStore.id && activity.parent_id != null
    ) || []
  );
});

onMounted(() => {
  activityStore.download();
})

</script>

<template>
  <Table :columns="columns" :data-source="myActivities" bordered :loading="activityStore.isLoading">
    <template #title> My Tasks </template>

    <template #bodyCell="{ column, record: activity }">
      <template v-if="column.key === 'name'">
        <Button type="text">{{ activity.name }}</Button>

        <Tag class="is-rounded" :color="getStatusColor(activity.status_id).color">
          {{ getStatusColor(activity.status_id).status }}
        </Tag>
      </template>

      <!-- TODO: add activity column -->

      <template v-if="column.key === 'duration'">
        {{ activityStore.fromDate(activity.id) }} -
        {{ activityStore.toDate(activity.id) }}
      </template>
    </template>
  </Table>
</template>

<style></style>
