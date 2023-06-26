<script lang="ts" setup>

import { useProjectStore } from '@/stores/projects';
import { Button, Space, Form, FormItem, Textarea, Spin, type FormInstance } from 'ant-design-vue';
import { ref } from 'vue';


const store = useProjectStore();
const strategyFormRef = ref<FormInstance>();

</script>

<template>
  <Spin :spinning="store.loading">
    <Form ref="strategyFormRef" layout="vertical" :model="store.current_project" name="evaluationFormRef">

      <FormItem
        label="What is the sustainability strategy for this project? How will impact continue to be created after the project ends?"
        name="sustainability_strategy" :rules="[{ required: true, message: 'Please input your evaluation strategy!' }]">
        <Textarea v-model:value="store.current_project.sustainability_strategy"
          :rows="8">{{ store.current_project.sustainability_strategy }}</Textarea>
      </FormItem>

      <FormItem>
        <!-- TODO: center button -->
        <Space align="center" style="justify-content: center;">
          <Button type="primary" @click="strategyFormRef.validateFields().then(() => store.updateStrategy())"
            :loading="store.loading">Submit</Button>
        </Space>
      </FormItem>
    </Form>

  </Spin>
</template>
