<script setup lang="ts">
import { useUserStore } from '@/stores/user';
import { InboxOutlined } from '@ant-design/icons-vue';
import {
  Modal, type FormInstance, Select, SelectOption,
  Space, Button, Form, FormItem, Input, Textarea, UploadDragger, type UploadProps
 } from 'ant-design-vue';
import axios from 'axios';
import { reactive, ref, watch } from 'vue';

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
  (e: 'close'): void;
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
  const fileList = ref<UploadProps['fileList']>([]);

function closeModal() {
  feedbackFormRef.value.resetFields();
  config.value.form = new Feedback();
  config.value.visible = false;
  emit('close');
}

function saveForm(){
  console.log(fileList.value);

  const formData = new FormData();
  fileList.value.forEach((file: UploadProps['fileList'][number]) => {
    console.log(file)
    formData.append('files', file.originFileObj as any);
  });


  axios.post(`${import.meta.env.VITE_SBC_API_URL}/feedback`, formData)
        .then((resp) => {
          console.log(resp);
          config.value.loading = false;
          closeModal();
        })
        .catch(() => {
          config.value.loading = false;
        });

  feedbackFormRef.value.validateFields()
    .then((values: any) => {
      config.value.loading = true;

      const form = config.value.form;
      form.editing_user_id = userStore.id;


      // Upload form with files to backend using axios
      Object.keys(form).forEach((key) => {
        // @ts-ignore
        formData.append(key, form[key]);
      });

      axios.post(`${import.meta.env.VITE_SBC_API_URL}/feedback`, formData)
        .then((resp) => {
          console.log(resp);
          config.value.loading = false;
          closeModal();
        })
        .catch(() => {
          config.value.loading = false;
        });


    });
}

const beforeUpload: UploadProps['beforeUpload'] = file => {
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

        <Button @click="closeModal()" :loading="config.loading">Cancel</Button>
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
          <Textarea v-model:value="config.form.description"></Textarea>
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
