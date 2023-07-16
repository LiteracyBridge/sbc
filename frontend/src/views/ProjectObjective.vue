<script setup lang="ts">

import { Card, Form, FormItem, Image, Textarea, type FormInstance, Input, Button, Divider, message } from 'ant-design-vue';
import { computed, onMounted, reactive, ref, watch } from 'vue';

import { useProjectDataStore } from '@/stores/projectData';
import GPTSuggestionPanel from '@/components/GPTSuggestionPanel.vue';
import MessageModal from '@/components/MessageModal.vue';
import BroadcastComponent from '@/components/BroadcastComponent.vue';

import { DeleteOutlined, MinusCircleOutlined, PlusOutlined } from '@ant-design/icons-vue';
import { useUserStore } from '@/stores/user';

interface Objective {
  value: string;
  id: number;
  is_new?: boolean;
}

const BULB_ICON = "/images/lightbulb.png"

const store = useProjectDataStore();

const config = ref({
  messages: false,
  suggestions: {
    questionId: null,
    isOpened: false,
    module: "objectives"
  },
});

// Dynamic objectives forms
const objectivesFormRef = ref<FormInstance>();
const dynamicValidateForm = reactive<{ objectives: Objective[], deleted: number[] }>({
  objectives: [],
  deleted: []
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

// Dynamic objectives forms
function removeObjective(item: Objective) {
  let index = dynamicValidateForm.objectives.indexOf(item);
  if (index !== -1) {
    const [el] = dynamicValidateForm.objectives.splice(index, 1);

    console.log(el)
    if (!el.is_new) {
      dynamicValidateForm.deleted.push(el.id);
    }
  }
}

function addObjective() {
  dynamicValidateForm.objectives.push({
    value: '',
    id: Date.now(),
    is_new: true
  });
};

function saveForms() {
  objectivesFormRef.value.validateFields().then((values) => {
    store.updateData({
      name: "specific_objective",
      module: "objectives",
      editing_user_id: useUserStore().id,
      added: dynamicValidateForm.objectives
        .filter(i => i.is_new).map(i => i.value),
      updated: dynamicValidateForm.objectives.filter(i => !i.is_new)
        .map(i => {
          const _item: Record<string, any> = {};
          _item[i.id] = i.value;
          return _item;
        }),
      removed: dynamicValidateForm.deleted
    });
  });
}

function fetchData() {
  store.download().then((resp) => {
    dynamicValidateForm.objectives = store.new_project_data
      .filter(p => p.module == "objectives")
      .map(i => {
        return {
          value: i.data,
          id: i.id,
          is_new: false
        }
      });

    if (dynamicValidateForm.objectives.length == 0) {
      addObjective();
    }
  });
}

onMounted(() => {
  fetchData();
});
</script>

<template>
  <GPTSuggestionPanel
    :is-visible="config.suggestions.isOpened"
    @is-closed="config.suggestions.isOpened = false"
    :question-id="config.suggestions.questionId"
    :module="config.suggestions.module"
  >
  </GPTSuggestionPanel>

  <Card class="section" title="Project Objectives" :loading="store.loading">
    <template #extra>
      <Button type="primary" @click="saveForms()">Save Changes</Button>
    </template>

    <BroadcastComponent :module="config.suggestions.module"></BroadcastComponent>

    <Form layout="vertical">
      <!-- <div class="columns mx-4 is-vcentered"> -->

      <!-- <div class="column is-8"> -->

      <!-- <strong>{{ count + 1 }}. {{ q.q2u }} </strong><br />
      <img v-if="q.bulb" :src="BULB_ICON" ref="iconRefs" @click="submitContextAndPrompt(q.id, topic)"
        class="image is-32x32" />
      <textarea @change="updateData($event, q.id)" :value="projectDataStore.getData(q.id)" rows="4" cols="80" /><br />
      <br /><br /> -->

      <FormItem
        :name="`input-${count + 1}`"
        v-for="(q, count) in store.questionsForTopic(config.suggestions.module)"
        :key="q.id"
      >
        <template #label>
          <span class="font-weight-bold"> {{ count + 1 }}. {{ q.q2u }}</span>
        </template>
        <!-- <label class="label" :for="`input-${count + 1}`">{{ count + 1 }}. {{ q.q2u }}</label> -->

        <!-- <div class="control"> -->
        <img
          v-if="q.bulb"
          :src="BULB_ICON"
          ref="iconRefs"
          @click="showPanel(q.id)"
          class="image is-32x32"
        />
        <!-- </div> -->

        <!-- <div class="control"> -->
        <Textarea
          @change="updateData($event, q.id)"
          :value="store.getData(q.id)"
          :rows="7"
          :cols="40"
          style="width: 70%"
        ></Textarea>

        <!-- </div> -->
      </FormItem>
      <!-- </div> -->

      <!-- </div> -->
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
        v-for="(objective, index) in dynamicValidateForm.objectives"
        :key="objective.id"
        v-bind="index === 0 ? formItemLayout : {}"
        :name="['objectives', index, 'value']"
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
          v-model:value="objective.value"
          placeholder="Enter objective"
          style="width: 60%"
        />

        <Button
          type="ghost"
          :danger="true"
          size="small"
          v-if="dynamicValidateForm.objectives.length > 1"
          class="ml-2"
          :disabled="dynamicValidateForm.objectives.length === 1"
          @click="removeObjective(objective)"
        >
          <template #icon>
            <DeleteOutlined />
          </template>
          Delete
        </Button>
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
  </Card>
</template>
