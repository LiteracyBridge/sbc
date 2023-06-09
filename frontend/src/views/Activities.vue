<script setup>
import { onMounted, ref, reactive } from "vue";
import { useActivityStore } from "../stores/activities";
import { useInterventionStore } from "../stores/interventions";
import { useDriverStore } from "../stores/drivers";
import { useLookupStore } from "@/stores/lookups";
import { useProjectStore } from '@/stores/projects'
import { useParticipantStore } from '@/stores/participants'
import { useUserStore } from "@/stores/user";
import { useRouter } from 'vue-router'
import AddActivityModal from '../components/AddActivityModal.vue';

const showAddModal = ref(false);
const showEditModal = ref(false);

const userStore = useUserStore();
const interventionStore = useInterventionStore();
const driverStore = useDriverStore();
const lookupStore = useLookupStore();
const projectStore = useProjectStore();
const participantStore = useParticipantStore();
const expandActivity = ref([]);

onMounted (()=>userStore.loggedIn ? null :  useRouter().push({ path: '/login'}));

const activityStore = useActivityStore();

const emptyActivity = reactive({
      name:'',parent_id:null,intervention_id:null,
      driver_ids:[],owner_id:null, status_id:1, notes:'', url:''
      });

const draftActivity = ref(null);

function editActivity(activity) {
  draftActivity.value = JSON.parse(JSON.stringify(activity));
  showEditModal.value = true;
}

</script>

<template>
  <button class="button is-primary m-4" @click.prevent = "showAddModal = true">
    <span v-if="!showAddModal">Add</span>
  </button>

  <!-- <button class="button" @click.prevent = "showEditModal = true">
    <span v-if="!showEditModal">Edit Activity</span>
  </button> -->
  <AddActivityModal v-if="showAddModal" :draft-activity="emptyActivity" v-model="showAddModal"/>
  <AddActivityModal v-if="showEditModal" :draft-activity="draftActivity" v-model="showEditModal"/>
  <table class="table">
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
        <td v-if="activityStore.subActivitiesByActivityId(activity.id).length==0"></td>
        <td v-else-if="!expandActivity.includes(activity.id)"><a @click="expandActivity.push(activity.id)">></a></td>
        <td v-else><a @click="expandActivity.splice(expandActivity.indexOf(activity.id),1)">V</a></td>
        <td>{{activity.id}}</td> 
        <td><a @click="editActivity(activity)">{{activity.name}}</a></td>
        <td>{{lookupStore.lookupNameById('activity_status',activity.status_id)}}</td>
        <td>{{projectStore.userName(activity.owner_id)}}</td>
        <td>{{activityStore.fromDate(activity.id)}}</td>
        <td>{{activityStore.toDate(activity.id)}}</td>
        <td>{{interventionStore.interventionNameById(activity.intervention_id)}}</td>
        <td v-if="activity.driver_ids && activity.driver_ids.length==1">{{driverStore.nameById(activity.driver_ids[0])}}</td>
        <td v-else><i>{{activity.driver_ids.length}} drivers</i></td>
       </tr>
       <template v-if="expandActivity.includes(activity.id)">
        <tr v-for="subActivity in activityStore.subActivitiesByActivityId(activity.id)" class="has-text-weight-normal">
          <td></td>
          <td>{{subActivity.id}}</td>
          <td><span class="mx-2"><a @click="editActivity(subActivity)">{{subActivity.name}}</a></span></td>
          <td>{{lookupStore.lookupNameById('activity_status',subActivity.status_id)}}</td>
          <td>{{projectStore.userName(subActivity.owner_id)}}</td>
          <td>{{activityStore.fromDate(subActivity.id)}}</td>
          <td>{{activityStore.toDate(subActivity.id)}}</td>
          <td>{{interventionStore.interventionNameById(subActivity.intervention_id)}}</td>
          <td v-if="subActivity.driver_ids && subActivity.driver_ids.length==1">{{driverStore.nameById(subActivity.driver_ids[0])}}</td>
          <td v-else><i>{{subActivity.driver_ids.length}} drivers</i></td>
        </tr>
       </template>
      </template>
    </tbody>
  </table>  


</template>

<style>
.vertical-center {
  margin: 2rem;
}
</style>
