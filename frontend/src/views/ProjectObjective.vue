<script setup lang="ts">

import { Card, Form, FormItem, Image, Textarea, type FormInstance, Input, Button, Divider } from 'ant-design-vue';
import { reactive, ref } from 'vue';

import { useProjectDataStore } from '@/stores/projectData';
import GPTSuggestionPanel from '@/components/GPTSuggestionPanel.vue';
import { DeleteOutlined, MinusCircleOutlined, PlusOutlined } from '@ant-design/icons-vue';

interface Objective {
  value: string;
  key: number;
}

const BULB_ICON = "/images/lightbulb.png"

const projectDataStore = useProjectDataStore();

const config = ref({
  suggestions: {
    questionId: null,
    isOpened: false,
    module: "objectives"
  }
});

// Dynamic objectives forms
const objectivesFormRef = ref<FormInstance>();
const dynamicValidateForm = reactive<{ objectives: Objective[] }>({
  objectives: [],
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
  projectDataStore.setData(id, event.target.value);
}

// Dynamic objectives forms
function removeDomain(item: Objective) {
  let index = dynamicValidateForm.objectives.indexOf(item);
  if (index !== -1) {
    dynamicValidateForm.objectives.splice(index, 1);
  }
}

function addDomain() {
  dynamicValidateForm.objectives.push({
    value: '',
    key: Date.now(),
  });
};

function saveForms() {
  console.log(dynamicValidateForm)
  objectivesFormRef.value.validateFields().then((values) => {
    console.log(values);
  }).catch((error) => {
    console.log(error);
  });
}
</script>

<template>
  <GPTSuggestionPanel :is-visible="config.suggestions.isOpened" @is-closed="config.suggestions.isOpened = false;"
    :question-id="config.suggestions.questionId" :module="config.suggestions.module">
  </GPTSuggestionPanel>

  <Card class="section" title="Project Objectives">
    <template #extra>
      <Button type="primary" :ghost="true" @click="saveForms()">Save</Button>
    </template>

    <Form layout="vertical">
      <!-- <div class="columns mx-4 is-vcentered"> -->

      <!-- <div class="column is-8"> -->

      <!-- <strong>{{ count + 1 }}. {{ q.q2u }} </strong><br />
      <img v-if="q.bulb" :src="BULB_ICON" ref="iconRefs" @click="submitContextAndPrompt(q.id, topic)"
        class="image is-32x32" />
      <textarea @change="updateData($event, q.id)" :value="projectDataStore.getData(q.id)" rows="4" cols="80" /><br />
      <br /><br /> -->

      <FormItem :name="`input-${count + 1}`"
        v-for="(q, count) in projectDataStore.questionsForTopic(config.suggestions.module)" :key="q.id">
        <template #label>
          {{ count + 1 }}. {{ q.q2u }}
        </template>
        <!-- <label class="label" :for="`input-${count + 1}`">{{ count + 1 }}. {{ q.q2u }}</label> -->

        <!-- <div class="control"> -->
        <img v-if="q.bulb" :src="BULB_ICON" ref="iconRefs" @click="showPanel(q.id)" class="image is-32x32" />
        <!-- </div> -->

        <!-- <div class="control"> -->
        <Textarea @change="updateData($event, q.id)" :value="projectDataStore.getData(q.id)" :rows="7" :cols="40"
          style="width: 70%;"></Textarea>

        <!-- </div> -->

      </FormItem>
      <!-- </div> -->

      <!-- </div> -->
    </Form>


    <Divider>What specific objective(s) will your project achieve? What changes will your project make happen?</Divider>

    <Form ref="objectivesFormRef" name="dynamic_form_item" :model="dynamicValidateForm"
      v-bind="formItemLayoutWithOutLabel">

      <FormItem v-for="(objective, index) in dynamicValidateForm.objectives" :key="objective.key"
        v-bind="index === 0 ? formItemLayout : {}" label="" :name="['objectives', index, 'value']" :rules="{
          required: true,
          message: 'objective can not be null',
          trigger: 'change',
        }">

        <Input v-model:value="objective.value" placeholder="please input objective" style="width: 60%;" />

        <Button type="ghost" :danger="true" size="small" v-if="dynamicValidateForm.objectives.length > 1" class="ml-2"
          :disabled="dynamicValidateForm.objectives.length === 1" @click="removeDomain(objective)">
          <template #icon>
            <DeleteOutlined />
          </template>
          Delete
        </Button>
      </FormItem>

      <FormItem v-bind="formItemLayoutWithOutLabel">
        <Button type="dashed" style="width: 60%" @click="addDomain">
          <PlusOutlined />
          Add objective
        </Button>
      </FormItem>

      <!-- <FormItem v-bind="formItemLayoutWithOutLabel">
            <Button type="primary" html-type="submit" @click="submitForm">Submit</Button>
            <Button style="margin-left: 10px" @click="resetForm">Reset</Button>
          </FormItem> -->
    </Form>
  </Card>
</template>
