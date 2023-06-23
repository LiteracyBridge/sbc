<script lang="ts" setup>
import { onMounted, ref, reactive, } from "vue";
import { useActivityStore } from "@/stores/activities";
import { useInterventionStore } from "@/stores/interventions";
import { useDriverStore } from "@/stores/drivers";
import { useLookupStore } from "@/stores/lookups";
import { useProjectStore } from '@/stores/projects'
import { Button, Space, Spin, Table, Tag, Typography } from "ant-design-vue";
import { PlusCircleOutlined } from "@ant-design/icons-vue";

// import AddActivityModal from './AddActivityModal.vue';
// import SubActivitiesDrawer from "./SubActivitiesDrawer.vue";
import { Activity } from "@/types";

const config = ref({
  loading: false,
  selectedActivity: null,
  subActivityModal: { visible: false },
});

const columns = [
  {
    title: 'Theory of Change Item',
    key: 'toc',
  },
  {
    title: 'Risk',
    key: 'risk',
  },
  {
    title: 'Strategy',
    key: 'strategy',
  },
]
</script>

<template>
  <Spin :spinning="config.loading">

    <Table :columns="columns" :data-source="[]" bordered>
      <!-- <template #title>
        Risk Mitigation Strategy
      </template> -->

      <template #bodyCell="{ column, record }">
        <template v-if="column.key === 'name'">

        </template>

      </template>
    </Table>
  </Spin>
</template>

<style>
</style>
