<script setup>
import { useDriverStore } from "../stores/drivers";
import { useLookupStore } from "../stores/lookups";
import { useActivityStore } from "../stores/activities";
import { useInterventionStore } from "../stores/interventions";
import { ref, onMounted } from "vue";
import { useUserStore } from "@/stores/user";
import { useRouter } from 'vue-router'

const userStore = useUserStore();
onMounted (()=>userStore.loggedIn ? null :  useRouter().push({ path: '/login'}));

const driverStore = useDriverStore();
const lookupStore = useLookupStore();
const activityStore = useActivityStore();
const interventionStore = useInterventionStore();

const selectedDriver = ref(null);
const selectedFactor = ref(null);
const selectedCategoryId = ref(null);
 


const setDriver = function (driver = null) {
  if (selectedDriver.value && selectedDriver.value == driver) {
    selectedDriver.value = null;
    selectedFactor.value = null;
  } else {
    if (driver.parent_id == 0) {
        selectedFactor.value = driver;
    } else if (selectedFactor.value.id != selectedDriver.value.parent_id) {        
        selectedFactor.value = driverStore.driverByLUid(driver.parent_id);
    }
    selectedDriver.value = driver;
  }
  top.scrollTo(0,0);
}

const getImportanceColor = (importanceId) => lookupStore.importance[importanceId] ? lookupStore.importance[importanceId].color : 'white';

</script>

<template>
  <section ref="top" class="section">
    <div class="container">
      <div class="columns">
        <div class="column is-narrow">
          <aside class="is-small menu">
            <div
              v-for="category in driverStore.lu_driver_categories"
              :key="category.id"
              @click="selectedCategoryId=category.id"
            >
              <p class="menu-label">{{ category.name }}</p>

<!-- COLLAPSE IF ANOTHER CATEGORY'S DRIVER IS SELECTED -->
              <div class="menu-list" v-if="selectedDriver ? selectedCategoryId === category.id : true ">
                <div
                  v-for="driver in driverStore.factorsByCategory(category.id)"
                  :key="driver.id"
                  class="ml-2 my-2 menu-item has-tool-tip-multiline"
                  :data-tooltip="driver.text_short ? driver.text_short : null"
                >
                  <a
                    href="#"
                    @click.prevent="setDriver(driver)"
                    class="level"
                    :class="driver.id === selectedDriver ? 'is-active' : ''"
                    :style="`outline-style:solid;outline-color:${getImportanceColor(driver.importance_id)};background-color:${driverStore.lu_driver_categories[driver.category_id].color}`"
                  >
                    <div class="level-left">
                      <div class="level-item" :class="selectedFactor===driver ? 'has-text-weight-bold' : ''">
                        {{ driver.name }}
                      </div>
                    </div>
                  </a>
                    <div v-if="selectedFactor==driver">
                        <div
                        v-for="dimension in driverStore.dimensionsByFactor(driver)"
                        :key="dimension.id"
                        class="ml-4 my-4 menu-item"
                        >
                        <a
                            href="#"
                            @click.prevent="setDriver(dimension)"
                            class="level"
                            :class="dimension.id === selectedDriver ? 'is-active' : ''"
                            :style="`outline-style:solid;outline-color:${getImportanceColor(dimension.importance_id)};background-color:#${dimension.color}`"
                        >
                            <div class="level-left">
                            <div class="level-item">{{ dimension.name }}</div>
                            </div>
                        </a>
                        </div>

                    </div>
                </div>

              </div>
            </div>
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
                <span class="has-text-weight-bold is-italic is-size-5"
                  >Category: {{ driverStore.lu_driver_categories[selectedDriver.category_id].name }}</span
                >
                <p>{{ selectedDriver.text_long }}</p>
                <br />
                <div class="columns">
                  <div class="column is-narrow">
                    <div class="notification is-primary is-narrow">
                      <p>Importance to this project:</p>
                      <select
                        name="importance"
                        id="importance"
                        v-model="selectedDriver.importance_id"
                        @change="driverStore.setImportance(selectedDriver.lu_id)"
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
                  </div>
                </div>

                <div>Interventions:</div>
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
                          @click="activityStore.addActivity({ name: intervention.name, driver_ids: [selectedDriver.lu_id], intervention_id: intervention.id })"
                          class="button is-success"
                        >
                          <span class="icon is-small">
                            <i class="fas fa-check"></i>
                          </span>
                          <span>Add to Project</span>
                        </button>
                        <button
                          v-if="interventionStore.activityIds(intervention.id).length"
                          @click="activityStore.deleteIntervention(intervention.id)"
                          class="button is-danger is-outlined "
                        >
                          <span class="icon is-small">
                            <i class="fas fa-times"></i>
                          </span>
                          <span>Remove from Project</span>
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
