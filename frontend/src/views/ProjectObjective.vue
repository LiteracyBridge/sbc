<script setup lang="ts">
import {
  Card,
  Form,
  FormItem,
  Image,
  Textarea,
  Input,
  Button,
  Divider,
  Spin,
  Popconfirm,
  Modal,
} from "ant-design-vue";
import { computed, onMounted, reactive, ref, watch } from "vue";
import type { FormInstance } from "ant-design-vue";
import { ProjectDataForm, useProjectDataStore } from "@/stores/projectData";
import GPTSuggestionPanel from "@/components/GPTSuggestionPanel.vue";
import BroadcastComponent from "@/components/BroadcastComponent.vue";

import { DeleteOutlined, MinusCircleOutlined, PlusOutlined } from "@ant-design/icons-vue";
import { ProjectDataModule, ProjectData, ProjectDataName } from "@/types";
import { onBeforeRouteLeave } from "vue-router";

interface Objective {
  value: string;
  id: number;
  is_new?: boolean;
}

const BULB_ICON = "/images/lightbulb.png";

const store = useProjectDataStore();

const form = ref<ProjectDataForm[]>([]);
const config = ref({
  messages: false,
  pendingSave: false,
  suggestions: {
    questionId: null,
    isOpened: false,
    module: ProjectDataModule.objectives,
  },
});

// Dynamic objectives forms
const objectivesFormRef = ref<FormInstance>();
const dynamicValidateForm = reactive<{
  items: Partial<ProjectDataForm[]>;
}>({
  items: [],
});

const formItemLayout = {
  // labelCol: {
  //   xs: { span: 24 },
  //   sm: { span: 4 },
  // },
  // wrapperCol: {
  //   xs: { span: 24 },
  //   sm: { span: 20 },
  // },
};
const formItemLayoutWithOutLabel = {
  // wrapperCol: {
  //   xs: { span: 24, offset: 0 },
  //   sm: { span: 20, offset: 4 },
  // },
};

function showPanel(id: string | number) {
  config.value.suggestions.questionId = id;
  config.value.suggestions.module = config.value.suggestions.module;
  config.value.suggestions.isOpened = true;
}

function updateData(event: any, id: number) {
  store.setData(id, event.target.value);
}

function addObjective() {
  dynamicValidateForm.items.push({
    data: "",
    id: Date.now(),
    deleted: false,
  } as ProjectDataForm);
}

// const objectivesModel = computed(() => {
//   return dynamicValidateForm.objectives.map((i) => i.value);
// });

// function fetchData() {
//   store.download().then((resp) => {
//     dynamicValidateForm.objectives = store.new_project_data
//       .filter((p) => p.module == "objectives")
//       .map((i) => {
//         return {
//           value: i.data,
//           id: i.id,
//           is_new: false,
//         };
//       });

//     if (dynamicValidateForm.objectives.length == 0) {
//       addObjective();
//     }
//   });
// }

function deleteObj(id: number | string) {
  dynamicValidateForm.items = dynamicValidateForm.items.map((i) => {
    if (i.id == id) i.deleted = true;
    return i;
  });
  config.value.pendingSave = true;
}

function handleOnMounted() {
  dynamicValidateForm.items = store.new_project_data
    .filter((p) => p.name == ProjectDataName.specific_objective)
    .map((i) => {
      return {
        data: i.data,
        id: i.id,
        deleted: false,
      } as ProjectDataForm;
    });

  if (dynamicValidateForm.items.length == 0) {
    addObjective();
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
        module: ProjectDataModule.objectives,
        deleted: false,
        name: item?.name || "objective",
      };
    });
}

