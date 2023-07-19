<script lang="ts" setup>
import { computed, onMounted, ref, watch } from "vue";
import { useActivityStore } from "@/stores/activities";
import { useLookupStore } from "@/stores/lookups";
import { Button, Tag, Table } from "ant-design-vue";
import { formatDate } from "@/helpers";
import { useUserStore } from "@/stores/user";

const columns = [
  {
    title: "Name",
    key: "name",
  },
  {
    title: "Activity",
    key: "activity",
  },
  {
    title: "Deadline",
    key: "deadline",
  },
];

const userStore = useUserStore();
const lookupStore = useLookupStore();

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
});
</script>

<template>
  <Table
    :columns="columns"
    :data-source="myActivities"
    bordered
    :loading="activityStore.isLoading"
  >
    <template #title> My Tasks </template>

    <template #bodyCell="{ column, record: activity }">
      <template v-if="column.key === 'name'">
        <Button type="text">{{ activity.name }}</Button>

        <Tag class="is-rounded" :color="getStatusColor(activity.status_id).color">
          {{ getStatusColor(activity.status_id).status }}
        </Tag>
      </template>

      <template v-if="column.key === 'activity'">
        <Button type="text">{{ activityStore.activityById(activity.parent_id)?.name || 'N/A' }}</Button>
      </template>


      <template v-if="column.key === 'deadline'">
        {{ formatDate(activity.end_date) || "N/A" }}
      </template>
    </template>
  </Table>
</template>

<style></style>
