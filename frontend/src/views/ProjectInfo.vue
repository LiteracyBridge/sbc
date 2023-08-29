<script setup lang="ts">
import {
  Card,
  Form,
  FormItem,
  Select,
  SelectOption,
  Textarea,
  Row,
  Col,
  Button,
  Modal,
  Spin,
} from "ant-design-vue";
import { onMounted, ref, watch } from "vue";
import { ProjectDataForm, useProjectDataStore } from "@/stores/projectData";
import GPTSuggestionPanel from "@/components/GPTSuggestionPanel.vue";
import { useTheoryOfChangeStore } from "@/stores/theory_of_change";
import { ProjectDataModule } from "@/types";
import BroadcastComponent from "@/components/BroadcastComponent.vue";
import { onBeforeRouteLeave } from "vue-router";
import type { FormInstance } from "ant-design-vue";
const BULB_ICON = "/images/lightbulb.png";

const projectDataStore = useProjectDataStore();

const form = ref<ProjectDataForm[]>([]);
const config = ref({
  messages: false,
  loading: false,
  pendingSave: false,
  suggestions: {
    questionId: null,
    isOpened: false,
    module: "basic",
  },
});

function showPanel(id: string | number) {
  config.value.suggestions.questionId = id;
  config.value.suggestions.module = config.value.suggestions.module;
  config.value.suggestions.isOpened = true;
}

// function updateData(event: any, id: number) {
//   projectDataStore.setData(id, event.target.value);
// }

// const updateSector = (value: any, id: number) => {
//   projectDataStore.setData(id, value);
// };

function saveChanges() {
  return projectDataStore
    .addOrUpdate(form.value)
    .then((_) => (config.value.pendingSave = false));
}

onMounted(() => {
  form.value = projectDataStore
    .questionsForTopic(config.value.suggestions.module)
    .map((question) => {
      const item = projectDataStore.findByQuestionId(question.id);
      return {
        id: item?.id,
        q_id: question.id,
        label: question.q2u,
        showBuild: question.bulb,
        data: item?.data || "",
        module: ProjectDataModule.basics,
        deleted: false,
      };
    });
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

  <Card title="Project Info" :loading="config.loading" :bordered="false">
    <template #extra>
      <Button type="primary" @click="saveChanges()">Save Changes</Button>
    </template>

    <BroadcastComponent :module="config.suggestions.module"></BroadcastComponent>

    <Spin :spinning="projectDataStore.loading">
      <Form layout="vertical" ref="infoForm">
        <Row>
          <Col :span="14">
            <FormItem
              :name="`input-${index + 1}`"
              v-for="(item, index) in form"
              :key="index"
            >
              <template #label>
                <span class="font-weight-bold"> {{ index + 1 }}. {{ item.label }} </span>
              </template>
              <Select
                v-if="item.q_id == 1"
                v-model:value="item.data"
                style="padding-bottom: 15px"
                class="font-weight-bold"
                @change="config.pendingSave = true"
              >
                <SelectOption
                  v-for="(sector, index) in useTheoryOfChangeStore().getIndiKitSectors"
                  :key="index"
                  :value="sector"
                >
                  {{ sector }}
                </SelectOption>
              </Select>

              <!-- <div class="control"> -->
              <img
                v-if="item.showBuild"
                :src="BULB_ICON"
                ref="iconRefs"
                @click="showPanel(item.q_id)"
                class="image is-32x32"
              />

              <Textarea
                v-if="item.q_id != 1"
                v-model:value="item.data"
                :rows="7"
                :cols="40"
                @change="config.pendingSave = true"
              ></Textarea>
            </FormItem>
          </Col>
        </Row>
      </Form>
    </Spin>
  </Card>
</template>
