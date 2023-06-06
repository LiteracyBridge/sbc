<script lang="ts" setup>

import { ApiRequest } from '@/apis/api';
import type { Monitoring } from '@/types';
import {
  Modal, FormItem, Form, type FormInstance, Input,
  InputNumber, Row,
  Col, Select, Spin, SelectOption,
  message
} from 'ant-design-vue';
import { ref, watch } from 'vue';

const props = defineProps<{ visible: boolean, form: Monitoring }>();
const emit = defineEmits<{
  (e: 'isClosed', status: boolean): boolean,
  (e: 'isUpdated', data: Monitoring[]): void,
}>()

const monitorEditModalFormRef = ref<FormInstance>(),
  config = ref({
    visible: props.visible,
    isLoading: false,
  });


watch((props), (newProps) => {
  config.value.visible = newProps.visible;
}, { deep: true })

function closeModal() {
  monitorEditModalFormRef.value.resetFields();
  config.value.visible = false;

  emit('isClosed', true);
}

function saveForm() {
  monitorEditModalFormRef.value
    .validateFields()
    .then(values => {
      config.value.isLoading = true;

      ApiRequest.put<Monitoring>(`monitoring/${props.form.id}`, values)
        .then((response) => {
          message.success('Monitoring record updated successfully!');
          emit('isUpdated', response);

          closeModal();
        })
        .catch((error) => {
          message.error(error.message);

          console.log(error);
        })
        .finally(() => {
          config.value.isLoading = false;
        });
    });
}

</script>

<template>
  <!-- Monitory item edit modal -->
  <Modal v-model:visible="config.visible" title="Update Indicator Monitoring" ok-text="Update" cancel-text="Cancel"
    @cancel="closeModal()" :mask-closable="false" @ok="saveForm">

    <Spin :spinning="config.isLoading">
      <Form layout="vertical" ref="monitorEditModalFormRef" name="monitoring_edit" :model="props.form">

        <!-- TODO: exclude already tracked periods from dropdown -->
        <FormItem name="data_collection_method" label="Data collection method" has-feedback
          :rules="[{ required: false, message: 'Please input data collection method' }]">
          <Input v-model:value="props.form.data_collection_method" />
        </FormItem>

        <FormItem name="data_collection_frequency" label="Data collection frequency" has-feedback
          :rules="[{ required: false, message: 'Please input data collection frequency' }]">
          <Input v-model:value="props.form.data_collection_frequency" />
        </FormItem>


        <Row :gutter="6">
          <Col :span="12">
          <FormItem label="Baseline" name="baseline"
            :rules="[{ required: true, message: 'Please enter baseline value!' }]">
            <InputNumber v-model:value="props.form.baseline" :min="0" />
          </FormItem>
          </Col>

          <Col :span="12">
          <FormItem label="Target" name="target" :rules="[{ required: true, message: 'Please enter target value!' }]">
            <InputNumber v-model:value="props.form.target" :min="0" />
          </FormItem>
          </Col>
        </Row>

        <FormItem name="evaluation_period" label="Select Evaluation Period" has-feedback
          :rules="[{ required: true, message: 'Please select an evaluation period!' }]">
          <Select v-model:value="props.form.evaluation_period" placeholder="Please select evaluation period"
            :show-search="true">
            <SelectOption value="weekly">Weekly</SelectOption>
            <SelectOption value="monthly">Monthly</SelectOption>
          </Select>
        </FormItem>
      </Form>
    </Spin>

  </Modal>
</template>