function saveChanges() {
  const temp = dynamicValidateForm.items.map((i) => ({
    id: i?.id,
    q_id: 10,
    label: "",
    showBuild: false,
    data: i.data || "",
    module: ProjectDataModule.objectives,
    deleted: i.deleted || false,
    name: ProjectDataName.specific_objective,
  }));

  store.addOrUpdate([...temp, ...form.value]).then((resp) => {
    config.value.pendingSave = false;
    handleOnMounted();
    // if (resp != null) {
    //   const index = dynamicValidateForm.objectives.findIndex((i) => i.id == id);

    //   dynamicValidateForm.objectives[index] = {
    //     value: resp.data,
    //     id: resp.id,
    //     is_new: false,
    //   };
    // }
  });
}

// function saveChanges2() {
//   store.addOrUpdate(form.value).then((resp) => (config.value.pendingSave = false));
// }

onMounted(() => {
  handleOnMounted();
});

onBeforeRouteLeave((to, from, next) => {
  if (config.value.pendingSave) {
    Modal.confirm({
      title: "You have unsaved changes. Are you sure you want to leave?",
      onOk: () => {
        next();
      },
      onCancel: () => {
        next(false);
      },
    });
  } else {
    next();
  }
});

const handleSuggestionSave = (value: string) => {
  form.value = form.value.map((i) => {
    if (i.q_id == config.value.suggestions.questionId) {
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
    :question-id="config.suggestions.questionId"
    :module="config.suggestions.module"
    @saved="handleSuggestionSave"
  >
  </GPTSuggestionPanel>

  <Card title="Project Objectives" :bordered="false">
    <template #extra>
      <Button type="primary" @click="saveChanges()">Save Changes</Button>
    </template>

    <BroadcastComponent :module="config.suggestions.module"></BroadcastComponent>

    <Spin :spinning="store.loading">
      <Form layout="vertical">
        <FormItem :name="`input-${count + 1}`" v-for="(q, count) in form" :key="q.q_id">
          <template #label>
            <span class="font-weight-bold"> {{ count + 1 }}. {{ q.label }}</span>
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
            style="width: 70%"
          ></Textarea>
        </FormItem>
      </Form>

      <!-- <Divider>What specific objective(s) will your project achieve? What changes will your project make happen?</Divider> -->

      <Form
        ref="objectivesFormRef"
        name="dynamic_form_item"
        :model="dynamicValidateForm"
        v-bind="formItemLayoutWithOutLabel"
        layout="vertical"
      >
        <FormItem
          v-for="(objective, index) in dynamicValidateForm.items.filter(
            (i) => !i.deleted
          )"
          :key="objective.id"
          v-bind="index === 0 ? formItemLayout : {}"
          :name="['items', index, 'value']"
          :rules="{
            required: false,
            message: 'Objective can not be empty',
            trigger: 'change',
          }"
        >
          <template #label v-if="index == 0">
            <span class="font-weight-bold"
              >{{
                index != 0
                  ? ""
                  : "3. What specific objective(s) will your project achieve? What changes will your project make happen?"
              }}
            </span>
          </template>

          <Input
            v-model:value="objective.data"
            placeholder="Enter objective"
            style="width: 60%"
            @change="config.pendingSave = true"
          />

          <Popconfirm
            title="All associated theory of change, communications and indictors will be deleted. Are you sure?"
            @confirm="deleteObj(objective.id)"
          >
            <Button
              type="primary"
              :ghost="true"
              :danger="true"
              size="small"
              v-if="dynamicValidateForm.items.length > 1"
              class="ml-2"
              :disabled="dynamicValidateForm.items.length === 1"
            >
              <template #icon>
                <DeleteOutlined />
              </template>
              Delete
            </Button>
          </Popconfirm>
        </FormItem>

        <FormItem v-bind="formItemLayoutWithOutLabel">
          <Button type="primary" :ghost="true" style="width: 60%" @click="addObjective">
            <PlusOutlined />
            Add Objective
          </Button>
        </FormItem>

        <!-- <FormItem v-bind="formItemLayoutWithOutLabel">
              <Button type="primary" html-type="submit" @click="submitForm">Submit</Button>
              <Button style="margin-left: 10px" @click="resetForm">Reset</Button>
            </FormItem> -->
      </Form>
    </Spin>
  </Card>
</template>
