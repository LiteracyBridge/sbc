<script lang="ts" setup>
import { onMounted, ref, reactive } from "vue";
import {
  Descriptions,
  DescriptionsItem,
  Modal,
  Spin,
  Table,
  Button,
  Typography,
} from "ant-design-vue";
import { SwapOutlined } from "@ant-design/icons-vue";
import RiskModal from "../theory-of-change/RiskModal.vue";
import { Activity, Risk } from "@/types";
import { useTheoryOfChangeStore } from "@/stores/theory_of_change";
import { truncate } from "lodash-es";

const store = useTheoryOfChangeStore();
const modal = ref({
  visible: false,
  selectedRisk: null as Risk | null,
});
const editModal = ref({
  visible: false,
  risk: { toc_from_id: null, toc_to_id: null },
});

const columns = [
  {
    title: "Theory of Change Item",
    key: "toc",
    ellipsis: true,
  },
  {
    title: "Risk",
    key: "risk",
  },
  {
    title: "Assumptions",
    key: "assumptions",
    ellipsis: true,
  },
  {
    title: "Mitigation Strategy",
    key: "mitigation",
    ellipsis: true,
  },
  {
    title: "",
    key: "action",
  },
];
</script>

<template>
  <!-- Risk Edit Modal -->
  <RiskModal
    :visible="editModal.visible"
    @close="
      editModal.risk = { toc_from_id: null, toc_to_id: null };
      editModal.visible = false;
    "
    :edge="editModal.risk"
  ></RiskModal>

  <Table
    :columns="columns"
    :data-source="store.risks"
    bordered
    :loading="store.isLoading"
    size="small"
  >
    <!-- <template #title>
        Risk Mitigation Strategy
      </template> -->

    <template #bodyCell="{ column, record }">
      <template v-if="column.key === 'toc'">
        <Button
          type="link"
          @click="
            modal.selectedRisk = record;
            modal.visible = true;
          "
        >
          <span v-if="record.toc_from_id != null && record.toc_to_id != null">
            {{ record.toc_from?.name }}
            <SwapOutlined />
            {{ record.toc_to?.name }}
          </span>

          <span v-else>
            {{ record.toc_from?.name || record.toc_to?.name || "N/A" }}
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

      <template v-if="column.key === 'action'">
        <Button
          size="small"
          @click.prevent="
            editModal.risk = record;
            editModal.visible = true;
          "
          type="primary"
          :ghost="true"
          :danger="true"
          >Edit</Button
        >
      </template>
    </template>
  </Table>

  <Modal
    :visible="modal.visible"
    :title="modal.selectedRisk?.name"
    @closed="
      modal.visible = false;
      modal.selectedRisk = null;
    "
  >
    <template #footer>
      <Button
        @click="
          modal.visible = false;
          modal.selectedRisk = null;
        "
      >
        Close
      </Button>
    </template>

    <Descriptions layout="vertical" :column="1">
      <DescriptionsItem label="Risks" :label-style="{ fontWeight: 'bold' }"
        ><span class="preserve-whitespace">{{ modal.selectedRisk?.risks }}</span>
      </DescriptionsItem>
      <DescriptionsItem label="Assumptions" :label-style="{ fontWeight: 'bold' }"
        ><span class="preserve-whitespace">{{ modal.selectedRisk?.assumptions }}</span>
      </DescriptionsItem>
      <DescriptionsItem label="Mitigation" :label-style="{ fontWeight: 'bold' }">
        <span class="preserve-whitespace">{{ modal.selectedRisk?.mitigation }}</span>
      </DescriptionsItem>
    </Descriptions>
  </Modal>
</template>

<style></style>
