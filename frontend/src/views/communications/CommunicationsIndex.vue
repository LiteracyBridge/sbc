<script setup lang="ts">

import { onMounted, ref, computed } from 'vue';

import { PlusOutlined } from '@ant-design/icons-vue';
import {
  Card, CollapsePanel, Collapse,
  Descriptions, DescriptionsItem,
  Button, Space, Form, type FormInstance,
  FormItem, Input, Textarea,
  Select, SelectOption,
  Drawer, Spin, Popconfirm, Empty
} from 'ant-design-vue';
import { useProjectDataStore } from '@/stores/projectData';
import { useTheoryOfChangeStore } from '@/stores/theory_of_change';
import { useCommunicationStore } from '@/stores/communication.store';
import { Communication } from '@/types';
import { useDriverStore } from '@/stores/drivers';
import GPTSuggestionPanel from '@/components/GPTSuggestionPanel.vue';

const BULB_ICON = "/images/lightbulb.png"


const projectDataStore = useProjectDataStore(),
  store = useCommunicationStore();

const config = ref({
  loading: false,
  collapseKey: '',
  selectedItem: {} as Communication,
  modal: {
    visible: false,
    form: {
      id: null,
      project_objectives: [] as number[],
      drivers: [] as number[],
      indicators: [] as number[],
      target_audiences: [] as number[],
      message_objectives: '',
      delivery_platforms: '',
      format: '',
      key_points: '',
      contents: '',
      title: '',
    }
  },
  suggestions: {
    type: null,
    visible: false,
    ai: {
      prompt: '',
      context: '',
      format: '',
      defaultValue: '',
    }
  }
});
const communicationFormRef = ref<FormInstance>();

function closeModal() {
  config.value.modal.visible = false;
  config.value.modal.form = {
    id: null,
    project_objectives: [] as number[],
    drivers: [] as number[],
    indicators: [] as number[],
    target_audiences: [] as number[],
    message_objectives: '',
    delivery_platforms: '',
    format: '',
    key_points: '',
    contents: '',
    title: '',
  };
  communicationFormRef.value.resetFields();
}

function saveForm() {
  communicationFormRef.value.validateFields().then((values) => {
    store.create(config.value.modal.form).then((response) => {
      closeModal();
    });
  }).catch((error) => {
    console.log(error);
  })
}

function onEditClick(item: Communication) {
  communicationFormRef.value?.resetFields();

  config.value.modal.form = {
    ...item,
    project_objectives: item.project_objectives.map((obj) => obj.objective_id),
    indicators: item.indicators.map((obj) => obj.indicator_id),
    target_audiences: item.target_audiences.map((obj) => obj.audience_id),
    drivers: item.drivers.map((obj) => obj.driver_id),
  };
  config.value.modal.visible = true;
}

onMounted(() => {
  store.download();
})

const generateAIPrompt = computed(() => {
  const { form } = config.value.modal;

  let context = "Message Title: " + config.value.modal.form.title + "\n";

  if (form.project_objectives?.length > 0) {
    context += "The project has the following objectives: " + projectDataStore.specificObjectives
      .filter(p => form.project_objectives?.includes(p.id)
      )
      ?.map((p, i) => `(${i + 1}). ${p.data}`).join(', ') + '.';
  }
  if (form.indicators?.length > 0) {
    context += "\nThe project has the following indicators: " + useTheoryOfChangeStore().allTocIndicators
      .filter(p => form.indicators?.includes(p.id)
      )
      ?.map((p, i) => `(${i + 1}). ${p.name}`).join(', ') + '.';
  }
  // TODO: add drivers
  if (form.target_audiences?.length > 0) {
    context += "\nThe messages to be delivered has the following target audiences: " + projectDataStore.audiences
      .filter(p => form.target_audiences?.includes(p.id)
      )
      ?.map((p, i) => `(${i + 1}). ${p.data}`).join(', ') + '.';
  }

  if(form.delivery_platforms){
    context += "\nThe message will be delivered through these platforms: " + form.delivery_platforms + ".";
  }

  return context
})

function messageKeyPointsSuggestion() {
  config.value.suggestions = {
    ai: {
      prompt: "List key points suitable for the message to be delivered.",
      context: generateAIPrompt.value,
      format: "list",
      defaultValue: config.value.modal.form.key_points
      },
      visible: true,
      type: "key_points"
  };
}

function messageContentSuggestion() {
  const form = config.value.modal.form
  config.value.suggestions = {
    ai: {
      prompt: `Suggest suitable message content for the project. YOUR RESPONSE SHOULD BE IN '${form.format}' FORM!`,
      context: generateAIPrompt.value,
      format: "essay",
      defaultValue: form.contents
    },
    visible: true,
    type: "content"
  };
}

