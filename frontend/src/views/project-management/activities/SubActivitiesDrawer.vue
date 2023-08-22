<script lang="ts" setup>
import { ref, watch } from "vue";
import { useActivityStore } from "@/stores/activities";
import { useLookupStore } from "@/stores/lookups";
import { useProjectStore } from "@/stores/projects";
import { Button, Tag, Drawer, Table, Popconfirm } from "ant-design-vue";
import { Activity } from "@/types";
import { PlusCircleOutlined } from "@ant-design/icons-vue";
import { formatDate } from "@/helpers";
import dayjs from "dayjs";

import AddSubActivityModal from "./AddSubActivityModal.vue";

const lookupStore = useLookupStore();
const projectStore = useProjectStore();

const emit = defineEmits<{
  (e: "isClosed", status: boolean): boolean;
}>();
const props = defineProps<{ activity?: Activity; visible: boolean }>();

const config = ref({
  visible: false,
  modal: {
    visible: false,
    editing: false,
    task: null as Activity | null,
  },
});

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

function editActivity(id: number) {
  const activity = activityStore.activityById(id);
  activity.start_date = dayjs(activity.start_date);
  activity.end_date = dayjs(activity.end_date);
  // activity.end_date = activity.end_date?.toDate() as any;

  config.value.modal.task = activity;
  config.value.modal.visible = true;
}

watch(
  props,
  (newProps) => {
    console.log("new props", newProps);
    config.value.visible = newProps.activity == null ? false : newProps.visible;
  },
  { deep: true }
);

function closeModal() {
  config.value.visible = false;
  emit("isClosed", false);
}

function showModal() {
  config.value.modal.task = new Activity();
  config.value.modal.visible = true;
}

const columns = [
  {
    title: "Name",
    dataIndex: "name",
    key: "name",
  },
  {
    title: "Owner",
    dataIndex: "Owner",
    key: "owner",
  },
  {
    title: "Deadline",
    key: "deadline",
  },
  { title: "Action", key: "action" },
];
</script>

<template>
  <AddSubActivityModal
    v-if="config.modal.visible"
    :parent-activity="props.activity"
    :draft-activity="config.modal.task"
    :visible="config.modal.visible"
    @closed="config.modal.visible = false"
  >
  </AddSubActivityModal>

  <Drawer
    :title="props.activity?.name"
    v-model:open="config.visible"
    :mask-closable="false"
    width="70vw"
    @close="closeModal()"
  >
    <template #extra>
      <Button @click="closeModal()"> Close </Button>
    </template>

    <div v-if="props.activity?.id != null">
      <Table
        :columns="columns"
        :data-source="activityStore.subActivitiesByActivityId(props.activity.id)"
        bordered
        :loading="activityStore.isLoading"
      >
        <template #title>
          <Button type="primary" @click="showModal()">
            <PlusCircleOutlined /> Add Task
          </Button>
        </template>

        <template #bodyCell="{ column, record: activity }">
          <template v-if="column.key === 'name'">
            <span>{{
              activity.name
            }}</span>

            <Tag class="is-rounded" :color="getStatusColor(activity.status_id).color">
              {{ getStatusColor(activity.status_id).status }}
            </Tag>
          </template>

          <template v-if="column.key === 'owner'">
            {{ projectStore.userName(activity.owner_id) }}
          </template>

          <template v-if="column.key === 'deadline'">
            {{ formatDate(activity.end_date) || "N/A" }}
          </template>

          <template v-if="column.key === 'action'">
            <Popconfirm
              title="Are you sure?"
              ok-text="Yes"
              cancel-text="No"
              @confirm="activityStore.deleteActivity(activity.id)"
            >
              <Button type="primary" :ghost="true" danger size="small"> Delete </Button>
            </Popconfirm>

            <Button
              @click="editActivity(activity.id)"
              type="primary"
              :ghost="true"
              size="small"
              class="ml-2"
              >Edit</Button
            >
          </template>
        </template>
      </Table>
    </div>
  </Drawer>
</template>

<style></style>
