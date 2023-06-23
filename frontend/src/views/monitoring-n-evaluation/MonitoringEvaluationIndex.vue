<script lang="ts" setup>
// TODO: add button for viewing progress in a modal
// TODO: add button for capturing progress in a modal

import { ApiRequest } from '@/apis/api';
import { useProjectStore } from '@/stores/projects';
import { Monitoring } from '@/types';
import { SmileOutlined, DownOutlined, PlusCircleOutlined, SettingOutlined } from '@ant-design/icons-vue';
import { Tag, Table, Divider, Button, Space, Typography, ButtonGroup, Modal, DescriptionsItem, Descriptions, Form, FormItem, Input, Select, SelectOption, Tabs, TabPane, Textarea, Spin, message } from 'ant-design-vue';
import { onMounted, ref } from 'vue';

import { useTheoryOfChangeStore } from '@/stores/theory_of_change';
import MonitoringEditModal from './MonitoringEditModal.vue';
import ProgressTrackingModal from './ProgressTrackingModal.vue';
import AddMonitoringIndicatorModal from './AddMonitoringIndicatorModal.vue';
import { useMonitoringStore } from '@/stores/monitoring.store';

const projectStore = useProjectStore(),
  theoryOfChangeStore = useTheoryOfChangeStore(),
  store = useMonitoringStore();

// const monitoringData = ref<Array<Monitoring>>([]);
const config = ref({
  activeTab: '1',
  isLoading: false,
  selectedRow: undefined,
  editModalVisible: false,
  indicatorModalVisible: false,
  evaluationForm: {
    evaluation_strategy: '',
    feedback_strategy: '',
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
      value: '',
      period: ''
    },
    onClose: () => {
      config.value.progressTrackingModal.visible = false;
    },
  },
});


const columns = [
  {
    title: 'Theory of Change Item',
    dataIndex: 'tocItem',
    key: 'tocItem',
  },
  {
    title: 'Indicator',
    name: 'Indicator',
    dataIndex: 'indicator',
    key: 'indicator',
  },
  {
    title: 'Related Results',
    name: 'Related Results',
    dataIndex: 'relatedResults',
    key: 'relatedResults',
  },
  {
    title: 'Date Collection Method',
    name: 'Date Collection Method',
    dataIndex: 'data_collection_method',
    key: 'data_collection_method',
  },
  {
    title: 'Frequency of Data Collection',
    key: 'data_collection_frequency',
    dataIndex: 'data_collection_frequency',
  },
  {
    dataIndex: 'target',
    title: 'Target',
    key: 'target',
  },
  {
    dataIndex: 'baseline',
    title: 'Baseline',
    key: 'baseline',
  },

  // {
  //     title: 'Q1',
  //     key: 'qa',
  // },
  // {
  //     title: 'Q2',
  //     key: 'q2',
  // },
  {
    title: '% Progress',
    key: 'progress_rate',
  },
  {
    title: 'Actions',
    key: 'actions',
  },
];


// function fetchData() {
//   config.value.isLoading = true;

//   ApiRequest.get<Monitoring>(`monitoring/${projectStore.prj_id}`)
//     .then((resp) => {
//       monitoringData.value = resp;
//     })
//     .catch(err => message.error(err.message))
//     .finally(() => config.value.isLoading = false)
// }

onMounted(() => {
  store.download();
});

</script>

