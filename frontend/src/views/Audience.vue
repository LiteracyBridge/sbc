<script setup lang="ts">

import { Card, Form, FormItem, Image, Textarea, type FormInstance, Input, Button, Divider, message } from 'ant-design-vue';
import { computed, onMounted, reactive, ref, watch } from 'vue';

import { useProjectDataStore } from '@/stores/projectData';
import GPTSuggestionPanel from '@/components/GPTSuggestionPanel.vue';
import { DeleteOutlined, PlusOutlined } from '@ant-design/icons-vue';
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
    module: "audiences"
  },
});

// Dynamic objectives forms
const audienceFormRef = ref<FormInstance>();
const dynamicValidateForm = reactive<{ audiences: Objective[], deleted: number[] }>({
  audiences: [],
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
function removeAudience(item: Objective) {
  let index = dynamicValidateForm.audiences.indexOf(item);
  if (index !== -1) {
    const [el] = dynamicValidateForm.audiences.splice(index, 1);

    console.log(el)
    if (!el.is_new) {
      dynamicValidateForm.deleted.push(el.id);
    }
  }
}

function addAudience() {
  dynamicValidateForm.audiences.push({
    value: '',
    id: Date.now(),
    is_new: true
  });
};

function saveForms() {
  console.log(dynamicValidateForm)

  audienceFormRef.value.validateFields().then((values) => {
    config.value.loading = true;

    const body = {
      editing_user_id: useUserStore().id,
      added: dynamicValidateForm.audiences
        .filter(i => i.is_new).map(i => i.value),
      updated: dynamicValidateForm.audiences.filter(i => !i.is_new)
        .map(i => {
          const _item: Record<string, any> = {};
          _item[i.id] = i.value;
          return _item;
        }),
      removed: dynamicValidateForm.deleted
    }

    ApiRequest.post<ProjectData>(`project/${useProjectStore().prj_id}/audience`, body)
      .then(resp => {
        projectDataStore.project_data = resp
        config.value.projectData = resp;

        message.success("Project audiences updated successfully");
      })
      .catch(err => message.error(err.message))
      .finally(() => config.value.loading = false);
  });
}

function fetchData() {
  config.value.loading = true;
  ApiRequest.get<ProjectData>(`project/${useProjectStore().prj_id}/data`).then((resp) => {
    config.value.projectData = resp;
    dynamicValidateForm.audiences = resp
      .filter(p => p.module == config.value.suggestions.module)
      .map(i => {
        return {
          value: i.data,
          id: i.id,
          is_new: false
        }
      });

    if (dynamicValidateForm.audiences.length == 0) {
      addAudience();
    }
  })
    .catch(err => message.error(err.message))
    .finally(() => config.value.loading = false);
}

onMounted(() => {
  fetchData();
})

const getObjectivesData = computed(() => {
  return config.value.projectData.filter(i => i.module == "objectives");
});
</script>

<template>
  <GPTSuggestionPanel :is-visible="config.suggestions.isOpened" @is-closed="config.suggestions.isOpened = false;"
    :question-id="config.suggestions.questionId" :module="config.suggestions.module">
  </GPTSuggestionPanel>

  <Card class="section" title="Project Audiences" :loading="config.loading">
    <template #extra>
      <Button type="primary" :ghost="true" @click="saveForms()">Save Changes</Button>
    </template>

    <Form layout="vertical">

      <FormItem :name="`input-${count + 1}`"
        v-for="(q, count) in projectDataStore.questionsForTopic(config.suggestions.module)" :key="q.id">
        <template #label>
          {{ count + 1 }}. {{ q.q2u }}
        </template>

        <img v-if="q.bulb" :src="BULB_ICON" ref="iconRefs" @click="showPanel(q.id)" class="image is-32x32" />

        <Textarea @change="updateData($event, q.id)" :value="projectDataStore.getData(q.id)" :rows="7" :cols="40"
          style="width: 70%;"></Textarea>

      </FormItem>

    </Form>

    <Form ref="audienceFormRef" name="audience-form-item" :model="dynamicValidateForm" layout="vertical"
      v-bind="formItemLayoutWithOutLabel">

      <FormItem v-for="(objective, index) in dynamicValidateForm.audiences" :key="objective.id"
        v-bind="index === 0 ? formItemLayout : {}"
        :label="index != 0 ? '' : 'Who else influences the actions of your main target audience? What other audiences need to be involved? Who else influences the actions of your main target audience? What other audiences need to be involved?'"
        :name="['audiences', index, 'value']" :rules="{
          required: true,
          message: 'Audience can not be empty',
          trigger: 'change',
        }">

        <Input v-model:value="objective.value" placeholder="please input audience" style="width: 60%;" />

        <Button type="ghost" :danger="true" size="small" v-if="dynamicValidateForm.audiences.length > 1" class="ml-2"
          :disabled="dynamicValidateForm.audiences.length === 1" @click="removeAudience(objective)">
          <template #icon>
            <DeleteOutlined />
          </template>
          Delete
        </Button>
      </FormItem>

      <FormItem v-bind="formItemLayoutWithOutLabel">
        <Button type="dashed" style="width: 60%" @click="addAudience">
          <PlusOutlined />
          Add Audience
        </Button>
      </FormItem>

    </Form>
  </Card>
</template>
