<script setup lang="ts">
import {
  Card,
  Form,
  FormItem,
  Image,
  Textarea,
  Input,
  Button,
  Row,
  Col,
  Tooltip,
  Modal,
  Spin,
} from "ant-design-vue";
import { computed, onMounted, reactive, ref, watch } from "vue";
import type { FormInstance } from "ant-design-vue";
import { ProjectDataForm, useProjectDataStore } from "@/stores/projectData";
import GPTSuggestionPanel from "@/components/GPTSuggestionPanel.vue";
import BroadcastComponent from "@/components/BroadcastComponent.vue";
import { DeleteOutlined, PlusOutlined, InfoCircleOutlined } from "@ant-design/icons-vue";
import { ProjectData, ProjectDataModule, ProjectDataName } from "@/types";
import { onBeforeRouteLeave } from "vue-router";

const BULB_ICON = "/images/lightbulb.png";

const store = useProjectDataStore();

const form = ref<ProjectDataForm[]>([]);
const config = ref({
  pendingSave: false,
  // loading: false,
  // projectData: [] as ProjectData[],
  suggestions: {
    questionId: null,
    isOpened: false,
    module: ProjectDataModule.audiences,
  },
});

// Dynamic objectives forms
const audienceFormRef = ref<FormInstance>();
const primaryFormRef = ref<FormInstance>();
const secondaryAudienceForm = reactive<{
  audiences: ProjectDataForm[];
}>({
  audiences: [],
});

const primaryAudienceForm = reactive<{
  audiences: ProjectDataForm[];
}>({
  audiences: [],
});

function showPanel(id: string | number) {
  config.value.suggestions.questionId = id;
  config.value.suggestions.module = config.value.suggestions.module;
  config.value.suggestions.isOpened = true;
}

function deleteAudience(id: number | string, primary: boolean) {
  if (primary) {
    primaryAudienceForm.audiences = primaryAudienceForm.audiences.map((i) => {
      if (i.id == id) i.deleted = true;
      return i;
    });
  } else {
    secondaryAudienceForm.audiences = secondaryAudienceForm.audiences.map((i) => {
      if (i.id == id) i.deleted = true;
      return i;
    });
  }
}

function addAudience(primary: boolean) {
  if (primary) {
    primaryAudienceForm.audiences.push({
      data: "",
      id: Date.now(),
      deleted: false,
    } as ProjectDataForm);
    return;
  }

  secondaryAudienceForm.audiences.push({
    data: "",
    id: Date.now(),
    deleted: false,
  } as ProjectDataForm);
}

function handleOnMounted() {
  secondaryAudienceForm.audiences = store.new_project_data
    .filter((p) => p.name == ProjectDataName.secondary_audience)
    .map((i) => {
      return {
        data: i.data,
        deleted: false,
        id: i.id,
      } as ProjectDataForm;
    });

  if (secondaryAudienceForm.audiences.length == 0) {
    addAudience(false);
  }

  primaryAudienceForm.audiences = store.new_project_data
    .filter((p) => p.name == ProjectDataName.primary_audience)
    .map((i) => {
      return {
        data: i.data,
        deleted: false,
        id: i.id,
      } as ProjectDataForm;
    });

  if (primaryAudienceForm.audiences.length == 0) {
    addAudience(true);
  }

  form.value = store
    .questionsForTopic(config.value.suggestions.module)
    .map((question) => {
      const item = store.findByQuestionId(question.id);
      return {
        id: item?.id,
        q_id: question.id,
        label: question.q2u,
        showBuild: question.bulb,
        data: item?.data || "",
        module: ProjectDataModule.audiences,
        deleted: false,
        name: item?.name || "audience",
      };
    });
}

function saveChanges() {
  const temp1 = primaryAudienceForm.audiences.map((i) => ({
    id: i?.id,
    q_id: 11,
    label: "",
    showBuild: false,
    data: i.data || "",
    module: ProjectDataModule.audiences,
    deleted: i.deleted || false,
    name: ProjectDataName.primary_audience,
  }));
  const temp2 = secondaryAudienceForm.audiences.map((i) => ({
    id: i?.id,
    q_id: 11,
    label: "",
    showBuild: false,
    data: i.data || "",
    module: ProjectDataModule.audiences,
    deleted: i.deleted || false,
    name: ProjectDataName.secondary_audience,
  }));

  return store.addOrUpdate([...temp1, ...temp2, ...form.value]).then((_) => {
    config.value.pendingSave = false;
    handleOnMounted();
  });
}

onMounted(() => {
  handleOnMounted();
});

onBeforeRouteLeave((to, from, next) => {
  if (config.value.pendingSave) {
    Modal.confirm({
      title: "You have unsaved changes. Do you want to save them?",
      okText: "Yes. Save Changes",
      cancelText: "Discard Changes",
      onOk: () => {
        return saveChanges().then(() => next());
      },
      onCancel: () => next(),
    });
  } else {
    next();
  }
});

