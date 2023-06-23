<script lang="ts" setup>
// TODO: add button for viewing progress in a modal
// TODO: add button for capturing progress in a modal

import { useProjectStore } from '@/stores/projects';
import { Button, Space, Form, FormItem, Textarea, Spin, type FormInstance } from 'ant-design-vue';
import { ref } from 'vue';


const store = useProjectStore();
const evaluationFormRef = ref<FormInstance>();

</script>

<template>
  <Spin :spinning="store.loading">
    <Form ref="evaluationFormRef" layout="vertical" :model="store.current_project" name="evaluationFormRef">
      <!-- TODO: Implement saving of form -->

      <FormItem label="How will you evaluate the impact of our project? (evaluation strategy narrative)"
        name="evaluation_strategy" :rules="[{ required: true, message: 'Please input your evaluation strategy!' }]">
        <Textarea v-model:value="store.current_project.evaluation_strategy"
          :rows="8">{{ store.current_project.evaluation_strategy }}</Textarea>
      </FormItem>

      <FormItem label="How will you gather and respond to feedback from participants and stakeholders?"
        name="feedback_strategy" :rules="[{ required: true, message: 'Please input your feedback strategy!' }]">
        <Textarea v-model:value="store.current_project.feedback_strategy" :rows="8"></Textarea>
      </FormItem>

      <FormItem>
        <!-- TODO: center button -->
        <Space align="center" style="justify-content: center;">
          <Button type="primary" @click="evaluationFormRef.validateFields().then(() => store.updateStrategy())"
            :loading="store.loading">Submit</Button>
        </Space>
      </FormItem>
    </Form>

  </Spin>
</template>
