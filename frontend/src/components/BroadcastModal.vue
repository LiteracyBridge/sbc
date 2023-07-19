<script setup lang="ts">
import { useProjectDataStore } from "@/stores/projectData";
import { useProjectStore } from "@/stores/projects";
import { Stakeholder, ProjectUser } from "@/types";
import { Button, Modal, message, Spin, Steps, Step, Table, type TableProps } from "ant-design-vue";
import { computed, ref, watch } from "vue";

const props = defineProps<{
  module: string;
  visible: boolean;
}>();
const emit = defineEmits<{
  (e: "close"): void;
}>();

const store = useProjectDataStore();
const projectStore = useProjectStore();

const config = ref({
  visible: false,
  currentStep: 0,
  stakeholders: [] as Stakeholder[],
  users: [] as ProjectUser[],
});
const steps = [
  {
    title: "Message Preview",
    description: " What you see is what your users will receive.",
  },
  {
    title: "Project Users",
    description: "Internal users you want to broadcast to.",
  },
  {
    title: "Stakeholders",
    description: "External users you want to broadcast to.",
  },
];

function broadcast() {
  store.broadcastPage(props.module);
  emit("close");
}

function cancel() {
  config.value.visible = false;
  emit("close");
}

watch(props, (newProps) => {
  config.value.visible = newProps.visible;
});

// Project stakeholders selection
const columns = [
  {
    title: "Name",
    dataIndex: "name",
    key: "name",
  },
  {
    title: "WhatsApp",
    dataIndex: "whatsapp",
    key: "whatsapp",
  },
  {
    title: "SMS",
    dataIndex: "sms",
    key: "sms",
  },
];

const getStakeHolders = computed(() => {
  return projectStore.stakeholders.map((s) => ({...s, key: s.id}));
});

const stakeholdersRowSelection: TableProps['rowSelection'] = {
  onChange: (selectedRowKeys: string[], selectedRows: Stakeholder[]) => {
    config.value.stakeholders = selectedRows;
  },
  getCheckboxProps: (record: Stakeholder) => ({
    disabled: false,
    name: record.name,
  }),
};


const getUsers = computed(() => {
  return projectStore.users_in_project.map((s) => ({...s, key: s.id}));
});

const usersRowSelection: TableProps['rowSelection'] = {
  onChange: (_selectedRowKeys: string[], selectedRows: ProjectUser[]) => {
    config.value.users = selectedRows;
  },
  getCheckboxProps: (record: ProjectUser) => ({
    disabled: false,
    name: record.name,
  }),
};
</script>

<template>
  <Modal
    title="Are you sure to broadcast this message?"
    v-model:open="config.visible"
    @cancel="cancel()"
    width="80vw"
  >
    <template #footer>
      <Button type="primary" :danger="true" @click="broadcast()" :loading="store.loading"
        >Broadcast</Button
      >
      <Button :disabled="store.loading" @click="cancel()">Cancel</Button>
    </template>

    <Steps :current="config.currentStep" :items="steps">
      <!-- <Step
        title="Message Preview"
        description="What you see is what your users will receive."
      >
        <h1>sdflskdf</h1>
      </Step> -->
    </Steps>

    <div class="steps-content">
      <!-- Preview step -->
      <div v-if="config.currentStep == 0">
        <p class="preserve-whitespace">{{ store.buildBroadcastMessage(props.module) }}</p>
      </div>

      <!-- Project users selection -->
      <div v-else-if="config.currentStep == 1">
        <Table
          size="small"
          :row-selection="usersRowSelection"
          :columns="columns"
          :data-source="getUsers"
        >
        </Table>
      </div>

      <!-- Stakeholders selection -->
      <div v-else>
        <Table
          size="small"
          :row-selection="stakeholdersRowSelection"
          :columns="columns"
          :data-source="getStakeHolders"
        >
        </Table>
      </div>
    </div>

    <div class="steps-action">
      <Button
        v-if="config.currentStep < steps.length - 1"
        type="primary"
        @click="config.currentStep++"
      >
        Next
      </Button>

      <Button
        v-if="config.currentStep == steps.length - 1"
        type="primary"
        @click="message.success('Processing complete!')"
      >
        Broadcast Now
      </Button>

      <Button
        v-if="config.currentStep > 0"
        style="margin-left: 8px"
        @click="config.currentStep--"
        >Previous
      </Button>
    </div>

    <Spin :spinning="store.loading"> </Spin>
  </Modal>
</template>
