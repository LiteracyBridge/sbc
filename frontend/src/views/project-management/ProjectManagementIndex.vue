<script lang="ts" setup>
import { onMounted, ref, reactive, watch } from "vue";
import { Button, TabPane, Card, Tabs, Tag, Typography } from "ant-design-vue";

import ActivitiesTable from "./activities/ActivitiesTable.vue";
import RiskMitigation from "./RiskMitigation.vue";
import SustainabilityStrategy from './SustainabilityStrategy.vue';
import MyTasks from "./activities/MyTasks.vue";

const config = ref({
  activeTab: 'activities'
})


</script>

<template>
  <Card title="Project Management">
    <Tabs v-model:activeKey="config.activeTab" centered>
      <TabPane key="tasks" tab="My Tasks">
        <MyTasks></MyTasks>
      </TabPane>
      <TabPane key="activities" tab="Project Activities">
        <ActivitiesTable></ActivitiesTable>
      </TabPane>
      <TabPane key="risk" tab="Risk Mitigation Strategy">
        <RiskMitigation></RiskMitigation>
      </TabPane>
      <TabPane key="sustainability" tab="Sustainability Strategy">
        <SustainabilityStrategy></SustainabilityStrategy>
      </TabPane>
    </Tabs>
  </Card>
</template>

<style>
</style>
