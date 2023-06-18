<script lang="ts" setup>

// TODO: implement adding activity schedules
import { ref, watch } from "vue";
import { useActivityStore } from "@/stores/activities";
import { useInterventionStore } from "@/stores/interventions";
import { useDriverStore } from "@/stores/drivers";
import { useLookupStore } from "@/stores/lookups";
import { useProjectStore } from '@/stores/projects'
import { Button, Drawer, Table } from "ant-design-vue";
import { Activity } from "@/types";
import { PlusCircleOutlined } from "@ant-design/icons-vue";

import AddSubActivityModal from './AddSubActivityModal.vue';

const interventionStore = useInterventionStore();
const driverStore = useDriverStore();
const lookupStore = useLookupStore();
const projectStore = useProjectStore();

const emit = defineEmits<{
  (e: 'isClosed', status: boolean): boolean,
}>()
const props = defineProps<{ activity: Activity, visible: boolean }>()

const config = ref({
  visible: false,
  modal: {
    visible: false,
    editing: false,
    task: null as Activity | null,
  }
})

const activityStore = useActivityStore();


function editActivity(activity: Activity) {
  // TODO: implement activity editing

  // draftActivity.value = JSON.parse(JSON.stringify(activity));
  // showEditModal.value = true;
}


watch(props, (newProps) => {
  config.value.visible = newProps.visible
}, { deep: true })

function closeModal() {
  config.value.visible = false
  emit('isClosed', false)
}

const columns = [
  {
    title: 'Name',
    dataIndex: 'name',
    key: 'name',
  },
  {
    title: 'Status',
    dataIndex: 'status',
    key: 'status',
  },
  {
    title: 'Owner',
    dataIndex: 'Owner',
    key: 'owner',
  },
  {
    title: 'Duration',
    dataIndex: 'duration',
    key: 'duration',
  },
  // {
  //   title: 'Intervention',
  //   dataIndex: 'intervention',
  //   key: 'intervention',
  // },
  // {
  //   title: 'Drivers',
  //   dataIndex: 'drivers',
  //   key: 'drivers',
  // },
]
</script>

<template>
  <AddSubActivityModal v-if="config.modal.visible" :parent-activity="props.activity" :draft-activity="config.modal.task"
    :visible="config.modal.visible" @closed="config.modal.visible = false">
  </AddSubActivityModal>

  <Drawer title="Activity Tasks" v-model:visible="config.visible" :mask-closable="false" width="70vw">
    <template #extra>
      <Button @click="closeModal()">
        Close
      </Button>
    </template>

    <Table :columns="columns" :data-source="activityStore.subActivitiesByActivityId(props.activity.id)" bordered>
      <template #title>
        <Button type="primary" @click="config.modal.visible = true; config.modal.task = new Activity()">
          <PlusCircleOutlined /> Add Task
        </Button>
      </template>

      <template #bodyCell="{ column, record: activity }">
        <template v-if="column.key === 'name'">
          <Button type="text" @click="editActivity(activity)">{{ activity.name }}</Button>
        </template>

        <template v-if="column.key === 'status'">
          {{ lookupStore.lookupNameById('activity_status', activity.status_id) }}
        </template>

        <template v-if="column.key === 'owner'">
          {{ projectStore.userName(activity.owner_id) }}
        </template>

        <template v-if="column.key === 'duration'">
          {{ activityStore.fromDate(activity.id) }} - {{ activityStore.toDate(activity.id) }}
        </template>

        <!-- <template v-if="column.key === 'intervention'">
          {{ interventionStore.interventionNameById(activity.intervention_id) }}
        </template>

        <template v-if="column.key === 'drivers'">
          <span v-if="activity.driver_ids && activity.driver_ids.length == 1">{{
            driverStore.nameById(activity.driver_ids[0]) }}
          </span>

          <span v-else>
            <i>0 drivers</i>
          </span>
        </template> -->
      </template>
    </Table>
  </Drawer>
</template>

<style>
</style>
