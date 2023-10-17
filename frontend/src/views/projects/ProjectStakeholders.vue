<script lang="ts" setup>
import { computed, ref } from "vue";
import { useProjectStore } from "@/stores/projects";
import {
  Table,
  Spin,
  Space,
  Col,
  Row,
  Modal,
  Button,
  Tag,
  Typography,
  Form,
  FormItem,
  Input,
  Popconfirm,
  Textarea,
} from "ant-design-vue";
import type { FormInstance } from "ant-design-vue";
import { PlusCircleOutlined } from "@ant-design/icons-vue";
import { Stakeholder } from "@/types";

const store = useProjectStore();
const modal = ref<{ visible: boolean; form: Stakeholder | Record<string, any> }>({
  visible: false,
  form: new Stakeholder(),
});
const stakeholderFormRef = ref<FormInstance>();

const columns = [
  {
    title: "Name",
    key: "name",
  },
  {
    title: "WhatsApp",
    key: "whatsapp",
  },
  {
    title: "SMS",
    key: "sms",
  },
  {
    title: "Email",
    key: "email",
  },
  {
    title: "Description",
    key: "description",
  },
  {
    title: "",
    key: "actions",
  },
];

function closeModal() {
  stakeholderFormRef.value.resetFields();
  modal.value.form = new Stakeholder();
  modal.value.visible = false;
}

function saveForm() {
  stakeholderFormRef.value.validateFields().then((_values) => {
    store.createOrUpdateStakeholder(modal.value.form as Stakeholder).then(() => {
      closeModal();
    });
  });
}

const isEditing = computed(() => modal.value.form?.id != null);
</script>

<template>
  <Table
    :columns="columns"
    :data-source="store.stakeholders"
    bordered
    :loading="store.loading"
  >
    <template #title>
      <Row justify="space-between">
        <Col :span="20">
          <Typography :level="2">Project Stakeholders</Typography>
        </Col>

        <Col :span="4">
          <!-- TODO: implement creating new project in a modal -->
          <Button type="primary" @click="modal.visible = true">
            <template #icon>
              <PlusCircleOutlined />
            </template>
            Add Stakeholder
          </Button>
        </Col>
      </Row>
    </template>

    <template #bodyCell="{ column, record }">
      <template v-if="column.key == 'name'">
        {{ record.name }}
      </template>

      <template v-if="column.key == 'whatsapp'">
        {{ record.whatsapp || "N/A" }}
      </template>

      <template v-if="column.key == 'sms'">
        {{ record.sms || "N/A" }}
      </template>

      <template v-if="column.key == 'email'">
        {{ record.email || "N/A" }}
      </template>

      <template v-if="column.key == 'description'">
        {{ record.description || "N/A" }}
      </template>

      <template v-if="column.key === 'actions'">
        <Space>
          <Button
            type="primary"
            size="small"
            :ghost="true"
            @click.prevent="
              modal.form = record;
              modal.visible = true;
            "
          >
            Edit
          </Button>

          <!-- TODO: show confirmation box for archiving -->
          <Popconfirm
            title="Are you sure to delete this stakeholder?"
            ok-text="Yes"
            cancel-text="No"
            @confirm="store.deleteStakeholder(record.id)"
          >
            <Button type="primary" size="small" :ghost="true" :danger="true">
              Delete
            </Button>
          </Popconfirm>

          <!-- TODO: Add unarchive button -->
        </Space>
      </template>
    </template>
  </Table>

  <Modal v-model:open="modal.visible" @cancel="closeModal()" :mask-closable="false">
    <template #title>
      <span>{{ isEditing ? "Update" : "Add" }} New Stakeholder</span>
    </template>

    <template #footer>
      <Space>
        <Button
          type="primary"
          @click="saveForm()"
          :disabled="store.loading"
          :loading="store.loading"
        >
          {{ isEditing ? "Update" : "Add" }} Stakeholder
        </Button>

        <Button @click="closeModal()" :loading="store.loading">Cancel</Button>
      </Space>
    </template>

    <Spin :spinning="store.loading">
      <Form
        name="new-stakeholder-form"
        ref="stakeholderFormRef"
        :model="modal.form"
        layout="vertical"
      >
        <FormItem
          label="Stakeholder Name"
          name="name"
          :rules="[{ required: true, message: 'Please enter stakeholder name!' }]"
        >
          <Input v-model:value="modal.form.name" />
        </FormItem>

        <Row :gutter="8">
          <Col :span="12">
            <FormItem label="WhatsApp Number" name="whatsapp">
              <Input v-model:value="modal.form.whatsapp" type="tel" />
            </FormItem>
          </Col>

          <Col :span="12">
            <FormItem label="SMS Number" name="sms">
              <Input v-model:value="modal.form.sms" type="tel" />
            </FormItem>
          </Col>
        </Row>

        <Row :gutter="8">
          <Col :span="12">
            <FormItem label="Email" name="email">
              <Input v-model:value="modal.form.email" type="email" />
            </FormItem>
          </Col>
        </Row>

        <FormItem label="Additional Notes" name="description">
          <Textarea v-model:value="modal.form.description"></Textarea>
        </FormItem>
      </Form>
    </Spin>
  </Modal>
</template>
