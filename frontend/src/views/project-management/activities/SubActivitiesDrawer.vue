<script lang="ts" setup>
// TODO: implement adding activity schedules
import { ref, watch } from "vue";
import { useActivityStore } from "@/stores/activities";
import { useInterventionStore } from "@/stores/interventions";
import { useDriverStore } from "@/stores/drivers";
import { useLookupStore } from "@/stores/lookups";
import { useProjectStore } from "@/stores/projects";
import { Button, Tag, Drawer, Table, Popconfirm } from "ant-design-vue";
import { Activity } from "@/types";
import { PlusCircleOutlined } from "@ant-design/icons-vue";
import { formatDate } from "@/helpers";

import AddSubActivityModal from "./AddSubActivityModal.vue";

const interventionStore = useInterventionStore();
const driverStore = useDriverStore();
const lookupStore = useLookupStore();
const projectStore = useProjectStore();

const emit = defineEmits<{
  (e: "isClosed", status: boolean): boolean;
}>();
const props = defineProps<{ activity: Activity; visible: boolean }>();

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

function editActivity(activity: Activity) {
  // TODO: implement activity editing
  // draftActivity.value = JSON.parse(JSON.stringify(activity));
  // showEditModal.value = true;
}

watch(
  props,
  (newProps) => {
    config.value.visible = newProps.visible;
  },
  { deep: true }
);

function closeModal() {
  config.value.visible = false;
  emit("isClosed", false);
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
    v-model:visible="config.visible"
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
          <Button
            type="primary"
            @click="
              config.modal.visible = true;
              config.modal.task = new Activity();
            "
          >
            <PlusCircleOutlined /> Add Task
          </Button>
        </template>

        <template #bodyCell="{ column, record: activity }">
          <template v-if="column.key === 'name'">
            <Button type="text" @click="editActivity(activity)">{{
              activity.name
            }}</Button>

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
          </template>
        </template>
      </Table>
    </div>
  </Drawer>
</template>

<style></style>
