<script setup>
import { useDriverStore } from "../stores/drivers";
import { useLookupStore } from "../stores/lookups";
import { useActivityStore } from "../stores/activities";
import { useInterventionStore } from "../stores/interventions";
import { ref, onMounted } from "vue";
import { useUserStore } from "@/stores/user";
import { useRouter } from 'vue-router'

const userStore = useUserStore();
onMounted (()=> {
  userStore.loggedIn ? null :  useRouter().push({ path: '/login'})
}
);

const driverStore = useDriverStore();
const lookupStore = useLookupStore();
const activityStore = useActivityStore();
const interventionStore = useInterventionStore();

const selectedDriver = ref(null);
const selectedPrjDriver = ref(null);


function addIntervention(intervention) {
  let driver_ids = [];
  if (selectedPrjDriver.value) {
    driver_ids = [selectedPrjDriver.value.id];
  } 
  activityStore.addActivity({ name: intervention.name, driver_ids, intervention_id: intervention.id })
}

</script>

<template>
  <section ref="top" class="section">
    <div class="container">
      <main>
        <div
          v-for="intervention in interventionStore.interventions"
          :key="intervention.key"
        >
        <div v-if="intervention.name != 'Social movements'">
          <div class="level">
            <div class="level-left">
              <div class="level-item has-text-weight-bold">
                {{ intervention.name }}
              </div>
            </div>
            <div class="level-right">
              <div class="level-item">
                <button
                  v-if="!interventionStore.activityIds(intervention.id).length"
                  @click="addIntervention(intervention)"
                  class="button is-success"
                >
                  <span class="icon is-small">
                    <i class="fas fa-check"></i>
                  </span>
                  <span>Add</span>
                </button>
                <button
                  v-if="interventionStore.activityIds(intervention.id).length"
                  @click="activityStore.deleteIntervention(intervention.id)"
                  class="button is-danger is-outlined "
                >
                  <span class="icon is-small">
                    <i class="fas fa-times"></i>
                  </span>
                  <span>Remove</span>
                </button>
              </div>
            </div>
          </div>
          <p class="is-italic">{{ intervention.text_short }}</p>
          <br />
          <p>{{ intervention.text_long }}</p>
          <br />
          <br />
        </div>
        </div>
      </main>
    </div>
  </section>
</template>

<style>
.vertical-center {
  margin: 2rem;
}
</style>
<!-- 
 -->
