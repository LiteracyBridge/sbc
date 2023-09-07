<script setup lang="ts">
import { toBase64 } from "@/helpers";
import { useUserStore } from "@/stores/user";
import { InboxOutlined } from "@ant-design/icons-vue";
import {
  Modal,
  Select,
  SelectOption,
  Space,
  Button,
  Form,
  FormItem,
  Input,
  Textarea,
  UploadDragger,
  message,
  Spin,
} from "ant-design-vue";
import type { FormInstance, UploadProps } from "ant-design-vue";
import axios from "axios";
import { ref, watch } from "vue";

class Feedback {
  type: string;
  title: string;
  description: string;
  editing_user_id: number;
}

const props = defineProps<{
  visible: boolean;
}>();

const emit = defineEmits<{
  (e: "close"): void;
}>();

const userStore = useUserStore();

const config = ref({
  loading: false,
  visible: props.visible,
  form: new Feedback(),
});

watch(props, (newProps) => {
  config.value.visible = newProps.visible;
});

const feedbackFormRef = ref<FormInstance>();
const fileList = ref<UploadProps["fileList"]>([]);

function closeModal() {
  feedbackFormRef.value.resetFields();
  config.value.form = new Feedback();
  config.value.visible = false;
  fileList.value = [];

  emit("close");
}

function saveForm() {
  feedbackFormRef.value.validateFields().then(async (_: any) => {

    const form = config.value.form;
    form.editing_user_id = userStore.id;

    // const formData = new FormData();
    const formData: any = { files: [] };

    let index = 0,
      cancel = false;
    for (const file of fileList.value) {
      // Max file size 1MB
      if (file.size > 1000000) {
        cancel = true;
        alert(`File ${index + 1} is too big! Maximum file size is 1MB.`);
        return;
      }
      const data = await toBase64(file.originFileObj as any);
      formData.files.push((data as string).split(",")[1]);

      index++;
    }

    if (cancel) return;

    Object.keys(form).forEach((key) => {
      formData[key] = form[key];
    });

    config.value.loading = true;
    axios
      .post(`${import.meta.env.VITE_SBC_API_URL}/feedback`, formData, {
        headers: {
          Accept: "application/json",
          Authorization: `Bearer ${userStore.token}`,
        },
      })
      .then((_) => {
        message.success("Your feedback has been submitted successfully!");
        closeModal();
      })
      .catch((err) => {
        message.error(
          "There was an error submitting your feedback. Please try again:" + err.message
        );
      })
      .finally(() => {
        config.value.loading = false;
      });
  });
}

const beforeUpload: UploadProps["beforeUpload"] = (file) => {
  fileList.value = [...(fileList.value || []), file];
  return false;
};
</script>

<template>
  <Modal
    v-model:open="config.visible"
    @cancel="closeModal()"
    :mask-closable="false"
    title="Send us Feedback"
  >
    <template #footer>
      <Space>
        <Button
          type="primary"
          @click="saveForm()"
          :disabled="config.loading"
          :loading="config.loading"
        >
          Submit Feedback
        </Button>

        <Button @click="closeModal()" :disabled="config.loading">Cancel</Button>
      </Space>
    </template>

    <Spin :spinning="config.loading">
      <Form
        name="feedback-form"
        ref="feedbackFormRef"
        :model="config.form"
        layout="vertical"
      >
        <FormItem
          label="Title"
          name="title"
          :rules="[
            { required: true, message: 'Please enter the title/summary of the feedback' },
          ]"
        >
          <Input v-model:value="config.form.title" />
        </FormItem>

        <FormItem
          label="Type of Feedback"
          name="type"
          :rules="[{ required: true, message: 'Please select the type of  feedback' }]"
        >
          <Select v-model:value="config.form.type" :allow-clear="true">
            <SelectOption value="feature">Feature Request</SelectOption>
            <SelectOption value="suggestions"
              >Recommendations or Suggestions</SelectOption
            >
            <SelectOption value="error">Error Report</SelectOption>
            <SelectOption value="other">Other</SelectOption>
          </Select>
        </FormItem>

        <FormItem
          label="Description"
          name="description"
          :rules="[
            {
              required: true,
              message:
                'Please give as much as possible, detailed description of the issue',
            },
          ]"
        >
          <Textarea v-model:value="config.form.description" :rows="5"></Textarea>
        </FormItem>

        <FormItem label="Upload screenshots">
          <FormItem name="dragger" no-style>
            <UploadDragger
              :before-upload="beforeUpload"
              v-model:fileList="fileList"
              name="files"
            >
              <p class="ant-upload-drag-icon">
                <InboxOutlined />
              </p>
              <p class="ant-upload-text">Click or drag file to this area to upload</p>
              <p class="ant-upload-hint">Support for a single or bulk upload.</p>
            </UploadDragger>
          </FormItem>
        </FormItem>
      </Form>
    </Spin>
  </Modal>
</template>
