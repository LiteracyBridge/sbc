<script lang="ts" setup>
import { onMounted, ref, reactive, watch } from "vue";
import { Button, TabPane, Table, Tabs, Tag, Typography } from "ant-design-vue";

import ActivitiesTable from "./activities/ActivitiesTable.vue";
import RiskMitigation from "./RiskMitigation.vue";
import SustainabilityStrategy from './SustainabilityStrategy.vue';

const config = ref({
  activeTab: 'activities'
})


</script>

<template>
  <section class="section">
    <Tabs v-model:activeKey="config.activeTab" centered class="my-3 mx-3">
      <TabPane key="activities" tab="Activities">
        <ActivitiesTable></ActivitiesTable>
      </TabPane>
      <TabPane key="risk" tab="Risk Mitigation Strategy">
        <RiskMitigation></RiskMitigation>
      </TabPane>
      <TabPane key="sustainability" tab="Sustainability Strategy">
        <SustainabilityStrategy></SustainabilityStrategy>
      </TabPane>
    </Tabs>
  </section>
</template>

<style>
</style>
