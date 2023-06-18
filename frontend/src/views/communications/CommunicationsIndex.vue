<script setup lang="ts">

import { ref } from 'vue';

import { PlusOutlined } from '@ant-design/icons-vue';
import { Card, CollapsePanel, Collapse, Descriptions, DescriptionsItem, Button, Modal, Form, type FormInstance } from 'ant-design-vue';

const config = ref({
  loading: false,
  collapseKey: '',
  modal: {
    visible: false
  }
})

</script>

<template>
  <Card title="Communications and Messaging">
    <template #extra>
      <Button type="primary" @click="config.modal.visible = true">
        <template #icon>
          <PlusOutlined />
        </template>
        Add
      </Button>

    </template>
    <Collapse v-model:activeKey="config.collapseKey">
      <CollapsePanel key="1" header="This is panel header 1">

        <Descriptions :column="2" bordered>
          <DescriptionsItem :labelStyle="{ 'font-weight': 'bold' }" label="Target project objective(s)">Cloud Database
          </DescriptionsItem>

          <DescriptionsItem :labelStyle="{ 'font-weight': 'bold' }" label="Related indicator(s)">Cloud Database
          </DescriptionsItem>

          <DescriptionsItem :labelStyle="{ 'font-weight': 'bold' }" label="Target audience(s)">Cloud Database
          </DescriptionsItem>

          <DescriptionsItem :labelStyle="{ 'font-weight': 'bold' }" label="Target behavioral driver(s)">Cloud Database
          </DescriptionsItem>

          <DescriptionsItem :labelStyle="{ 'font-weight': 'bold' }" label="Message objective(s)">Cloud Database
          </DescriptionsItem>

          <DescriptionsItem :labelStyle="{ 'font-weight': 'bold' }" label="Message delivery platform(s)">Cloud Database
          </DescriptionsItem>

          <DescriptionsItem :labelStyle="{ 'font-weight': 'bold' }" label="Message format">Cloud Database
          </DescriptionsItem>

          <DescriptionsItem :labelStyle="{ 'font-weight': 'bold' }" label="Key points">Cloud Database
          </DescriptionsItem>

          <DescriptionsItem :labelStyle="{ 'font-weight': 'bold' }" label="Message content">Cloud Database
          </DescriptionsItem>

        </Descriptions>

      </CollapsePanel>
    </Collapse>
  </Card>

</template>
