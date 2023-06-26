<script lang="ts" setup>
import { onMounted, ref, reactive, } from "vue";
import { Button, Space, Spin, Table, Tag, Typography } from "ant-design-vue";
import { SwapOutlined } from "@ant-design/icons-vue";

import { Activity } from "@/types";
import { useTheoryOfChangeStore } from "@/stores/theory_of_change";

const store = useTheoryOfChangeStore();
const config = ref({
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
    title: 'Assumptions',
    key: 'assumptions',
    ellipsis: true,
  },
  {
    title: 'Mitigation Strategy',
    key: 'mitigation',
    ellipsis: true,
  },
]
</script>

<template>
  <Spin :spinning="store.isLoading">

    <Table :columns="columns" :data-source="store.risks" bordered>
      <!-- <template #title>
        Risk Mitigation Strategy
      </template> -->

      <template #bodyCell="{ column, record }">
        <template v-if="column.key === 'toc'">
          <span v-if="record.toc_from_id != null && record.toc_to_id != null">
            {{ record.toc_from?.name }}
            <SwapOutlined />
            {{ record.toc_to?.name }}
          </span>

          <span v-else>
            {{ record.toc_from?.name || record.toc_to?.name || 'N/A' }}
          </span>

        </template>

        <template v-if="column.key === 'risk'">
          {{ record.risks }}
        </template>

        <template v-if="column.key === 'assumptions'">
          {{ record.assumptions }}
        </template>

        <template v-if="column.key === 'mitigation'">
          {{ record.mitigation }}
        </template>

        <!-- TODO: Add edit button for adding strategy -->
      </template>
    </Table>
  </Spin>
</template>

<style>
</style>
