<script lang="ts" setup>

import { useMonitoringStore } from '@/stores/monitoring.store';
import { useProjectStore } from '@/stores/projects';
import { Monitoring } from '@/types';
import { Modal, Form, FormItem, Input, Select, SelectOption, Spin, type FormInstance, message } from 'ant-design-vue';
import { computed, h, ref, watch } from 'vue';
import dayjs from 'dayjs';

const props = defineProps<{ visible: boolean, record: Monitoring }>();
const emit = defineEmits<{
  (e: 'isClosed', status: boolean): boolean,
}>()

const store = useMonitoringStore(),
  projectStore = useProjectStore();

const progressTrackingFormRef = ref<FormInstance>(),
  config = ref({
    visible: props.visible,
    form: {
      value: '',
      period: '',
      progress: null,
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
  if(props.record.type == "Quantitative") {
    if (props.record?.target == null) {
      Modal.error({
        title: 'Indicator target required',
        content: h('div', {}, [
          h('p', 'Please set a target first!'),
        ])
      });
      return;
    }
  }

  progressTrackingFormRef.value
    .validateFields()
    .then(values => {

      // Calculate progress
      if(props.record.type == "Quantitative") {
        let total = +props.record.progress ?? 0;
        for(const i of (props.record.evaluation || [])) {
            total += +i.value
        }

        config.value.form.progress = ((total / +props.record.target) * 100).toFixed(2);
      }

      store.recordProgress(props.record.id, config.value.form)
        .then((resp) => {
          closeModal();
        });
    });
}
</script>

<template>
  <Modal
    v-model:visible="config.visible"
    title="Record Progress"
    ok-text="Update"
    cancel-text="Cancel"
    @cancel="closeModal()"
    :mask-closable="false"
    @ok="recordProgress"
  >
    <Spin :spinning="store.loading">
      <Form
        layout="vertical"
        :model="config.form"
        name="progress_tracking_form"
        ref="progressTrackingFormRef"
      >
        <!-- TODO: exclude already tracked periods from dropdown -->
        <FormItem
          name="period"
          label="Reporting Period"
          has-feedback
          :rules="[{ required: true, message: 'Enter reporting period!' }]"
        >
          <Input v-model:value="config.form.period" placeholder="eg. Month 1"> </Input>
        </FormItem>

        <FormItem
          label="Value"
          name="value"
          :rules="[{ required: true, message: 'Progress value is required!' }]"
        >
          <Input v-model:value="config.form.value" />
        </FormItem>
      </Form>
    </Spin>
  </Modal>
</template>
