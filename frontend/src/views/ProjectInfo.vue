<script setup lang="ts">

import { Card, Form, FormItem, Image, Textarea, type FormInstance, Input, Button, Divider, message } from 'ant-design-vue';
import { computed, onMounted, reactive, ref, watch } from 'vue';

import { useProjectDataStore } from '@/stores/projectData';
import GPTSuggestionPanel from '@/components/GPTSuggestionPanel.vue';
import { DeleteOutlined, MinusCircleOutlined, PlusOutlined } from '@ant-design/icons-vue';
import { ApiRequest } from '@/apis/api';
import { useProjectStore } from '@/stores/projects';
import { ProjectData } from '@/types';
import { useUserStore } from '@/stores/user';

interface Objective {
  value: string;
  id: number;
  is_new?: boolean;
}

const BULB_ICON = "/images/lightbulb.png"

const projectDataStore = useProjectDataStore();

const config = ref({
  loading: false,
  projectData: [] as ProjectData[],
  suggestions: {
    questionId: null,
    isOpened: false,
    module: "basic"
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
  projectDataStore.setData(id, event.target.value);
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
  console.log(dynamicValidateForm)

  objectivesFormRef.value.validateFields().then((values) => {
    config.value.loading = true;

    const body = {
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
    }

    ApiRequest.post<ProjectData>(`project/${useProjectStore().prj_id}/objectives`, body)
      .then(resp => {
        projectDataStore.project_data = resp
        config.value.projectData = resp;

        message.success("Project objectives updated successfully");
      })
      .catch(err => message.error(err.message))
      .finally(() => config.value.loading = false);
  });
}

function fetchData() {
  config.value.loading = true;
  ApiRequest.get<ProjectData>(`project/${useProjectStore().prj_id}/data`).then((resp) => {
    config.value.projectData = resp;
    dynamicValidateForm.objectives = resp
      .filter(p => p.module == "objectives")
      .map(i => {
        return {
          value: i.data,
          id: i.id,
          is_new: false
        }
      });
  })
    .catch(err => message.error(err.message))
    .finally(() => config.value.loading = false);
}

onMounted(() => {
  fetchData();
})

</script>

<template>
  <GPTSuggestionPanel :is-visible="config.suggestions.isOpened" @is-closed="config.suggestions.isOpened = false;"
    :question-id="config.suggestions.questionId" :module="config.suggestions.module">
  </GPTSuggestionPanel>

  <Card title="Project Info" :loading="config.loading">
    <template #extra>
      <Button type="primary" :ghost="true" @click="saveForms()">Save Changes</Button>
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


    <!-- <Divider>What specific objective(s) will your project achieve? What changes will your project make happen?</Divider> -->
    <!--
    <Form ref="objectivesFormRef" name="dynamic_form_item" :model="dynamicValidateForm"
      v-bind="formItemLayoutWithOutLabel" layout="vertical"> -->

    <!-- <FormItem v-for="(objective, index) in dynamicValidateForm.objectives" :key="objective.id"
        v-bind="index === 0 ? formItemLayout : {}"
        :label="index != 0 ? '' : 'What specific objective(s) will your project achieve? What changes will your project make happen?'"
        :name="['objectives', index, 'value']" :rules="{
          required: true,
          message: 'Objective can not be empty',
          trigger: 'change',
        }">

        <Input v-model:value="objective.value" placeholder="please input objective" style="width: 60%;" />

        <Button type="ghost" :danger="true" size="small" v-if="dynamicValidateForm.objectives.length > 1" class="ml-2"
          :disabled="dynamicValidateForm.objectives.length === 1" @click="removeObjective(objective)">
          <template #icon>
            <DeleteOutlined />
          </template>
          Delete
        </Button>
      </FormItem>

      <FormItem v-bind="formItemLayoutWithOutLabel">
        <Button type="dashed" style="width: 60%" @click="addObjective">
          <PlusOutlined />
          Add Objective
        </Button>
      </FormItem> -->

    <!-- <FormItem v-bind="formItemLayoutWithOutLabel">
              <Button type="primary" html-type="submit" @click="submitForm">Submit</Button>
              <Button style="margin-left: 10px" @click="resetForm">Reset</Button>
            </FormItem> -->
    <!-- </Form> -->
  </Card>
</template>
