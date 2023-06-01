<script lang="ts" setup>
import { useActivityStore } from "../stores/activities";
import { useInterventionStore } from "../stores/interventions";
import { ref, computed } from "vue";
import { Button, Collapse, CollapsePanel } from "ant-design-vue";
import { CheckCircleOutlined, DeleteOutlined } from "@ant-design/icons-vue";

const config = ref({
  activePanel: ''
})

const activityStore = useActivityStore();
const interventionStore = useInterventionStore();
const selectedPrjDriver = ref(null);


function addIntervention(intervention: { name: string, id: number }) {
  let driver_ids: number[] = [];
  if (selectedPrjDriver.value) {
    driver_ids = [selectedPrjDriver.value.id];
  }
  activityStore.addActivity({ name: intervention.name, driver_ids, intervention_id: intervention.id })
}

const getInterventions = computed(() => {
  return interventionStore.interventions.filter((i) => {
    return i.name != 'Social movements';
  })
})

</script>

<template>
  <section class="section">
    <Collapse v-model:activeKey="config.activePanel">

      <CollapsePanel v-for="intervention in getInterventions" :key="intervention.key" :header="intervention.name">
        <template #extra>
          <Button v-if="!interventionStore.activityIds(intervention.id).length" @click="addIntervention(intervention)"
            type="primary" size="small" :ghost="true">
            <template #icon>
              <CheckCircleOutlined />
            </template>
            Add
          </Button>

          <Button v-if="interventionStore.activityIds(intervention.id).length"
            @click="activityStore.deleteIntervention(intervention.id)" type="ghost" :danger="true" size="small">
            <template #icon>
              <DeleteOutlined />
            </template>
            Remove
          </Button>

        </template>

        <p class="is-italic">{{ intervention.text_short }}</p>
        <br />
        <p>{{ intervention.text_long }}</p>
      </CollapsePanel>

    </Collapse>
  </section>
</template>
