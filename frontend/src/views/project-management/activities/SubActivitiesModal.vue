<script lang="ts" setup>
import { onMounted, ref, reactive, watch } from "vue";
import { useActivityStore } from "@/stores/activities";
import { useInterventionStore } from "@/stores/interventions";
import { useDriverStore } from "@/stores/drivers";
import { useLookupStore } from "@/stores/lookups";
import { useProjectStore } from '@/stores/projects'
import { useParticipantStore } from '@/stores/participants'
import { useUserStore } from "@/stores/user";
import { Button, Modal, Space, Spin, Table, Tag, Typography } from "ant-design-vue";
import { Activity } from "@/types";


const interventionStore = useInterventionStore();
const driverStore = useDriverStore();
const lookupStore = useLookupStore();
const projectStore = useProjectStore();

const emit = defineEmits<{
  (e: 'isClosed', status: boolean): boolean,
}>()
const props = defineProps<{ activity: Activity, visible: boolean }>()

const config = ref({ visible: false })

const activityStore = useActivityStore();


// function editActivity(activity) {
//   draftActivity.value = JSON.parse(JSON.stringify(activity));
//   showEditModal.value = true;
// }

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
  {
    title: 'Intervention',
    dataIndex: 'intervention',
    key: 'intervention',
  },
  {
    title: 'Drivers',
    dataIndex: 'drivers',
    key: 'drivers',
  },
]
</script>

<template>
  <Modal title="Sub Activities" v-model:visible="config.visible" @cancel="closeModal()" @ok="closeModal()">

    <Table :columns="columns" :data-source="activityStore.subActivitiesByActivityId(activity.id)" bordered>
      <template #bodyCell="{ column, record: activity }">
        <template v-if="column.key === 'name'">
          <Space>
            <a @click="editActivity(activity)">{{ activity.name }}</a>

            <Tag :style="{ 'border-radius': '10px' }" :color="'#108ee9'">sub activities</Tag>
          </Space>
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

        <template v-if="column.key === 'intervention'">
          {{ interventionStore.interventionNameById(activity.intervention_id) }}
        </template>

        <template v-if="column.key === 'drivers'">
          <span v-if="activity.driver_ids && activity.driver_ids.length == 1">{{
            driverStore.nameById(activity.driver_ids[0]) }}
          </span>

          <span v-else>
            <i>0 drivers</i>
          </span>
        </template>
      </template>
    </Table>
  </Modal>


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

<style>
</style>
