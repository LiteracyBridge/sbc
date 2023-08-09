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
} from "ant-design-vue";
import { onMounted, ref, watch } from "vue";
import { ProjectDataUpdateDto, useProjectDataStore } from "@/stores/projectData";
import GPTSuggestionPanel from "@/components/GPTSuggestionPanel.vue";
import { useTheoryOfChangeStore } from "@/stores/theory_of_change";
import { ProjectDataModule } from "@/types";
import BroadcastComponent from "@/components/BroadcastComponent.vue";

const BULB_ICON = "/images/lightbulb.png";

const projectDataStore = useProjectDataStore();

const form = ref<
  {
    label: string;
    data: string;
    module: ProjectDataModule;
    id?: number;
    q_id: number;
    showBuild: boolean;
  }[]
>([]);
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

function updateData(event: any, id: number) {
  projectDataStore.setData(id, event.target.value);
}

const updateSector = (value: any, id: number) => {
  projectDataStore.setData(id, value);
};

onMounted(() => {
  form.value = projectDataStore
    .questionsForTopic(config.value.suggestions.module)
    .map((question) => {
      const item = projectDataStore.getData(question.id);
      return {
        id: item?.id,
        q_id: question.id,
        label: question.q2u,
        showBuild: question.bulb,
        data: item?.data || "",
        module: ProjectDataModule.basics,
      };
    });
});

function saveChanges() {
  projectDataStore.addOrUpdate(form.value as ProjectDataUpdateDto[]);
}
</script>

<template>
  <GPTSuggestionPanel
    :is-visible="config.suggestions.isOpened"
    @is-closed="config.suggestions.isOpened = false"
    :question-id="config.suggestions.questionId"
    :module="config.suggestions.module"
  >
  </GPTSuggestionPanel>

  <Card title="Project Info" :loading="config.loading" :bordered="false">
    <template #extra>
      <Button type="primary" @click="saveChanges()">Save Changes</Button>
    </template>

    <BroadcastComponent :module="config.suggestions.module"></BroadcastComponent>

    <Form layout="vertical" @values-change="config.pendingSave = true">
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
            ></Textarea>
          </FormItem>
        </Col>
      </Row>
    </Form>
  </Card>
</template>
