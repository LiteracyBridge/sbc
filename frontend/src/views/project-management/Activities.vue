<script lang="ts" setup>
import { onMounted, ref, reactive, watch } from "vue";
import { useActivityStore } from "@/stores/activities";
import { useInterventionStore } from "@/stores/interventions";
import { useDriverStore } from "@/stores/drivers";
import { useLookupStore } from "@/stores/lookups";
import { useProjectStore } from '@/stores/projects'
import { useParticipantStore } from '@/stores/participants'
import { useUserStore } from "@/stores/user";
import { useRouter } from 'vue-router'
import AddActivityModal from '@/components/AddActivityModal.vue';
import { Button, Space, Spin, Table, Tag, Typography } from "ant-design-vue";
import { PlusCircleOutlined } from "@ant-design/icons-vue";

const showAddModal = ref(false);
const showEditModal = ref(false);

const userStore = useUserStore();
const interventionStore = useInterventionStore();
const driverStore = useDriverStore();
const lookupStore = useLookupStore();
const projectStore = useProjectStore();
const participantStore = useParticipantStore();
const expandActivity = ref([]);

onMounted(() => userStore.loggedIn ? null : useRouter().push({ path: '/login' }));

const activityStore = useActivityStore();

const emptyActivity = reactive({
  name: '', parent_id: null, intervention_id: null,
  driver_ids: [], owner_id: null, status_id: 1, notes: '', url: ''
});

const draftActivity = ref(null);

function editActivity(activity) {
  draftActivity.value = JSON.parse(JSON.stringify(activity));
  showEditModal.value = true;
}

onMounted(() => {
  activityStore.download();
})
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
  <Spin :spinning="activityStore.isLoading">
    <Table :columns="columns" :data-source="activityStore.topLevelActivities" bordered>
      <template #title>
        <div class="level">
          <div class="level-left">
            <Typography :level="3">Project Activities</Typography>
          </div>

          <div class="level-right">
            <Button type="primary" @click="showAddModal = true">
              <template #icon>
                <PlusCircleOutlined />
              </template>
              Add Activity
            </Button>

            <!-- <Button type="ghost" @click="config.settingsModal.visible = true">
                <template #icon>
                  <SettingOutlined />
                </template>
                Settings
              </Button> -->
          </div>
        </div>
      </template>

      <template #bodyCell="{ column, record: activity }">
        <template v-if="column.key === 'name'">
          <Space>
            <a @click="editActivity(activity)">{{ activity.name }}</a>

            <Tag :style="{'border-radius': '10px'}" :color="'#108ee9'">sub activities</Tag>
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
            <i>{{ activity.driver_ids.length }} drivers</i>
          </span>
        </template>
      </template>
    </Table>
  </Spin>

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
  <AddActivityModal v-if="showAddModal" :draft-activity="emptyActivity" v-model="showAddModal" />

  <!-- TODO: fix this -->
  <AddActivityModal v-if="showEditModal" @update:model-value="showEditModal = $event" v-model="showEditModal"
    :draft-activity="emptyActivity" />

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
