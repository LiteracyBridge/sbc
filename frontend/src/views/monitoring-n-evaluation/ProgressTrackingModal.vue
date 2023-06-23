<script lang="ts" setup>
// TODO: add button for viewing progress in a modal
// TODO: add button for capturing progress in a modal

import { ApiRequest } from '@/apis/api';
import { useMonitoringStore } from '@/stores/monitoring.store';
import { Monitoring } from '@/types';
import { Modal, Form, FormItem, Input, Select, SelectOption, Spin, type FormInstance, message } from 'ant-design-vue';
import { computed, h, ref, watch } from 'vue';


const props = defineProps<{ visible: boolean, record: Monitoring }>();
const emit = defineEmits<{
  (e: 'isClosed', status: boolean): boolean,
}>()

const store = useMonitoringStore();
const progressTrackingFormRef = ref<FormInstance>(),
  config = ref({
    visible: props.visible,
    form: {
      value: '',
      period: ''
    }
  });


watch((props), (newProps) => {
  config.value.visible = newProps.visible;
}, { deep: true })

function closeModal() {
  progressTrackingFormRef.value.resetFields();
  config.value.visible = false;

  emit('isClosed', true);
}

function recordProgress() {
  if ((props.record?.target ?? 0) <= 0) {
    Modal.error({
      title: 'Indicator target required',
      content: h('div', {}, [
        h('p', 'Please set a target first!'),
      ])
    });
    return;
  }

  progressTrackingFormRef.value
    .validateFields()
    .then(values => {
      store.recordProgress(props.record.id, config.value.form.value)
        .then((resp) => {
          closeModal();
        });
    });
}

const generatePeriods = computed(() => {
  const recorded_periods = Object.keys(props.record.evaluation);

  if (props.record.evaluation_period == 'monthly') {
    return Array(12).fill(0).map((_, i) => {
      const period = `Month ${i + 1}`,
        disabled = recorded_periods.includes(period);
      return {
        label: period,
        value: period,
        disabled: disabled
      }
    });
  }
  if (props.record.evaluation_period == "quarterly") {
    return Array(4).fill(0).map((_, i) => {
      const period = `Quarter ${i + 1}`,
        disabled = recorded_periods.includes(period);
      return {
        label: period,
        value: period,
        disabled: disabled
      }
    });
  }

  if (props.record.evaluation_period == "weekly") {
    return Array(53).fill(0).map((_, i) => {
      const period = `Week ${i + 1}`,
        disabled = recorded_periods.includes(period);
      return {
        label: period,
        value: period,
        disabled: disabled
      }
    });
  }

  return [];
});

</script>

<template>
  <Modal v-model:visible="config.visible" title="Record Progress" ok-text="Update" cancel-text="Cancel"
    @cancel="closeModal()" :mask-closable="false" @ok="recordProgress">

    <Spin :spinning="store.loading">

      <Form layout="vertical" :model="config.form" name="progress_tracking_form" ref="progressTrackingFormRef">

        <!-- TODO: exclude already tracked periods from dropdown -->
        <FormItem name="period" label="Select Period" has-feedback
          :rules="[{ required: true, message: 'Please select a period!' }]">
          <Select v-model:value="config.form.period" placeholder="Please period" :show-search="true" :allow-clear="true"
            :options="generatePeriods">
            <!-- <SelectOption v-for="period in generatePeriods" :value="period.value" :disabled="period.disabled"
              :label="period.label" :key="period.value"></SelectOption> -->
          </Select>
        </FormItem>

        <FormItem label="Value" name="value" :rules="[{ required: true, message: 'Please input your username!' }]">
          <Input v-model:value="config.form.value" type="number" />
        </FormItem>
      </Form>

    </Spin>
  </Modal>
</template>
