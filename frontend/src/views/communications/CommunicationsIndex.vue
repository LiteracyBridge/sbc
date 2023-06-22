<script setup lang="ts">

import { onMounted, ref } from 'vue';

import { PlusOutlined } from '@ant-design/icons-vue';
import {
  Card, CollapsePanel, Collapse,
  Descriptions, DescriptionsItem,
  Button, Space, Form, type FormInstance,
  FormItem, Input, Textarea,
  Select, SelectOption,
  Drawer, Spin
} from 'ant-design-vue';
import { useProjectDataStore } from '@/stores/projectData';
import { useTheoryOfChangeStore } from '@/stores/theory_of_change';
import { useCommunicationStore } from '@/stores/communication.store';

const projectDataStore = useProjectDataStore(),
  tocStore = useTheoryOfChangeStore(),
  store = useCommunicationStore();

const config = ref({
  loading: false,
  collapseKey: '',
  modal: {
    visible: false,
    form: {
      project_objectives: [] as number[],
      indicators: [] as number[],
      target_audiences: [] as number[],
      behavioral_drivers: [] as number[],
      message_objectives: '',
      delivery_platforms: '',
      format: '',
      key_points: '',
      content: '',
      title: '',
    }
  }
});
const communicationFormRef = ref<FormInstance>();

function closeModal() {
  config.value.modal.visible = false;
  communicationFormRef.value.resetFields();
}

function saveForm() {
  communicationFormRef.value.validateFields().then((values) => {
    console.log(values);

    store.create(config.value.modal.form).then((response) => {
      console.log(response);

      closeModal();
    });
  }).catch((error) => {
    console.log(error);
  })
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
        Add
      </Button>

    </template>

    <Spin :spinning="store.loading">
      <Collapse v-model:activeKey="config.collapseKey">
        <CollapsePanel key="1" header="This is panel header 1">

          <Descriptions :column="2" bordered>
            <DescriptionsItem :labelStyle="{ 'font-weight': 'bold' }" label="Target project objective(s)">Cloud Database
            </DescriptionsItem>

            <DescriptionsItem :labelStyle="{ 'font-weight': 'bold' }" label="Related indicator(s)">Cloud Database
            </DescriptionsItem>

            <DescriptionsItem :labelStyle="{ 'font-weight': 'bold' }" label="Target audience(s)">Cloud Database
            </DescriptionsItem>

            <DescriptionsItem :labelStyle="{ 'font-weight': 'bold' }" label="Target behavioral driver(s)">Cloud Database
            </DescriptionsItem>

            <DescriptionsItem :labelStyle="{ 'font-weight': 'bold' }" label="Message objective(s)">Cloud Database
            </DescriptionsItem>

            <DescriptionsItem :labelStyle="{ 'font-weight': 'bold' }" label="Message delivery platform(s)">Cloud Database
            </DescriptionsItem>

            <DescriptionsItem :labelStyle="{ 'font-weight': 'bold' }" label="Message format">Cloud Database
            </DescriptionsItem>

            <DescriptionsItem :labelStyle="{ 'font-weight': 'bold' }" label="Key points">Cloud Database
            </DescriptionsItem>

            <DescriptionsItem :labelStyle="{ 'font-weight': 'bold' }" label="Message content">Cloud Database
            </DescriptionsItem>

          </Descriptions>

        </CollapsePanel>
      </Collapse>
    </Spin>

  </Card>

  <Drawer v-model:visible="config.modal.visible" width="600px" title="Add Communication" :mask-closable="false">

    <template #extra>
      <Space>
        <Button type="primary" @click="saveForm">Save</Button>

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

        <FormItem name="indicators" label="Related Indicators" has-feedback
          :rules="[{ required: false, message: 'Please select related indicators!' }]">
          <Select v-model:value="config.modal.form.indicators" placeholder="Select related indicators"
            mode="multiple" :show-search="true">
            <SelectOption v-for="obj in tocStore.project_indicators" :value="obj.id" :key="obj.id">{{ obj.name }}
            </SelectOption>
          </Select>
        </FormItem>

        <FormItem name="target_audiences" label="Target Audiences" has-feedback
          :rules="[{ required: true, message: 'Please select target audiences!' }]">
          <Select v-model:value="config.modal.form.target_audiences" placeholder="Select target audiences" mode="multiple"
            :show-search="true">
            <SelectOption v-for="obj in projectDataStore.specificObjectives" :value="obj.id" :key="obj.id">{{ obj.data }}
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

        <FormItem name="content" label="Message Contents" has-feedback
          :rules="[{ required: true, message: 'Please enter message content!' }]">

          <Textarea v-model:value="config.modal.form.content" name="content"></Textarea>
        </FormItem>
      </Form>

    </Spin>
  </Drawer>
</template>