const onSuggestionClosed = (val: string) => {
  if(config.value.suggestions.type == "content"){
    config.value.modal.form.contents = val;
  } else {
    config.value.modal.form.key_points = val;
  }
  config.value.suggestions.visible = false;
}
</script>

<template>
  <GPTSuggestionPanel
    :is-visible="config.suggestions.visible"
    @is-closed="config.suggestions.visible = false"
    @saved="onSuggestionClosed"
    :ai="config.suggestions.ai"
  >
  </GPTSuggestionPanel>

  <Card title="Communications and Messaging" :bordered="false">
    <template #extra>
      <Button type="primary" @click="config.modal.visible = true">
        <template #icon>
          <PlusOutlined />
        </template>
        New Communication Message
      </Button>
    </template>

    <Spin :spinning="store.loading">
      <Empty v-if="store.data.length === 0"></Empty>

      <Collapse v-model:activeKey="config.collapseKey">
        <CollapsePanel v-for="item in store.data" :key="item.id" :header="item.title">
          <template #extra>
            <Space>
              <Button
                type="primary"
                :ghost="true"
                size="small"
                role="button"
                @click.prevent="onEditClick(item)"
              >
                Edit
              </Button>

              <Popconfirm
                title="Are you sure delete this message?"
                ok-text="Yes"
                cancel-text="No"
                @confirm="store.delete(item.id)"
              >
                <Button type="primary" :ghost="true" danger size="small"> Delete </Button>
              </Popconfirm>
            </Space>
          </template>

          <Descriptions size="small" :column="2" bordered layout="vertical">
            <DescriptionsItem
              :label-style="{ 'font-weight': 'bold' }"
              label="Target Project Objectives"
              >{{
                store
                  .projectObjectives(item.id)
                  ?.map((obj) => obj.data)
                  .join(", ") || "N/A"
              }}
            </DescriptionsItem>

            <DescriptionsItem
              label="Target Audiences"
              :label-style="{ 'font-weight': 'bold' }"
              >{{
                store
                  .targetAudiences(item.id)
                  ?.map((obj) => obj.data)
                  .join(", ") || "N/A"
              }}
            </DescriptionsItem>

            <!-- TODO: Implement related indicators -->
            <DescriptionsItem
              label="Related Indicators"
              :label-style="{ 'font-weight': 'bold' }"
              >{{
                store
                  .indicators(item.id)
                  ?.map((obj) => obj.name)
                  .join(", ") || "N/A"
              }}
            </DescriptionsItem>

            <DescriptionsItem
              label="Target Behavioral Drivers"
              :label-style="{ 'font-weight': 'bold' }"
            >
              {{
                store
                  .behavioralDrivers(item.id)
                  ?.map((obj) => obj.name)
                  .join(", ") || "N/A"
              }}
            </DescriptionsItem>

            <DescriptionsItem
              label="Message Objectives"
              :label-style="{ 'font-weight': 'bold' }"
            >
              <span class="preserve-whitespace">
                {{ item.message_objectives || "N/A" }}
              </span>
            </DescriptionsItem>

            <DescriptionsItem
              label="Message Delivery Channels"
              :label-style="{ 'font-weight': 'bold' }"
            >
              <span class="preserve-whitespace">
                {{ item.delivery_platforms || "N/A" }}
              </span>
            </DescriptionsItem>

            <DescriptionsItem
              label="Message Format"
              :label-style="{ 'font-weight': 'bold' }"
            >
              <span class="preserve-whitespace">
                {{ item.format || "N/A" }}
              </span>
            </DescriptionsItem>

            <DescriptionsItem label="Key Points" :label-style="{ 'font-weight': 'bold' }">
              <span class="preserve-whitespace">
                {{ item.key_points || "N/A" }}
              </span>
            </DescriptionsItem>

            <DescriptionsItem
              label="Message Content"
              :label-style="{ 'font-weight': 'bold' }"
              :span="2"
            >
              <span class="preserve-whitespace">
                {{ item.contents || "N/A" }}
              </span>
            </DescriptionsItem>
          </Descriptions>
        </CollapsePanel>
      </Collapse>
    </Spin>
  </Card>

  <Drawer
    v-model:open="config.modal.visible"
    width="60vw"
    :mask-closable="false"
    @close="closeModal"
  >
    <template #title>
      {{ config.modal.form?.id != null ? "Update" : "New" }} Communication
    </template>

    <template #extra>
      <Space>
        <Button type="primary" @click="saveForm">
          {{ config.modal.form?.id != null ? "Update" : "Save" }}
        </Button>

        <Button @click="closeModal">Cancel</Button>
      </Space>
    </template>

    <Spin :spinning="store.loading">
      <Form
        name="communications-form"
        ref="communicationFormRef"
        :model="config.modal.form"
        layout="vertical"
      >
        <FormItem
          name="title"
          label="Message Title"
          has-feedback
          :rules="[{ required: true, message: 'Please enter message title' }]"
        >
          <Input v-model:value="config.modal.form.title"> </Input>
        </FormItem>

        <FormItem
          name="project_objectives"
          label="Project objectives"
          has-feedback
          :rules="[{ required: true, message: 'Please select project objectives!' }]"
        >
          <Select
            v-model:value="config.modal.form.project_objectives"
            placeholder="Select project objectives"
            mode="multiple"
            :show-search="true"
          >
            <SelectOption
              v-for="obj in projectDataStore.specificObjectives"
              :value="obj.id"
              :key="obj.id"
              >{{ obj.data }}</SelectOption
            >
          </Select>
        </FormItem>

        <FormItem
          name="target_audiences"
          label="Target Audiences"
          has-feedback
          :rules="[{ required: true, message: 'Please select target audiences!' }]"
        >
          <Select
            v-model:value="config.modal.form.target_audiences"
            placeholder="Select target audiences"
            mode="multiple"
            :show-search="true"
          >
            <SelectOption
              v-for="obj in useProjectDataStore().audiences"
              :value="obj.id"
              :key="obj.id"
              >{{ obj.data }}
            </SelectOption>
          </Select>
        </FormItem>

        <FormItem
          name="drivers"
          label="Target Behavioral Drivers"
          has-feedback
          :rules="[{ required: false, message: 'Please select target drivers!' }]"
        >
          <Select
            v-model:value="config.modal.form.drivers"
            placeholder="Select target drivers"
            mode="multiple"
            :show-search="true"
          >
            <SelectOption
              v-for="obj in useDriverStore().driversInProject"
              :value="obj.id"
              :key="obj.id"
              >{{ obj.name }}
            </SelectOption>
          </Select>
        </FormItem>

        <FormItem
          name="indicators"
          label="Related Indicators"
          has-feedback
          :rules="[{ required: true, message: 'Please select related indicators!' }]"
        >
          <Select
            v-model:value="config.modal.form.indicators"
            placeholder="Select related indicators"
            mode="multiple"
            :show-search="true"
          >
            <SelectOption
              v-for="obj in useTheoryOfChangeStore().allTocIndicators"
              :value="obj.id"
              :key="obj.id"
              >{{ obj.name }}
            </SelectOption>
          </Select>
        </FormItem>

        <FormItem
          name="message_objectives"
          label="Message Objectives"
          has-feedback
          :rules="[{ required: true, message: 'Please enter message objectives' }]"
        >
          <Textarea v-model:value="config.modal.form.message_objectives" :rows="7">
          </Textarea>
        </FormItem>

        <FormItem
          name="delivery_platforms"
          label="Message Delivery Channels"
          has-feedback
          :rules="[
            { required: false, message: 'Please enter message delivery platforms' },
          ]"
        >
          <Textarea v-model:value="config.modal.form.delivery_platforms" :rows="7">
          </Textarea>
        </FormItem>

        <FormItem
          name="format"
          label="Message Format"
          has-feedback
          :rules="[{ required: false, message: 'Please enter message format!' }]"
        >
          <Textarea v-model:value="config.modal.form.format" :rows="7"></Textarea>
        </FormItem>

        <FormItem
          name="key_points"
          label="Message Key Points"
          has-feedback
          :rules="[{ required: true, message: 'Please enter message key points!' }]"
        >
          <img
            :src="BULB_ICON"
            @click="messageKeyPointsSuggestion()"
            class="image is-32x32"
          />
          <Textarea
            v-model:value="config.modal.form.key_points"
            name="key_points"
            :rows="10"
          ></Textarea>
        </FormItem>

        <FormItem
          name="contents"
          label="Message Contents"
          has-feedback
          :rules="[{ required: false, message: 'Please enter message content!' }]"
        >
          <img
            :src="BULB_ICON"
            @click="messageContentSuggestion()"
            class="image is-32x32"
          />

          <Textarea
            v-model:value="config.modal.form.contents"
            name="contents"
            :rows="10"
          ></Textarea>
        </FormItem>
      </Form>
    </Spin>
  </Drawer>
</template>
