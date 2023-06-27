<script setup lang="ts">

import { onMounted, ref } from 'vue';

import { PlusOutlined } from '@ant-design/icons-vue';
import {
  Card, CollapsePanel, Collapse,
  Descriptions, DescriptionsItem,
  Button, Space, Form, type FormInstance,
  FormItem, Input, Textarea,
  Select, SelectOption,
  Drawer, Spin, Popconfirm, Empty
} from 'ant-design-vue';
import { useProjectDataStore } from '@/stores/projectData';
import { useTheoryOfChangeStore } from '@/stores/theory_of_change';
import { useCommunicationStore } from '@/stores/communication.store';
import { Communication } from '@/types';
import { useDriverStore } from '@/stores/drivers';

const projectDataStore = useProjectDataStore(),
  tocStore = useTheoryOfChangeStore(),
  store = useCommunicationStore();

const config = ref({
  loading: false,
  collapseKey: '',
  selectedItem: {} as Communication,
  modal: {
    visible: false,
    form: {
      id: null,
      project_objectives: [] as number[],
      drivers: [] as number[],
      indicators: [] as number[],
      target_audiences: [] as number[],
      message_objectives: '',
      delivery_platforms: '',
      format: '',
      key_points: '',
      contents: '',
      title: '',
    }
  }
});
const communicationFormRef = ref<FormInstance>();

function closeModal() {
  config.value.modal.visible = false;
  config.value.modal.form = {
    id: null,
    project_objectives: [] as number[],
    drivers: [] as number[],
    indicators: [] as number[],
    target_audiences: [] as number[],
    message_objectives: '',
    delivery_platforms: '',
    format: '',
    key_points: '',
    contents: '',
    title: '',
  };
  communicationFormRef.value.resetFields();
}

function saveForm() {
  communicationFormRef.value.validateFields().then((values) => {
    store.create(config.value.modal.form).then((response) => {
      closeModal();
    });
  }).catch((error) => {
    console.log(error);
  })
}

function onEditClick(item: Communication) {
  communicationFormRef.value?.resetFields();

  config.value.modal.form = {
    ...item,
    project_objectives: item.project_objectives.map((obj) => obj.objective_id),
    indicators: item.indicators.map((obj) => obj.indicator_id),
    target_audiences: item.target_audiences.map((obj) => obj.audience_id),
    drivers: item.drivers.map((obj) => obj.driver_id),
  };
  config.value.modal.visible = true;
}

onMounted(() => {
  store.download();
})
</script>

