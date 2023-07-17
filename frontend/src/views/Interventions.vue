<script lang="ts" setup>
import { useActivityStore } from "../stores/activities";
import { useInterventionStore } from "../stores/interventions";
import { ref, computed, onMounted } from "vue";
import {
  Button,
  Collapse,
  CollapsePanel,
  Empty,
  Spin,
  TabPane,
  Tabs,
  Typography,
  Card,
  Popconfirm
} from "ant-design-vue";
import { DeleteOutlined, PlusCircleOutlined } from "@ant-design/icons-vue";
import { groupBy } from "lodash-es";
import { useTheoryOfChangeStore } from "@/stores/theory_of_change";
import { TheoryOfChangeType } from "@/types";
import { useUserStore } from "@/stores/user";

const config = ref({
  activePanel: "",
  activeTab: "",
});

const tocStore = useTheoryOfChangeStore();
const activityStore = useActivityStore();
const interventionStore = useInterventionStore();
const selectedPrjDriver = ref(null);

function addIntervention(intervention: { name: string; id: number }) {
  let driver_ids: number[] = [];
  if (selectedPrjDriver.value) {
    driver_ids = [selectedPrjDriver.value.id];
  }

  tocStore
    .addTocItem({
      name: intervention.name,
      type_id: TheoryOfChangeType.Activity,
      intervention_id: intervention.id,
      driver_ids,
      editing_user_id: useUserStore().id,
    })
    .then(() => activityStore.download());
}

const drivers = computed(() => {
  const data = groupBy(
    interventionStore.project_drivers.map((d) => {
      return {
        ...d,
        interventions: interventionStore.interventions.filter((i) =>
          d.intervention_ids.includes(i.id)
        ),
      };
    }),
    "name"
  );
  return Object.keys(data).map((name) => {
    return {
      name,
      interventions: data[name].flatMap((i) => i.interventions),
    };
  });
});

onMounted(() => {
  interventionStore.downloadProjectDrivers().then(() => {
    if (interventionStore.project_drivers.length > 0) {
      config.value.activeTab = interventionStore.project_drivers[0].name;
    }
  });
});
</script>

<template>
  <Card title="SBC Approaches">
    <Spin :spinning="interventionStore.loading || tocStore.isLoading">
      <Empty v-if="drivers.length == 0">
        <template #description>
          <span>No intervention found!</span> <br />

          <RouterLink to="/drivers">
            Click to choose driver(s) to add interventions
          </RouterLink>
        </template>
      </Empty>

      <div v-else>
        <Typography.Title :level="5">Project Behavior Drivers</Typography.Title>

        <Tabs v-model:activeKey="config.activeTab" tab-position="left" type="card">
          <TabPane v-for="driver in drivers" :key="driver.name" :tab="driver.name">
            <Collapse v-model:activeKey="config.activePanel">
              <CollapsePanel
                v-for="intervention in driver.interventions"
                :key="intervention.key"
                :header="intervention.name"
              >
                <template #extra>
                  <Button
                    v-if="!interventionStore.activityIds(intervention.id).length"
                    @click="addIntervention(intervention)"
                    type="primary"
                    :ghost="true"
                    size="small"
                  >
                    <template #icon>
                      <PlusCircleOutlined />
                    </template>
                    Add
                  </Button>

                  <Popconfirm
                    title="Are you sure to delete this intervention? All associated tasks will be deleted as well!"
                    ok-text="Yes"
                    cancel-text="No"
                    @confirm="activityStore.deleteIntervention(intervention.id)"
                  >
                    <Button
                      v-if="interventionStore.activityIds(intervention.id).length"
                      type="primary"
                      :ghost="true"
                      :danger="true"
                      size="small"
                    >
                      <template #icon>
                        <DeleteOutlined />
                      </template>
                      Remove
                    </Button>
                  </Popconfirm>
                </template>

                <p class="is-italic">{{ intervention.text_short }}</p>
                <br />
                <p>{{ intervention.text_long }}</p>
              </CollapsePanel>
            </Collapse>
          </TabPane>
        </Tabs>
      </div>
    </Spin>
  </Card>
</template>
