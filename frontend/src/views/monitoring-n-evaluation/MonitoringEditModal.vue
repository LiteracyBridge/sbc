<script lang="ts" setup>

import { ApiRequest } from '@/apis/api';
import { useMonitoringStore } from '@/stores/monitoring.store';
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
}>()

const store = useMonitoringStore();

const monitorEditFormRef = ref<FormInstance>(),
  config = ref({
    visible: props.visible,
  });


watch((props), (newProps) => {
  config.value.visible = newProps.visible;
}, { deep: true })

function closeModal() {
  monitorEditFormRef.value.resetFields();
  config.value.visible = false;

  emit('isClosed', true);
}

function saveForm() {
  monitorEditFormRef.value
    .validateFields()
    .then(values => {
      store.update(props.form.id, values).then((response) => {
        message.success('Monitoring record updated successfully!');

        closeModal();
      })
    });
}
</script>

<template>
  <Modal
    v-model:open="config.visible"
    :title="props.form?.toc_indicator?.indicator?.name"
    ok-text="Update"
    cancel-text="Cancel"
    @cancel="closeModal()"
    :mask-closable="false"
    @ok="saveForm"
  >
    <Spin :spinning="store.loading">
      <Form
        layout="vertical"
        ref="monitorEditFormRef"
        name="monitoring_edit"
        :model="props.form"
      >
        <Row :gutter="8">
          <Col :span="12">
            <FormItem
              name="data_collection_method"
              label="Data collection method"
              has-feedback
              :rules="[
                { required: false, message: 'Please input data collection method' },
              ]"
            >
              <Input v-model:value="props.form.data_collection_method" />
            </FormItem>
          </Col>
          <Col :span="12">
            <FormItem
              name="type"
              label="Monitoring Type"
              has-feedback
              :rules="[{ required: true, message: 'Please select monitoring type!' }]"
            >
              <Select
                v-model:value="props.form.type"
                placeholder="Select monitoring type"
                :show-search="true"
              >
                <SelectOption value="Qualitative">Qualitative</SelectOption>
                <SelectOption value="Quantitative">Quantitative (#)</SelectOption>
                <SelectOption value="Percentage">Percentage (%)</SelectOption>
              </Select>
            </FormItem>
          </Col>
        </Row>

        <Row :gutter="6">
          <Col :span="12">
            <FormItem label="Baseline" name="baseline">
              <Input v-model:value="props.form.baseline" type="text" />
            </FormItem>
          </Col>

          <Col :span="12">
            <FormItem label="Target" name="target">
              <Input v-model:value="props.form.target" type="text" />
            </FormItem>
          </Col>
        </Row>

        <FormItem
          name="reporting_period"
          label="Reporting Period"
          has-feedback
          :rules="[{ required: true, message: 'Select a reporting period!' }]"
        >
          <Select
            v-model:value="props.form.reporting_period"
            placeholder="Select reporting period"
            :show-search="true"
          >
            <SelectOption value="Weekly">Weekly</SelectOption>
            <SelectOption value="Monthly">Monthly</SelectOption>
            <SelectOption value="quarterly">Quarterly</SelectOption>
            <SelectOption value="Semi-Annually">Semi-Annually</SelectOption>
            <SelectOption value="Annually">Annually</SelectOption>
          </Select>
        </FormItem>
      </Form>
    </Spin>
  </Modal>
</template>