<template>
  <Card title="Communications and Messaging">
    <template #extra>
      <Button type="primary" @click="config.modal.visible = true">
        <template #icon>
          <PlusOutlined />
        </template>
        New Communication Message
      </Button>

    </template>

    <Spin :spinning="store.loading">
      <Empty v-if="store.data.length === 0"></Empty>

      <Collapse v-model:activeKey="config.collapseKey">
        <CollapsePanel v-for="item in store.data" :key="item.id" :header="item.title">

          <template #extra>
            <Space>
              <Button type="primary" :ghost="true" size="small" role="button" @click.prevent="onEditClick(item)">
                Edit
              </Button>

              <Popconfirm title="Are you sure delete this message?" ok-text="Yes" cancel-text="No"
                @confirm="store.delete(item.id)">

                <Button type="primary" :ghost="true" danger size="small">
                  Delete
                </Button>
              </Popconfirm>
            </Space>
          </template>

          <Descriptions size="small" bordered layout="vertical">
            <DescriptionsItem :content-style="{ 'max-width': '50px' }" :span="24" label="Target Project Objectives">{{
              store.projectObjectives(item.id)?.map((obj) => obj.data).join(', ') || 'N/A' }}
            </DescriptionsItem>

            <!-- TODO: Implement related indicators -->
            <DescriptionsItem label="Related indicator(s)">{{
              store.indicators(item.id)?.map((obj) => obj.name).join(', ') || 'N/A' }}
            </DescriptionsItem>

            <DescriptionsItem label="Target audience(s)">{{
              store.targetAudiences(item.id)?.map((obj) => obj.data).join(', ') || 'N/A' }}
            </DescriptionsItem>

            <DescriptionsItem label="Target Behavioral Driver(s)">
              {{
                store.behavioralDrivers(item.id)?.map((obj) => obj.name).join(', ') || 'N/A' }}
            </DescriptionsItem>

            <DescriptionsItem label="Message Objectives">
              <span class="preserve-whitespace">
                {{ item.message_objectives || 'N/A' }}
              </span>
            </DescriptionsItem>

            <DescriptionsItem label="Message Delivery Platform">
              <span class="preserve-whitespace">
                {{ item.delivery_platforms || 'N/A' }}
              </span>
            </DescriptionsItem>

            <DescriptionsItem label="Message format">
              <span class="preserve-whitespace">
                {{ item.format || 'N/A' }}
              </span>
            </DescriptionsItem>

            <DescriptionsItem label="Key Points">
              <span class="preserve-whitespace">
                {{ item.key_points || 'N/A' }}
              </span>
            </DescriptionsItem>

            <DescriptionsItem label="Message content">
              <span class="preserve-whitespace">
                {{ item.contents || 'N/A' }}
              </span>
            </DescriptionsItem>

          </Descriptions>

        </CollapsePanel>
      </Collapse>
    </Spin>

  </Card>

  <Drawer v-model:visible="config.modal.visible" width="650px" :mask-closable="false" @close="closeModal">
    <template #title>
      {{ config.modal.form?.id != null ? 'Update' : 'New' }} Communication
    </template>

    <template #extra>
      <Space>
        <Button type="primary" @click="saveForm">
          {{ config.modal.form?.id != null ? 'Update' : 'Save' }}
        </Button>

        <Button @click="closeModal">Cancel</Button>
      </Space>
    </template>

    <Spin :spinning="store.loading">
      <Form name="communications-form" ref="communicationFormRef" :model="config.modal.form" layout="vertical">

        <FormItem name="title" label="Message Title" has-feedback
          :rules="[{ required: true, message: 'Please enter message title' }]">

          <Input v-model:value="config.modal.form.title"> </Input>
        </FormItem>


        <FormItem name="project_objectives" label="Project objectives" has-feedback
          :rules="[{ required: true, message: 'Please select project objectives!' }]">
          <Select v-model:value="config.modal.form.project_objectives" placeholder="Select project objectives"
            mode="multiple" :show-search="true">
            <SelectOption v-for="obj in projectDataStore.specificObjectives" :value="obj.id" :key="obj.id">{{
              obj.data }}</SelectOption>
          </Select>
        </FormItem>

        <FormItem name="drivers" label="Target Behavioral Drivers" has-feedback
          :rules="[{ required: true, message: 'Please select target drivers!' }]">

          <Select v-model:value="config.modal.form.drivers" placeholder="Select target drivers" mode="multiple"
            :show-search="true">
            <SelectOption v-for="obj in useDriverStore().driversInProject" :value="obj.id" :key="obj.id">{{
              obj.name }}
            </SelectOption>
          </Select>
        </FormItem>

        <FormItem name="indicators" label="Related Indicators" has-feedback
          :rules="[{ required: false, message: 'Please select related indicators!' }]">
          <Select v-model:value="config.modal.form.indicators" placeholder="Select related indicators" mode="multiple"
            :show-search="true">
            <SelectOption v-for="obj in useTheoryOfChangeStore().allTocIndicators" :value="obj.id" :key="obj.id">{{
              obj.name }}
            </SelectOption>
          </Select>
        </FormItem>

        <FormItem name="target_audiences" label="Target Audiences" has-feedback
          :rules="[{ required: true, message: 'Please select target audiences!' }]">
          <Select v-model:value="config.modal.form.target_audiences" placeholder="Select target audiences" mode="multiple"
            :show-search="true">
            <SelectOption v-for="obj in useProjectDataStore().audiences" :value="obj.id" :key="obj.id">{{ obj.data }}
            </SelectOption>
          </Select>
        </FormItem>

        <!-- FIXME: Add target behaviour drivers -->

        <FormItem name="message_objectives" label="Message Objectives" has-feedback
          :rules="[{ required: true, message: 'Please enter message objectives' }]">

          <Textarea v-model:value="config.modal.form.message_objectives"> </Textarea>
        </FormItem>

        <FormItem name="delivery_platforms" label="Message Delivery Platforms" has-feedback
          :rules="[{ required: true, message: 'Please enter message delivery platforms' }]">

          <Textarea v-model:value="config.modal.form.delivery_platforms"> </Textarea>
        </FormItem>

        <FormItem name="format" label="Message Format" has-feedback
          :rules="[{ required: true, message: 'Please enter message format!' }]">

          <Textarea v-model:value="config.modal.form.format"></Textarea>
        </FormItem>

        <FormItem name="key_points" label="Message Key Points" has-feedback
          :rules="[{ required: true, message: 'Please enter message key points!' }]">

          <Textarea v-model:value="config.modal.form.key_points" name="key_points"></Textarea>
        </FormItem>

        <FormItem name="contents" label="Message Contents" has-feedback
          :rules="[{ required: true, message: 'Please enter message content!' }]">

          <Textarea v-model:value="config.modal.form.contents" name="contents"></Textarea>
        </FormItem>
      </Form>

    </Spin>
  </Drawer>
</template>
