<script setup>
import { useDriverStore } from "../stores/drivers";
import { useLookupStore } from "../stores/lookups";
import { useActivityStore } from "../stores/activities";
import { useMessageStore } from "../stores/messages";
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
const selectedFactor = ref(null);
const selectedPrjDriver = ref(null);
const selectedCategoryId = ref(null);
const driver_filter = ref("all");

function setImportance(event) {
  const importance_id = parseInt(event.target.value);
  selectedPrjDriver.value.importance_id = importance_id;
}

function addDriver() {
  driverStore.add(selectedDriver.value.id);
  const prjDriver = driverStore.prjDriverByLUid(selectedDriver.value.id);
  console.log(prjDriver);
  selectedPrjDriver.value = prjDriver;
}

function removeDriver() {
  if (activityStore.driverInActivities(selectedPrjDriver.value.id)) {
    // TODO: Add alert popup with this message:
    console.log('Cannot remove driver from project until there are no activities that support the driver.');
  } else {
    driverStore.remove(selectedPrjDriver.value.id);
    selectedPrjDriver.value = null;
  }
}

const setDriver = function (driver = null) {
  if (selectedDriver.value && selectedDriver.value == driver) {
    selectedDriver.value = null;
    selectedFactor.value = null;
    selectedPrjDriver.value = null;
  } else {
    if (driver.parent_id == 0) {
        selectedFactor.value = driver;
    } else if (selectedFactor.value.id != selectedDriver.value.parent_id) {        
        selectedFactor.value = driverStore.luDriverById(driver.parent_id);
    }
    selectedDriver.value = driver;
    selectedPrjDriver.value = driverStore.prjDriverByLUid(driver.id);
  }
  top.scrollTo(0,0);
}

function addIntervention(intervention) {
  let driver_ids = [];
  if (selectedPrjDriver.value) {
    driver_ids = [selectedPrjDriver.value.id];
  } 
  activityStore.addActivity({ name: intervention.name, driver_ids, intervention_id: intervention.id })
}

function getImportanceColor (driverId) {
  let color = 'white';
  const prjDriver = driverStore.prjDriverByLUid(driverId);
  if (prjDriver) {
    color = lookupStore.importance[prjDriver.importance_id].color;
  }
  return color;
}

function clearSelection () {
  if (driver_filter != 'all') {
    selectedCategoryId.value = null;
    selectedDriver.value = null;
    selectedFactor.value = null;
    selectedPrjDriver.value = null;
  }
}

</script>

<template>
  <section ref="top" class="section">
    <div class="container">
      <div class="columns">
        <div class="column is-narrow">
          <br/>
          <select name="filter_drivers" mx="mx-0" v-model="driver_filter" @change="clearSelection" class="outline-grey text-black text-base">
            <option value="all">All Drivers</option>
            <option value="project">Project Drivers</option>
            <option value="suggested">Suggested Drivers</option>
          </select>

          <aside class="is-small menu">
            <div
              v-for="category in driverStore.lu_driver_categories"
              :key="category.id"
              @click="selectedCategoryId=category.id"
            >
              <p class="menu-label">{{ category.name }}</p>

