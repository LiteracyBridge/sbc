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
  Row,
  Col,
  message,
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
import { ApiRequest } from "@/apis/api";
import { useProjectStore } from "@/stores/projects";
import { ProjectData, ProjectDataModule, ProjectDataName } from "@/types";
import { useUserStore } from "@/stores/user";
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
  pendingSave: false,
  // loading: false,
  // projectData: [] as ProjectData[],
  suggestions: {
    questionId: null,
    isOpened: false,
    module: "audiences",
  },
});

// Dynamic objectives forms
const audienceFormRef = ref<FormInstance>();
const primaryFormRef = ref<FormInstance>();
const secondaryAudienceForm = reactive<{
  audiences: ProjectDataForm[];
  deleted: number[];
}>({
  audiences: [],
  deleted: [],
});

const primaryAudienceForm = reactive<{
  audiences: ProjectDataForm[];
  deleted: number[];
}>({
  audiences: [],
  deleted: [],
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

  store.addOrUpdate([...temp1, ...temp2, ...form.value]).then((resp) => {
    config.value.pendingSave = false;
    handleOnMounted();
    // store.addOrUpdate({id, name, module: "audiences", q_id, value: (event.target as HTMLInputElement).value})
    // .then((resp) => {
    //   if(resp != null){
    //     const index = (primary? primaryAudienceForm: secondaryAudienceForm).audiences.findIndex(i => i.id == id);

    //     (primary? primaryAudienceForm: secondaryAudienceForm).audiences[index] = {value: resp.data, id: resp.id, is_new: false};
    //   }
  });
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

  // config.value.pendingSave = true;
  // store.deleteData(id).then((resp) => {
  //   if (resp != null) {
  //     const temp = (primary ? primaryAudienceForm : secondaryAudienceForm).audiences;
  //     const index = temp.findIndex((i) => i.id == id);
  //     temp.splice(index, 1);

  //     (primary ? primaryAudienceForm : secondaryAudienceForm).audiences = temp;
  //   }
  // });
}

// function removeAudience(item: Objective, primary: boolean) {
//   if (primary) {
//     let index = primaryAudienceForm.audiences.indexOf(item);
//     if (index !== -1) {
//       const [el] = primaryAudienceForm.audiences.splice(index, 1);
//       if (!el.is_new) {
//         primaryAudienceForm.deleted.push(el.id);
//       }
//     }
//     return;
//   }

//   let index = secondaryAudienceForm.audiences.indexOf(item);
//   if (index !== -1) {
//     const [el] = secondaryAudienceForm.audiences.splice(index, 1);
//     if (!el.is_new) {
//       secondaryAudienceForm.deleted.push(el.id);
//     }
//   }
// }

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

// function saveForms() {
//   // Save secondary audience
//   audienceFormRef.value.validateFields().then((values) => {
//     // config.value.loading = true;

//     store.updateData({
//       name: "secondary_audience",
//       editing_user_id: useUserStore().id,
//       added: secondaryAudienceForm.audiences
//         .filter(i => i.is_new).map(i => i.value),
//       updated: secondaryAudienceForm.audiences.filter(i => !i.is_new)
//         .map(i => {
//           const _item: Record<string, any> = {};
//           _item[i.id] = i.value;
//           return _item;
//         }),
//       removed: secondaryAudienceForm.deleted,
//       module: "audiences"
//     })
//   });

//   // Save primary audience
//   primaryFormRef.value.validateFields().then((values) => {
//     // config.value.loading = true;

//     store.updateData({
//       name: "primary_audience",
//       editing_user_id: useUserStore().id,
//       added: primaryAudienceForm.audiences
//         .filter(i => i.is_new).map(i => i.value),
//       updated: primaryAudienceForm.audiences.filter(i => !i.is_new)
//         .map(i => {
//           const _item: Record<string, any> = {};
//           _item[i.id] = i.value;
//           return _item;
//         }),
//       removed: primaryAudienceForm.deleted,
//       module: "audiences"
//     })
//   });

// }

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

onMounted(() => {
  handleOnMounted();

  // store.download()
  //   .then((_resp) => {
  //     secondaryAudienceForm.audiences = store.new_project_data
  //       .filter(p => p.name == "secondary_audience")
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

  //     primaryAudienceForm.audiences = store.new_project_data
  //       .filter(p => p.name == "primary_audience")
  //       .map(i => {
  //         return {
  //           value: i.data,
  //           id: i.id,
  //           is_new: false
  //         }
  //       });

  //     if (primaryAudienceForm.audiences.length == 0) {
  //       addAudience(true);
  //     }
  //   })
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
      <Form
        ref="primaryFormRef"
        :model="primaryAudienceForm"
        layout="vertical"
        v-bind="formItemLayoutWithOutLabel"
      >
        <Row>
          <Col
            :span="16"
            v-for="(item, index) in primaryAudienceForm.audiences.filter(
              (i) => !i.deleted
            )"
          >
            <FormItem
              :key="index"
              v-bind="index === 0 ? formItemLayout : {}"
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

        <FormItem v-bind="formItemLayoutWithOutLabel">
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
        v-bind="formItemLayoutWithOutLabel"
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
              v-bind="index === 0 ? formItemLayout : {}"
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

        <FormItem v-bind="formItemLayoutWithOutLabel">
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