const handleSuggestionSave = (value: string) => {
  form.value = form.value.map((i) => {
    if (i.showBuild) {
      i.data = value;
    }
    return i;
  });
};
</script>

<template>
  <GPTSuggestionPanel
    :is-visible="config.suggestions.isOpened"
    @is-closed="config.suggestions.isOpened = false"
    v-if="config.suggestions.module"
    :question-id="config.suggestions.questionId"
    :module="config.suggestions.module"
    @saved="handleSuggestionSave"
  >
  </GPTSuggestionPanel>

  <Card title="Project Audiences" :bordered="false">
    <template #extra>
      <Button type="primary" @click="saveChanges()">Save Changes</Button>
    </template>

    <BroadcastComponent :module="config.suggestions.module"></BroadcastComponent>

    <Spin :spinning="store.loading" size="large">
      <Form ref="primaryFormRef" :model="primaryAudienceForm" layout="vertical">
        <Row>
          <Col
            :span="16"
            v-for="(item, index) in primaryAudienceForm.audiences.filter(
              (i) => !i.deleted
            )"
          >
            <FormItem
              :key="index"
              :name="['audiences', index, 'value']"
              :rules="{
                required: false,
                message: 'Audience can not be empty',
                trigger: 'change',
              }"
              style="margin-bottom: 10px"
            >
              <template #label v-if="index == 0">
                <span class="font-weight-bold">{{
                  index != 0
                    ? ""
                    : "1. Who is the primary target audience for your project? Who will be adopting the behavior you want to influence?"
                }}</span>
              </template>

              <Input
                v-model:value="item.data"
                placeholder="Enter primary audience"
                style="width: 60%"
                @change="config.pendingSave = true"
              />

              <Button
                type="primary"
                :ghost="true"
                :danger="true"
                size="small"
                v-if="primaryAudienceForm.audiences.length > 1"
                class="ml-2"
                :disabled="primaryAudienceForm.audiences.length === 1"
                @click="deleteAudience(item.id, true)"
              >
                <template #icon>
                  <DeleteOutlined />
                </template>
                Delete
              </Button>
            </FormItem>
          </Col>
        </Row>

        <FormItem>
          <Button
            type="primary"
            :ghost="true"
            style="width: 40%"
            @click="addAudience(true)"
          >
            <PlusOutlined />
            Add Primary Audience
          </Button>
        </FormItem>
      </Form>

      <Form
        ref="audienceFormRef"
        name="audience-form-item"
        :model="secondaryAudienceForm"
        layout="vertical"
      >
        <Row>
          <Col
            :span="16"
            v-for="(item, index) in secondaryAudienceForm.audiences.filter(
              (i) => !i.deleted
            )"
          >
            <FormItem
              :key="index"
              :name="['audiences', index, 'value']"
              :rules="{
                required: false,
                message: 'Audience can not be empty',
                trigger: 'change',
              }"
              style="margin-bottom: 10px"
            >
              <!-- help= -->
              <template #label v-if="index == 0">
                <span class="font-weight-bold">{{
                  index != 0
                    ? ""
                    : "2. Who else influences the actions of your main target audience?"
                }}</span>
              </template>

              <Input
                v-model:value="item.data"
                placeholder="please input audience"
                style="width: 60%"
                @change="config.pendingSave = true"
              >
                <template #suffix>
                  <Tooltip
                    title="What other audiences need to be involved? Who else influences the actions of your main target audience? What other audiences need to be involved?"
                  >
                    <InfoCircleOutlined />
                  </Tooltip>
                </template>
              </Input>

              <Button
                type="primary"
                :ghost="true"
                :danger="true"
                size="small"
                v-if="secondaryAudienceForm.audiences.length > 1"
                class="ml-2"
                :disabled="secondaryAudienceForm.audiences.length === 1"
                @click="deleteAudience(item.id, false)"
              >
                <template #icon>
                  <DeleteOutlined />
                </template>
                Delete
              </Button>
            </FormItem>
          </Col>
        </Row>

        <FormItem>
          <Button
            type="primary"
            :ghost="true"
            style="width: 40%"
            @click="addAudience(false)"
          >
            <PlusOutlined />
            Add Secondary Audience
          </Button>
        </FormItem>
      </Form>

      <Form layout="vertical">
        <Row>
          <Col :span="16" v-for="(q, count) in form">
            <FormItem :name="`input-${count + 3}`" :key="q.id">
              <template #label>
                <span class="font-weight-bold"> {{ count + 3 }}. {{ q.label }}</span>
              </template>

              <img
                v-if="q.showBuild"
                :src="BULB_ICON"
                ref="iconRefs"
                @click="showPanel(q.q_id)"
                class="image is-32x32"
              />

              <Textarea
                @change="config.pendingSave = true"
                v-model:value="q.data"
                :rows="7"
                :cols="40"
              ></Textarea>
            </FormItem>
          </Col>
        </Row>
      </Form>
    </Spin>
  </Card>
</template>
