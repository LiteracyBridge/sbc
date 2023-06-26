<script setup lang="ts">

import {
  Card, Form, FormItem, Image, Textarea,
  type FormInstance, Input, Button, Divider, Row, Col, message
} from 'ant-design-vue';
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

const store = useProjectDataStore();

const config = ref({
  // loading: false,
  // projectData: [] as ProjectData[],
  suggestions: {
    questionId: null,
    isOpened: false,
    module: "audiences"
  },
});

// Dynamic objectives forms
const audienceFormRef = ref<FormInstance>();
const primaryFormRef = ref<FormInstance>();
const secondaryAudienceForm = reactive<{
  audiences: Objective[], deleted: number[]
}>({
  audiences: [],
  deleted: []
});

const primaryAudienceForm = reactive<{
  audiences: Objective[], deleted: number[]
}>({
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
  store.setData(id, event.target.value);
}

// Dynamic objectives forms
function removeAudience(item: Objective, primary: boolean) {
  if (primary) {
    let index = primaryAudienceForm.audiences.indexOf(item);
    if (index !== -1) {
      const [el] = primaryAudienceForm.audiences.splice(index, 1);
      if (!el.is_new) {
        primaryAudienceForm.deleted.push(el.id);
      }
    }
    return;
  }

  let index = secondaryAudienceForm.audiences.indexOf(item);
  if (index !== -1) {
    const [el] = secondaryAudienceForm.audiences.splice(index, 1);
    if (!el.is_new) {
      secondaryAudienceForm.deleted.push(el.id);
    }
  }
}

function addAudience(primary: boolean) {
  if (primary) {
    primaryAudienceForm.audiences.push({
      value: '',
      id: Date.now(),
      is_new: true
    });
    return;
  }

  secondaryAudienceForm.audiences.push({
    value: '',
    id: Date.now(),
    is_new: true
  });
};

function saveForms() {
  // Save secondary audience
  audienceFormRef.value.validateFields().then((values) => {
    // config.value.loading = true;

    store.updateData({
      name: "secondary_audience",
      editing_user_id: useUserStore().id,
      added: secondaryAudienceForm.audiences
        .filter(i => i.is_new).map(i => i.value),
      updated: secondaryAudienceForm.audiences.filter(i => !i.is_new)
        .map(i => {
          const _item: Record<string, any> = {};
          _item[i.id] = i.value;
          return _item;
        }),
      removed: secondaryAudienceForm.deleted,
      module: "audiences"
    })
  });

  // Save primary audience
  primaryFormRef.value.validateFields().then((values) => {
    // config.value.loading = true;

    store.updateData({
      name: "primary_audience",
      editing_user_id: useUserStore().id,
      added: primaryAudienceForm.audiences
        .filter(i => i.is_new).map(i => i.value),
      updated: primaryAudienceForm.audiences.filter(i => !i.is_new)
        .map(i => {
          const _item: Record<string, any> = {};
          _item[i.id] = i.value;
          return _item;
        }),
      removed: primaryAudienceForm.deleted,
      module: "audiences"
    })
  });

}

// function fetchData() {
//   config.value.loading = true;
//   ApiRequest.get<ProjectData>(`project/${useProjectStore().prj_id}/data`).then((resp) => {
//     config.value.projectData = resp;
//     secondaryAudienceForm.audiences = resp
//       .filter(p => p.module == config.value.suggestions.module)
//       .map(i => {
//         return {
//           value: i.data,
//           id: i.id,
//           is_new: false
//         }
//       });

//     if (secondaryAudienceForm.audiences.length == 0) {
//       addAudience(false);
//     }
//   })
//     .catch(err => message.error(err.message))
//     .finally(() => config.value.loading = false);
// }

onMounted(() => {
  store.download()
    .then((_resp) => {
      secondaryAudienceForm.audiences = store.new_project_data
        .filter(p => p.name == "secondary_audience")
        .map(i => {
          return {
            value: i.data,
            id: i.id,
            is_new: false
          }
        });

      if (secondaryAudienceForm.audiences.length == 0) {
        addAudience(false);
      }

      primaryAudienceForm.audiences = store.new_project_data
        .filter(p => p.name == "primary_audience")
        .map(i => {
          return {
            value: i.data,
            id: i.id,
            is_new: false
          }
        });

      if (primaryAudienceForm.audiences.length == 0) {
        addAudience(true);
      }
    })
})

</script>

<template>
  <GPTSuggestionPanel :is-visible="config.suggestions.isOpened" @is-closed="config.suggestions.isOpened = false;"
    :question-id="config.suggestions.questionId" :module="config.suggestions.module">
  </GPTSuggestionPanel>

  <Card class="section" title="Project Audiences" :loading="store.loading">
    <template #extra>
      <Button type="primary" :ghost="true" :loading="store.loading" @click="saveForms()">Save Changes</Button>
    </template>

    <Form ref="primaryFormRef" :model="primaryAudienceForm" layout="vertical" v-bind="formItemLayoutWithOutLabel">

      <Row>
        <Col :span="16" v-for="(objective, index) in primaryAudienceForm.audiences">

        <FormItem :key="objective.id" v-bind="index === 0 ? formItemLayout : {}"
          :label="index != 0 ? '' : 'Who is the primary target audience for your project? Who will be adopting the behavior you want to influence?'"
          :name="['audiences', index, 'value']" :rules="{
            required: true,
            message: 'Audience can not be empty',
            trigger: 'change',
          }" style="margin-bottom: 10px;">

          <Input v-model:value="objective.value" placeholder="Enter primary audience" style="width: 60%;" />

          <Button type="ghost" :danger="true" size="small" v-if="primaryAudienceForm.audiences.length > 1" class="ml-2"
            :disabled="primaryAudienceForm.audiences.length === 1" @click="removeAudience(objective, true)">

            <template #icon>
              <DeleteOutlined />
            </template>
            Delete
          </Button>
        </FormItem>

        </Col>
      </Row>

      <FormItem v-bind="formItemLayoutWithOutLabel">
        <Button type="dashed" @click="addAudience(true)">
          <PlusOutlined />
          Add Primary Audience
        </Button>
      </FormItem>

    </Form>


    <Form layout="vertical">
      <Row>
        <Col :span="16" v-for="(q, count) in store.questionsForTopic(config.suggestions.module)">

        <FormItem :name="`input-${count + 1}`" :key="q.id">
          <template #label>
            {{ count + 1 }}. {{ q.q2u }}
          </template>

          <img v-if="q.bulb" :src="BULB_ICON" ref="iconRefs" @click="showPanel(q.id)" class="image is-32x32" />

          <Textarea @change="updateData($event, q.id)" :value="store.getData(q.id)" :rows="7" :cols="40"></Textarea>

        </FormItem>

        </Col>
      </Row>


    </Form>

    <Form ref="audienceFormRef" name="audience-form-item" :model="secondaryAudienceForm" layout="vertical"
      v-bind="formItemLayoutWithOutLabel">

      <Row>
        <Col :span="16" v-for="(objective, index) in secondaryAudienceForm.audiences">
        <FormItem :key="objective.id" v-bind="index === 0 ? formItemLayout : {}"
          :label="index != 0 ? '' : '3. Who else influences the actions of your main target audience?'"
          :name="['audiences', index, 'value']" :rules="{
            required: true,
            message: 'Audience can not be empty',
            trigger: 'change',
          }"
          help="What other audiences need to be involved? Who else influences the actions of your main target audience? What other audiences need to be involved?"
          style="margin-bottom: 10px;">

          <Input v-model:value="objective.value" placeholder="please input audience" style="width: 60%;" />

          <Button type="ghost" :danger="true" size="small" v-if="secondaryAudienceForm.audiences.length > 1" class="ml-2"
            :disabled="secondaryAudienceForm.audiences.length === 1" @click="removeAudience(objective, false)">

            <template #icon>
              <DeleteOutlined />
            </template>
            Delete
          </Button>
        </FormItem>

        </Col>
      </Row>

      <FormItem v-bind="formItemLayoutWithOutLabel">
        <Button type="dashed" @click="addAudience(false)">
          <PlusOutlined />
          Add Audience
        </Button>
      </FormItem>

    </Form>
  </Card>
</template>
