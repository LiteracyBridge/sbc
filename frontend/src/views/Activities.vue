<script setup>
import { useActivityStore } from "../stores/activities";
import { onMounted, ref, reactive } from "vue";
import { useUserStore } from "@/stores/user";
import { useRouter } from 'vue-router'
import AddActivityModal from '../components/AddActivityModal.vue';

const showAddModal = ref(false);
const showEditModal = ref(false);

const userStore = useUserStore();
onMounted (()=>userStore.loggedIn ? null :  useRouter().push({ path: '/login'}));

const activityStore = useActivityStore();

const emptyActivity = reactive({
      name:'',parent_id:null,intervention_id:null,
      driver_ids:[],owner_id:null, status_id:1, notes:'', url:''
      });

const activity = reactive(JSON.parse(JSON.stringify(activityStore.activityById(27))));
console.log(activity);

</script>

<template>
  <button class="button" @click.prevent = "showAddModal = true">
    <span v-if="!showAddModal">Add Activity</span>
  </button>

  <button class="button" @click.prevent = "showEditModal = true">
    <span v-if="!showEditModal">Edit Activity</span>
  </button>

  <AddActivityModal 
    v-if="showAddModal" :draft-activity="emptyActivity" v-model="showAddModal"
  />

  <AddActivityModal 
    v-if="showEditModal" :draft-activity="activity" v-model="showEditModal"
  />


</template>

  <!-- <section ref="top" class="section">
    <div class="container">
      <div class="columns">
      </div>
    </div>
  </section> -->

<style>
.vertical-center {
  margin: 2rem;
}
</style>
