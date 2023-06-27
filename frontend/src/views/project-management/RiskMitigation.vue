<script lang="ts" setup>
import { onMounted, ref, reactive, } from "vue";
import {
  Button, Descriptions, DescriptionsItem, Modal, Spin, Table,
  Tag, Typography
} from "ant-design-vue";
import { SwapOutlined } from "@ant-design/icons-vue";

import { Activity, Risk } from "@/types";
import { useTheoryOfChangeStore } from "@/stores/theory_of_change";

const store = useTheoryOfChangeStore();
const modal = ref({
  visible: false,
  selectedRisk: null as Risk | null
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

          <Button type="link" @click="modal.selectedRisk = record; modal.visible = true;">
            <span v-if="record.toc_from_id != null && record.toc_to_id != null">
              {{ record.toc_from?.name }}
              <SwapOutlined />
              {{ record.toc_to?.name }}
            </span>

            <span v-else>
              {{ record.toc_from?.name || record.toc_to?.name || 'N/A' }}
            </span>
          </Button>

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

  <Modal :visible="modal.visible" :title="modal.selectedRisk?.name">
    <template #footer>
      <Button @click="modal.visible = false; modal.selectedRisk = null">
        Close
      </Button>
    </template>

    <Descriptions layout="vertical" :column="1">
      <DescriptionsItem label="Risks" :label-style="{ 'fontWeight': 'bold' }"><span class="preserve-whitespace">{{
        modal.selectedRisk?.risks }}</span>
      </DescriptionsItem>
      <DescriptionsItem label="Assumptions" :label-style="{ 'fontWeight': 'bold' }"><span class="preserve-whitespace">{{
        modal.selectedRisk?.assumptions }}</span>
      </DescriptionsItem>
      <DescriptionsItem label="Mitigation" :label-style="{ 'fontWeight': 'bold' }">
        <span class="preserve-whitespace">{{ modal.selectedRisk?.mitigation }}</span>
      </DescriptionsItem>
    </Descriptions>
  </Modal>
</template>

<style>
</style>
