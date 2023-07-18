<script lang="ts" setup>
import { ref, computed, watch } from "vue";
import { Risk } from "@/types";
import {
  Button,
  Card,
  Divider,
  Form,
  FormItem,
  Input,
  Modal,
  Space,
  Spin,
  Switch,
  Textarea,
} from "ant-design-vue";
import { SwapOutlined } from "@ant-design/icons-vue";
import { useTheoryOfChangeStore } from "@/stores/theory_of_change";

const props = defineProps<{
  visible: boolean;
  edge: { toc_from_id: number; toc_to_id: number };
}>();

const emit = defineEmits<{ (e: "close"): void }>();

const store = useTheoryOfChangeStore();

const config = ref({
  visible: props.visible,
  loading: false,
  form: new Risk(),
});

function closeModal() {
  config.value.visible = false;
  config.value.form = new Risk();
  emit("close");
}

function saveForm() {
  config.value.loading = true;
  store
    .saveRisk(config.value.form)
    .then((resp) => {
      closeModal();
    })
    .finally(() => {
      config.value.loading = false;
    });
}

watch(props, (newProps) => {
  config.value.visible = newProps.visible;
  const edge = newProps.edge;

  const existingRisk = store.risks.find(
    (i) => i.toc_from_id == edge.toc_from_id && i.toc_to_id == edge.toc_to_id
  );
  config.value.form = existingRisk ?? new Risk();
  config.value.form.toc_from_id ??= edge.toc_from_id;
  config.value.form.toc_to_id ??= edge.toc_to_id;
  config.value.visible = true;
});

const getLabel = computed(() => {
  return (tocId: number) => store.theory_of_change.find((i) => i.id == tocId)?.name;
});
</script>

<template>
  <Modal v-model:open="config.visible" @ok="closeModal()" @cancel="closeModal()">
    <template #title>
      <span>
        {{ getLabel(edge.toc_from_id) }}
        <SwapOutlined />
        {{ getLabel(edge.toc_to_id) }}
      </span>
    </template>

    <template #footer>
      <Space>
        <Button :disabled="config.loading" @click="closeModal()">Cancel</Button>

        <Button :loading="config.loading" @click="saveForm()" type="primary">
          {{ config.form?.id ? "Update" : "Save" }}
        </Button>
      </Space>
    </template>

    <Spin :spinning="config.loading">
      <Form layout="vertical" :model="config.form">
        <FormItem
          label="Name"
          name="name"
          :rules="[{ require: true, message: 'Enter risk name!' }]"
          has-feedback
        >
          <Input v-model:value="config.form.name" placeholder="" />
        </FormItem>

        <FormItem label="Assumptions" name="assumptions">
          <Textarea v-model:value="config.form.assumptions" placeholder=""></Textarea>
        </FormItem>

        <FormItem label="Risks" name="risks">
          <Textarea v-model:value="config.form.risks" placeholder=""></Textarea>
        </FormItem>

        <FormItem label="Mitigation" name="mitigation">
          <Textarea v-model:value="config.form.mitigation" placeholder=""></Textarea>
        </FormItem>
      </Form>
    </Spin>
  </Modal>
</template>
