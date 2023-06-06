<script lang="ts" setup>
// TODO: add button for viewing progress in a modal
// TODO: add button for capturing progress in a modal

import { ApiRequest } from '@/apis/api';
import { useProjectStore } from '@/stores/projects';
import { Monitoring } from '@/types';
import { SmileOutlined, DownOutlined, PlusCircleOutlined, SettingOutlined } from '@ant-design/icons-vue';
import { Tag, Table, Divider, Button, Space, Typography, ButtonGroup, Modal, DescriptionsItem, Descriptions, Form, FormItem, Input, Select, SelectOption, Tabs, TabPane, Textarea, Spin } from 'ant-design-vue';
import { onMounted, ref } from 'vue';
import MonitoringEditModal from './MonitoringEditModal.vue';

const projectStore = useProjectStore();

const monitoringData = ref<Array<Monitoring>>([]);
const config = ref({
    activeTab: '1',
    isLoading: false,
    selectedMonitoring: undefined,
    editModalVisible: false,
    evaluationForm: {
        evaluation_strategy: '',
        feedback_strategy: '',
    },
    settingsModal: {
        visible: false,
        onClose: () => {
            config.value.settingsModal.visible = false;
        },
        form: {
            evaluation_period: '',
        }
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
        title: 'Indicator ID',
        name: 'Indicator ID',
        dataIndex: 'indicatorId',
        key: 'indicatorId',
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

const data = [
    {
        key: '1',
        name: 'John Brown',
        age: 32,
        address: 'New York No. 1 Lake Park',
        tags: ['nice', 'developer'],
    },
    {
        key: '2',
        name: 'Jim Green',
        age: 42,
        address: 'London No. 1 Lake Park',
        tags: ['loser'],
    },
    {
        key: '3',
        name: 'Joe Black',
        age: 32,
        address: 'Sidney No. 1 Lake Park',
        tags: ['cool', 'teacher'],
    },
];

function fetchData() {
    config.value.isLoading = true;

    ApiRequest.get<Monitoring>(`monitoring/${projectStore.projectId}/`)
        .then((resp) => {
            console.warn(resp)
            monitoringData.value = resp;
        })
        .finally(() => config.value.isLoading = false)
}

onMounted(() => {
    fetchData();
});
</script>

<template>
    <MonitoringEditModal v-if="config.selectedMonitoring != null" :visible="config.editModalVisible"
        :form="config.selectedMonitoring" @is-closed="config.selectedMonitoring = null; config.editModalVisible = false;"
        @is-updated="monitoringData = $event">
    </MonitoringEditModal>

    <Spin :spinning="config.isLoading">
        <Tabs v-model:activeKey="config.activeTab" centered class="my-3 mx-3">
            <TabPane key="1" tab="Indicators Monitoring">
                <Table :columns="columns" :data-source="monitoringData" bordered>
                    <template #title>
                        <div class="level">
                            <div class="level-left">
                                <Typography :level="3">Indicators Monitoring</Typography>
                            </div>

                            <div class="level-right">
                                <Space>
                                    <Button type="primary">
                                        <template #icon>
                                            <PlusCircleOutlined />
                                        </template>
                                        Add Indicator
                                    </Button>

                                    <Button type="ghost" @click="config.settingsModal.visible = true">
                                        <template #icon>
                                            <SettingOutlined />
                                        </template>
                                        Settings
                                    </Button>
                                </Space>
                            </div>
                        </div>
                    </template>

                    <template #bodyCell="{ column, record }">
                        <template v-if="column.key === 'indicatorId'">
                            {{ record.name }}
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

                        <template v-else-if="column.key === 'tags'">
                            <span>
                                <Tag v-for="tag in record.tags" :key="tag"
                                    :color="tag === 'loser' ? 'volcano' : tag.length > 5 ? 'geekblue' : 'green'">
                                    {{ tag.toUpperCase() }}
                                </Tag>
                            </span>
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
                            <Tag @click="config.evaluationModal.visible = true">{{ record.progress || 0 }}%</Tag>
                        </template>

                        <template v-else-if="column.key === 'actions'">
                            <Space>
                                <Button type="primary" :ghost="true" size="small"
                                    @click="config.progressTrackingModal.visible = true">Record
                                    Progress</Button>

                                <!-- TODO: should open edit modal -->
                                <Button type="primary" :danger="true" :ghost="true" size="small"
                                    @click="config.selectedMonitoring = record; config.editModalVisible = true;">Edit</Button>
                            </Space>
                        </template>
                    </template>
                </Table>
            </TabPane>

            <TabPane key="2" tab="Project Evaluation Strategy">

                <Form class="mx-6" layout="vertical" name="evaluation_strategy_form">
                    <!-- TODO: Implement saving of form -->

                    <FormItem label="How will you evaluate the impact of our project? (evaluation strategy narrative)"
                        name="evaluation_strategy"
                        :rules="[{ required: true, message: 'Please input your evaluation strategy!' }]">
                        <Textarea v-model:value="config.evaluationForm.evaluation_strategy" :rows="8"></Textarea>
                    </FormItem>

                    <FormItem label="How will you gather and respond to feedback from participants and stakeholders?"
                        name="feedback_strategy"
                        :rules="[{ required: true, message: 'Please input your feedback strategy!' }]">
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
        @ok="config.evaluationModal.onClose()">
        <template #footer></template>

        <Descriptions size="small">
            <DescriptionsItem label="Week 1">Cloud Database</DescriptionsItem>
            <DescriptionsItem label="Week 2">Prepaid</DescriptionsItem>
            <DescriptionsItem label="Week 3">18:00:00</DescriptionsItem>
            <DescriptionsItem label="Week 6">$80.00</DescriptionsItem>
            <DescriptionsItem label="Week 7">$20.00</DescriptionsItem>
            <DescriptionsItem label="Week 9">$60.00</DescriptionsItem>
        </Descriptions>
    </Modal>


    <Modal v-model:visible="config.progressTrackingModal.visible" title="Record Progress"
        @ok="config.progressTrackingModal.onClose()">

        <Form layout="vertical" name="progress_tracking_form">

            <!-- TODO: exclude already tracked periods from dropdown -->
            <FormItem name="period" label="Select Period" has-feedback
                :rules="[{ required: true, message: 'Please select a period!' }]">
                <Select v-model:value="config.progressTrackingModal.form.period" placeholder="Please period"
                    :show-search="true">
                    <SelectOption value="week 1">Week 1</SelectOption>
                    <SelectOption value="week 2">Week 2</SelectOption>
                    <SelectOption value="week 3">Week 3</SelectOption>
                </Select>
            </FormItem>

            <FormItem label="Value" name="value" :rules="[{ required: true, message: 'Please input your username!' }]">
                <Input v-model:value="config.progressTrackingModal.form.value" />
            </FormItem>
        </Form>
    </Modal>


    <Modal v-model:visible="config.settingsModal.visible" title="Record Progress" @ok="config.settingsModal.onClose()">

        <Form layout="vertical" name="settings" :model="config.settingsModal.form">

            <!-- TODO: Make this one time configuration -->
            <FormItem name="period" label="Select Evaluation Period" has-feedback
                :rules="[{ required: true, message: 'Please select an evaluation period!' }]">
                <Select v-model:value="config.settingsModal.form.evaluation_period"
                    placeholder="Please select evaluation period" :show-search="true">
                    <SelectOption value="weekly">Weekly</SelectOption>
                    <SelectOption value="monthly">Monthly</SelectOption>
                </Select>
            </FormItem>
        </Form>

    </Modal>
</template>
