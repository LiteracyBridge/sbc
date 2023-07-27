<script setup lang="ts">
import { SBC_TW_URL } from "@/apis/lambda";
import { useProjectDataStore } from "@/stores/projectData";
import { useProjectStore } from "@/stores/projects";
import { useUserStore } from "@/stores/user";
import { Stakeholder, ProjectUser } from "@/types";
import { Button, Modal, message, Spin, Steps, Step, Table, type TableProps, Drawer, Space, Popconfirm } from "ant-design-vue";
import axios from "axios";
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


function closeModal() {
  config.value = {
    visible: false,
    currentStep: 0,
    stakeholders: [] as Stakeholder[],
    users: [] as ProjectUser[]
  };
  emit("close");
}

function broadcast() {
  if(config.value.stakeholders.length == 0 && config.value.users.length == 0) {
    message.error("Please select at least one user or stakeholder to broadcast to.");
    return;
  }

  store.loading = true;

  message.info("Broadcasting message to all users in the project");
  axios.post(`${SBC_TW_URL}/broadcast`, {
    project_id: projectStore.prj_id,
    message:  store.buildBroadcastMessage(props.module),
    related_item: props.module,
    stakeholder_ids: config.value.stakeholders.map((s) => s.id),
    user_ids: config.value.users.map((s) => s.user_id),
    user_id_sending: useUserStore().id,
  }).then((resp) => {
    console.log(resp)
    closeModal()
  }).finally(() => store.loading = false)

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
  onChange: (_selectedRowKeys: string[], selectedRows: Stakeholder[]) => {
    config.value.stakeholders = selectedRows;
  },
  getCheckboxProps: (record: Stakeholder) => ({
    disabled: false,
    name: record.name,
  }),
};


const getUsers = computed(() => {
  return projectStore.users_in_project.map((s) => ({...s, key: s.user_id}));
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
  <Drawer
    title="Are you sure to broadcast this message?"
    v-model:open="config.visible"
    @cancel="closeModal()"
    width="60vw"
  >
    <template #footer>
      <!-- <Button type="primary" :danger="true" @click="broadcast()" :loading="store.loading"
        >Broadcast</Button
      >
      <Button :disabled="store.loading" @click="cancel()">Cancel</Button> -->

      <div class="steps-action" style="justify-content: space-between; display: flex">
        <Button :disabled="store.loading" @click="closeModal()">Cancel</Button>

        <Space>
          <Button v-if="config.currentStep > 0" @click="config.currentStep--">
            Previous
          </Button>

          <Popconfirm
            v-if="config.currentStep == steps.length - 1"
            ok-text="Broadcast"
            @confirm="broadcast()"
            title="This will broadcast the message to all selected users."
          >
            <Button
              v-if="config.currentStep == steps.length - 1"
              type="primary"
              :danger="true"
            >
              Broadcast Now
            </Button>
          </Popconfirm>

          <Button
            v-if="config.currentStep < steps.length - 1"
            type="primary"
            @click="config.currentStep++"
          >
            Next
          </Button>
        </Space>
      </div>
    </template>

    <Spin :spinning="store.loading">
      <Steps :current="config.currentStep" :items="steps" size="small"> </Steps>

      <div class="steps-content" style="padding-top: 20px">
        <!-- Preview step -->
        <div v-show="config.currentStep == 0">
          <p class="preserve-whitespace">
            {{ store.buildBroadcastMessage(props.module) }}
          </p>
        </div>

        <!-- Project users selection -->
        <div v-show="config.currentStep == 1">
          <Table
            size="small"
            :row-selection="usersRowSelection"
            :columns="columns"
            :data-source="getUsers"
          >
          </Table>
        </div>

        <!-- Stakeholders selection -->
        <div v-show="config.currentStep == 2">
          <Table
            size="small"
            :row-selection="stakeholdersRowSelection"
            :columns="columns"
            :data-source="getStakeHolders"
          >
          </Table>
        </div>
      </div>
    </Spin>
  </Drawer>
</template>
