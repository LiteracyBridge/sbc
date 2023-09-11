<script lang="ts" setup>
import { DownOutlined, PlusCircleOutlined } from "@ant-design/icons-vue";
import {
  Tag,
  Table,
  Divider,
  Button,
  Space,
  Typography,
  Modal,
  DescriptionsItem,
  Descriptions,
  Tabs,
  TabPane,
  Empty,
  Spin,
} from "ant-design-vue";
import { onMounted, ref } from "vue";

import MonitoringEditModal from "./MonitoringEditModal.vue";
import ProgressTrackingModal from "./ProgressTrackingModal.vue";
import AddMonitoringIndicatorModal from "./AddMonitoringIndicatorModal.vue";
import EvaluationStrategy from "./EvaluationStrategy.vue";
import { useMonitoringStore } from "@/stores/monitoring.store";
import { useTheoryOfChangeStore } from "@/stores/theory_of_change";
import { Monitoring } from "@/types";

const store = useMonitoringStore();

const config = ref({
  activeTab: "1",
  isLoading: false,
  selectedRow: undefined,
  editModalVisible: false,
  indicatorModalVisible: false,
  evaluationForm: {
    evaluation_strategy: "",
    feedback_strategy: "",
  },
  evaluationModal: {
    visible: false,
    onClose: () => {
      config.value.evaluationModal.visible = false;
    },
  },
  progressTrackingModal: {
    visible: false,
    form: {
      value: "",
      period: "",
    },
    onClose: () => {
      config.value.progressTrackingModal.visible = false;
    },
  },
});

const columns = [
  {
    title: "Theory of Change",
    key: "tocItem",
  },
  {
    title: "Indicator",
    name: "Indicator",
    dataIndex: "indicator",
    key: "indicator",
  },
  {
    title: "Data Collection Method",
    name: "Data Collection Method",
    dataIndex: "data_collection_method",
    key: "data_collection_method",
  },
  {
    title: "Reporting Period",
    key: "reporting_period",
  },
  {
    dataIndex: "target",
    title: "Target",
    key: "target",
  },
  {
    dataIndex: "baseline",
    title: "Baseline",
    key: "baseline",
  },
  {
    title: "Recent Progress",
    key: "recent",
  },
  {
    title: "Progress",
    key: "progress_rate",
  },
  {
    title: "Actions",
    key: "actions",
  },
];

onMounted(() => {
  store.download();
});

function getTypeColor(type?: string): string {
  if (!type) return null;

  switch (type.toLowerCase()) {
    case "qualitative":
      return "blue";
    case "quantitative":
      return "green";
    case "percentage":
      return "purple";
    default:
      return "white";
  }
}

function showEditModal(record: Monitoring) {
  config.value.selectedRow = record;
  config.value.editModalVisible = true;
  config.value.progressTrackingModal.visible = false;
}
</script>

<template>
  <MonitoringEditModal
    v-if="config.selectedRow != null"
    :visible="config.editModalVisible"
    :form="config.selectedRow"
    @is-closed="
      config.selectedRow = null;
      config.editModalVisible = false;
    "
  >
  </MonitoringEditModal>

  <AddMonitoringIndicatorModal
    :visible="config.indicatorModalVisible"
    @is-closed="config.indicatorModalVisible = false"
  >
  </AddMonitoringIndicatorModal>

  <ProgressTrackingModal
    v-if="config.selectedRow != null"
    :visible="config.progressTrackingModal.visible"
    @is-closed="config.progressTrackingModal.visible = true"
    :record="config.selectedRow"
  >
  </ProgressTrackingModal>

  <Spin :spinning="config.isLoading || store.loading">
    <Tabs v-model:activeKey="config.activeTab" centered>
      <TabPane key="1" tab="Indicators Monitoring">
        <Table :columns="columns" size="large" :data-source="store.data" bordered>
          <template #title>
            <div class="full-width">
              <div></div>

              <Button type="primary" @click.prevent="config.indicatorModalVisible = true">
                <template #icon>
                  <PlusCircleOutlined />
                </template>
                Add Indicator
              </Button>
            </div>
          </template>

          <template #bodyCell="{ column, record }">
            <template v-if="column.key === 'tocItem'">
              {{ record.toc_indicator?.theory_of_change?.name ?? "N/A" }}
            </template>

            <template v-if="column.key === 'indicator'">
              <span>
                {{
                  record.toc_indicator.name ||
                  record.toc_indicator?.indikit?.name ||
                  "N/A"
                }}
              </span>
              <Tag
                :color="getTypeColor(record.type)"
                class="ml-3"
                v-if="record.type != null"
                >{{ record.type }}</Tag
              >
            </template>

            <!-- <template v-if="column.key === 'relatedResults'">
              {{ record.name }}
            </template> -->

            <template v-if="column.key === 'data_collection_method'">
              {{ record.data_collection_method }}
            </template>

            <template v-if="column.key === 'reporting_period'">
              {{ record.reporting_period }}
            </template>

            <template v-else-if="column.key === 'target'">
              {{ record.target }}
            </template>

            <template v-else-if="column.key === 'baseline'">
              {{ record.baseline }}
            </template>

            <template v-else-if="column.key === 'recent'">
              <span v-if="store.getRecentProgress(record)?.value == null">N/A</span>

              <span v-else>
                {{ store.getRecentProgress(record).value }}
              </span>
            </template>

            <template v-else-if="column.key === 'progress_rate'">
              <!-- TODO: Should only display modal -->
              <Tag
                :color="getTypeColor(record.type)"
                @click.prevent="
                  config.selectedRow = record;
                  config.evaluationModal.visible = true;
                "
              >
                <span v-if="record.type == 'Quantitative' || record.type == 'Percentage'">
                  {{ record.progress || 0 }}%
                </span>
                <span v-else>
                  {{ store.getRecentProgress(record).value }}
                </span>
              </Tag>
            </template>

            <template v-else-if="column.key === 'actions'">
              <Space v-if="record.type != null">
                <Button
                  type="primary"
                  :ghost="true"
                  size="small"
                  @click.prevent="
                    config.selectedRow = record;
                    config.progressTrackingModal.visible = true;
                    config.editModalVisible = false;
                  "
                  >Record Progress</Button
                >

                <Button
                  size="small"
                  @click.prevent="showEditModal(record as Monitoring)"
                  >Edit</Button
                >

                <!-- TODO: add popconfirm -->
                <Button
                  type="primary"
                  :danger="true"
                  :ghost="true"
                  size="small"
                  @click.prevent="store.deleteIndicator(record.toc_indicator_id)"
                  >Delete
                </Button>
              </Space>

              <Button
                v-else
                type="primary"
                :ghost="true"
                size="small"
                @click.prevent="showEditModal(record as Monitoring)"
                >Setup</Button
              >
            </template>
          </template>
        </Table>
      </TabPane>

      <TabPane key="2" tab="Project Evaluation Strategy">
        <EvaluationStrategy></EvaluationStrategy>
      </TabPane>
    </Tabs>
  </Spin>

  <Modal
    v-model:open="config.evaluationModal.visible"
    title="Evaluation Periods"
    width="800px"
    @ok="
      config.evaluationModal.onClose();
      config.selectedRow = null;
    "
  >
    <template #footer></template>

    <Empty v-if="(config.selectedRow?.evaluation || []).length == 0"></Empty>

    <Descriptions v-else size="small" :label-style="{ fontWeight: 'bold' }">
      <DescriptionsItem
        v-for="item in config.selectedRow?.evaluation || []"
        :label="item.period"
      >
        {{ item.value }}
      </DescriptionsItem>
    </Descriptions>
  </Modal>
</template>