<template>
  <MonitoringEditModal v-if="config.selectedRow != null" :visible="config.editModalVisible" :form="config.selectedRow"
    @is-closed="config.selectedRow = null; config.editModalVisible = false;">
  </MonitoringEditModal>

  <AddMonitoringIndicatorModal :visible="config.indicatorModalVisible" @is-closed="config.indicatorModalVisible = false">
  </AddMonitoringIndicatorModal>

  <ProgressTrackingModal v-if="config.selectedRow != null" :visible="config.progressTrackingModal.visible"
    @is-closed="config.progressTrackingModal.visible = true" :record="config.selectedRow">
  </ProgressTrackingModal>

  <Spin :spinning="config.isLoading || store.loading">
    <Tabs v-model:activeKey="config.activeTab" centered class="my-3 mx-3">
      <TabPane key="1" tab="Indicators Monitoring">
        <Table :columns="columns" :data-source="store.data" bordered>
          <template #title>
            <div class="level">
              <div class="level-left">
                <Typography :level="3">Indicators Monitoring</Typography>
              </div>

              <div class="level-right">
                <Space>
                  <Button type="primary" @click="config.indicatorModalVisible = true">
                    <template #icon>
                      <PlusCircleOutlined />
                    </template>
                    Add Indicator
                  </Button>

                </Space>
              </div>
            </div>
          </template>

          <template #bodyCell="{ column, record }">
            <template v-if="column.key === 'tocItem'">
              {{ record.toc_item_indicator.toc_item.name }}
            </template>

            <template v-if="column.key === 'indicator'">
              {{ record.toc_item_indicator.indicator.name }}
            </template>

            <template v-if="column.key === 'relatedResults'">
              {{ record.name }}
            </template>

            <template v-if="column.key === 'data_collection_method'">
              {{ record.data_collection_method }}
            </template>

            <template v-if="column.key === 'data_collection_frequency'">
              {{ record.data_collection_frequency }}
            </template>

            <template v-else-if="column.key === 'action'">
              <span>
                <a>Invite 一 {{ record.name }}</a>
                <Divider type="vertical" />
                <a>Delete</a>
                <Divider type="vertical" />
                <a class="ant-dropdown-link">
                  More actions
                  <down-outlined />
                </a>
              </span>
            </template>

            <template v-else-if="column.key === 'target'">
              {{ record.target }}
            </template>

            <template v-else-if="column.key === 'baseline'">
              {{ record.baseline }}
            </template>

            <template v-else-if="column.key === 'progress_rate'">
              <!-- TODO: Should only display modal -->
              <Tag :color="'cyan'" @click="config.selectedRow = record; config.evaluationModal.visible = true">
                <Typography :level="'4'">{{ record.progress || 0 }}% </Typography>
              </Tag>
            </template>

            <template v-else-if="column.key === 'actions'">
              <Space>
                <Button type="primary" :ghost="true" size="small"
                  @click="config.selectedRow = record; config.progressTrackingModal.visible = true">Record
                  Progress</Button>

                <!-- TODO: should open edit modal -->
                <Button type="primary" :danger="true" :ghost="true" size="small"
                  @click="config.selectedRow = record; config.editModalVisible = true;">Edit</Button>
              </Space>
            </template>
          </template>
        </Table>
      </TabPane>

      <TabPane key="2" tab="Project Evaluation Strategy">

        <Form class="mx-6" layout="vertical" name="evaluation_strategy_form">
          <!-- TODO: Implement saving of form -->

          <FormItem label="How will you evaluate the impact of our project? (evaluation strategy narrative)"
            name="evaluation_strategy" :rules="[{ required: true, message: 'Please input your evaluation strategy!' }]">
            <Textarea v-model:value="config.evaluationForm.evaluation_strategy" :rows="8"></Textarea>
          </FormItem>

          <FormItem label="How will you gather and respond to feedback from participants and stakeholders?"
            name="feedback_strategy" :rules="[{ required: true, message: 'Please input your feedback strategy!' }]">
            <Textarea v-model:value="config.evaluationForm.feedback_strategy" :rows="8"></Textarea>
          </FormItem>

          <FormItem>
            <!-- TODO: center button -->
            <Space>
              <Button type="primary" html-type="submit">Submit</Button>
            </Space>
          </FormItem>
        </Form>

      </TabPane>
    </Tabs>
  </Spin>


  <Modal v-model:visible="config.evaluationModal.visible" title="Evaluation Periods" width="800px"
    @ok="config.evaluationModal.onClose(); config.selectedRow = null">
    <template #footer></template>

    <Descriptions size="small" :label-style="{ 'fontWeight': 'bold' }">
      <DescriptionsItem v-for="period in Object.keys(config.selectedRow.evaluation || {})" :label="period"> {{
        config.selectedRow.evaluation[period] }}</DescriptionsItem>
    </Descriptions>
  </Modal>
</template>