<!-- COLLAPSE IF ANOTHER CATEGORY'S DRIVER IS SELECTED -->
              <div class="menu-list"> <!--v-if="selectedDriver ? selectedCategoryId === category.id : true "-->
                <div
                  v-for="driver in driverStore.factorsByCategory(category.id,driver_filter)"
                  :key="driver.id"
                  class="ml-2 my-2 menu-item"
                  >
                  <div 
                    class="has-tooltip-multiline"
                    :data-tooltip="driver.text_short ? driver.text_short : null"
                  >
                    <a
                      href="#"
                      @click.prevent="setDriver(driver)"
                      class="level"
                      :class="driver.id === selectedDriver ? 'is-active' : ''"
                      :style="`outline-style:solid;outline-color:${getImportanceColor(driver.id)};background-color:${driverStore.lu_driver_categories[driver.category_id].color}`"
                    >
                      <div class="level-left">
                        <div class="level-item" :class="selectedFactor===driver ? 'has-text-weight-bold' : ''">
                          {{ driver.name }}
                        </div>
                      </div>
                    </a>
                  </div>
                  <div v-if="selectedFactor==driver">    <!-- driver_filter=='project' ||  -->
                      <div
                      v-for="dimension in driverStore.dimensionsByFactor(driver,driver_filter)"
                      :key="dimension.id" class="ml-4 my-4 menu-item"  
                      >
                      <a
                          href="#"
                          @click.prevent="setDriver(dimension)"
                          class="level"
                          :class="dimension.id === selectedDriver ? 'is-active' : ''"
                          :style="`outline-style:solid;outline-color:${getImportanceColor(dimension.id)};background-color:#${dimension.color}`"
                      >
                          <div class="level-item" :class="selectedDriver===dimension ? 'has-text-weight-bold' : ''">
                            {{ dimension.name }}
                          </div>
                      </a>
                      </div>

                  </div>
                </div>

              </div>
            </div>
            <br/>
            <button v-if="driver_filter=='suggested'" @click="driverStore.suggestDrivers()">Refresh Suggestions</button>
          </aside>
        </div>
        <div class="column">
          <main>
            <div v-if="selectedDriver" class="message is-link">
              <div class="message-header">
                <div class="level">
                  <!-- show the icon for the selected factor -- the driver or parent driver if a dimension -->
                  <img 
                    :src="'/images/' + driverStore.iconFilename(selectedFactor)"
                    class="level-left image is-32x32 mx-4"
                  />
                  <span class="level-left is-size-3">{{ selectedDriver.name }}</span>
                </div>
              </div>



              <div class="message-body">
                <!-- <div class="is-size-5"> -->
                <!-- <div v-if="selectedPrjDriver" class="columns"> -->
                  <!-- <div class="column is-narrow"> -->
                    <!-- <div class="notification is-link is-narrow"> -->
<div class="level">
  <div class="is-pulled-left">
                  <button
                    v-if="selectedPrjDriver == null"
                    class="button is-success"
                    @click="addDriver"
                  >
                    <span class="icon is-small">
                      <i class="fas fa-check"></i>
                    </span>
                    <span>Add</span>
                  </button>
                  <button
                    v-else
                    class="button is-danger"
                    @click="removeDriver"
                  >
                    <span class="icon is-small">
                      <i class="fas fa-times"></i>
                    </span>
                    <span class="has-text-centered">Remove</span>
                  </button>
                </div>

<div v-if="selectedPrjDriver" class="is-pulled-right">
                      Importance:
                      <select
                        name="importance"
                        id="importance"
                        :value ="selectedPrjDriver.importance_id"
                        @change="setImportance"
                      >
                        <option
                          v-for="importance in lookupStore.importance"
                          :key="importance.id"
                          :value="importance.id"
                        >
                          {{ importance.name }}
                        </option>
                      </select>
</div>
<!-- </div> -->
                    <!-- </div> -->
                  <!-- </div> -->
                <!-- </div> -->
              </div>

                <div class="has-text-weight-bold is-italic is-size-5">
                  <!-- <p>
                    Category: {{ driverStore.lu_driver_categories[selectedDriver.category_id].name }}
                  </p> -->
                </div>


                <p>{{ selectedDriver.text_long }}</p>
                <br />

                <div v-if="driver_filter=='suggested'">
                  <span class="has-text-weight-bold is-italic is-size-5">Relevance to Project:</span> 
                  <br/>
                  <span v-if="selectedDriver">{{driverStore.suggestionExplanation(selectedDriver.id)}}</span>
                  <br/>
                  <br/>
                  <span class="has-text-weight-bold is-italic is-size-5">Example:</span> 
                  <br/>
                  <span v-if="selectedDriver">{{driverStore.suggestionExample(selectedDriver.id)}}</span>
                </div>
                <br/>
                <br/>
                <div 
                    class="has-text-weight-bold is-italic is-size-5"
                    v-if="interventionStore.interventionsByDriver(selectedDriver)"
                  >Interventions:
                  <br/>
                </div>
                <div
                  v-for="intervention in interventionStore.interventionsByDriver(
                    selectedDriver
                  )"
                  :key="intervention.key"
                >
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
            </div>
          </main>
        </div>
      </div>
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
