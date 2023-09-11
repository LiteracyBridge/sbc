<script lang="ts" setup>
import { useMonitoringStore } from "@/stores/monitoring.store";
import { useProjectStore } from "@/stores/projects";
import { Monitoring } from "@/types";
import {
  Modal,
  Form,
  FormItem,
  Input,
  Select,
  SelectOption,
  Spin,
  Tooltip,
} from "ant-design-vue";
import type { FormInstance } from "ant-design-vue";
import { computed, h, ref, watch } from "vue";
import { InfoCircleOutlined } from "@ant-design/icons-vue";

const props = defineProps<{ visible: boolean; record: Monitoring }>();
const emit = defineEmits<{
  (e: "isClosed", status: boolean): boolean;
}>();

const store = useMonitoringStore();

const progressTrackingFormRef = ref<FormInstance>(),
  config = ref({
    visible: props.visible,
    form: {
      value: "",
      period: "",
      progress: null,
    },
  });

watch(
  props,
  (newProps) => {
    config.value.visible = newProps.visible;
  },
  { deep: true }
);

function closeModal() {
  progressTrackingFormRef.value.resetFields();
  config.value.visible = false;

  emit("isClosed", true);
}

function recordProgress() {
  if (props.record.type == "Quantitative") {
    if (props.record?.target == null) {
      Modal.error({
        title: "Indicator target required",
        content: h("div", {}, [h("p", "Please set a target first!")]),
      });
      return;
    }
  }

  progressTrackingFormRef.value.validateFields().then((values) => {
    // Calculate progress
    if (
      props.record.type == "Quantitative"
    ) {
      let total = +config.value.form.value;
      for (const i of props.record.evaluation || []) {
        total += +i.value;
      }

      if (props.record.target == null) {
        Modal.error({
          title: "Indicator target not set",
          content: h("div", {}, [h("p", "Please set a target first!")]),
        });
        return;
      }

      config.value.form.progress = ((total / (+props.record.target ?? 1)) * 100).toFixed(
        2
      );
      console.log(config.value.form.value)
    }

    store.recordProgress(props.record.id, config.value.form).then((resp) => {
      closeModal();
    });
  });
}
</script>

<template>
  <Modal
    v-model:open="config.visible"
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
          <Input v-model:value="config.form.value">
            <template #suffix>
              <Tooltip
                title="Progress value must be for the period that is being recorded. Cumulative reporting is not supported."
              >
                <InfoCircleOutlined />
              </Tooltip>
            </template>
          </Input>
        </FormItem>
      </Form>
    </Spin>
  </Modal>
</template>
