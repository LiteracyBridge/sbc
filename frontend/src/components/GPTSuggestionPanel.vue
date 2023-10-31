<script lang="ts" setup>
import { ref, computed, watch, onMounted } from "vue";

import { useProjectDataStore } from "@/stores/projectData";
import * as lambda from "@/apis/lambda";
import PulseLoaderVue from "./spinners/PulseLoader.vue";
import {
  Drawer,
  Form,
  Button,
  Space,
  FormItem,
  Textarea,
  Row,
  Col,
  Divider,
  message,
  notification,
} from "ant-design-vue";
import { CheckOutlined } from "@ant-design/icons-vue";
import { useOpenAIStore } from "@/stores/open-ai.store";
import { getAnalytics, logEvent } from "firebase/analytics";
import { useProjectStore } from "@/stores/projects";

const emit = defineEmits<{
  (e: "isClosed"): void;
  (e: "saved", data: string): string;
}>();

const props = defineProps<{
  module?: string;
  questionId?: number;
  ai?: {
    defaultValue?: string;
    prompt: string;
    context: string;
    format: string;
  };
  isVisible: boolean;
}>();

const projectStore = useProjectDataStore();
const store = useOpenAIStore();

const gptResponse = ref({
  answer: null,
  error: null,
  id: null as number,
});
const formInput = ref("");
const config = ref({
  visible: props.isVisible,
});

const moduleQuestion = computed(() => {
  return projectStore
    .questionsForTopic(props.module)
    .find((i) => i.id == props.questionId);
});

function parseAIResponse(resp: { id: number; error?: string; result?: string }) {
  if (resp == null) return null;

  if (resp.error != null) {
    return notification.error({
      message: "Error",
      description: resp.error,
    });
  }

  const { id, result } = resp;
  gptResponse.value = { id, answer: result, error: null };
}

// FIXME: Rewrite submitContextAndPrompt function with more clarity
async function submitContextAndPrompt(refresh: boolean = false) {
  if (refresh && gptResponse.value.id != null) {
    store.trackUsage(gptResponse.value.id, "rejected");
  }

  store.loading = true;

  const { questionId: id } = props;

  gptResponse.value = { answer: "", id: null, error: null };

  if (props.ai == null) {
    let context = "";
    let qToFill = null;
    for (var q of projectStore.questions) {
      const a = projectStore.getData(q.id);
      if (q.id == id) {
        qToFill = q;
      } else if (!(a == null || a == "")) {
        context += q.label + ":" + a + "\n";
      }
    }

    parseAIResponse(await store.gptCompletion(qToFill.q2ai, context, qToFill.f4ai));
  } else {
    parseAIResponse(
      await store.gptCompletion(props.ai.prompt, props.ai.context, props.ai.format)
    );
  }

  // gptResponse.value.answer = ai_answer;
  // gptResponse.value.isLoading = false;
}

const closeDrawer = () => {
  gptResponse.value.answer = null;
  formInput.value = "";

  emit("isClosed");
};

const saveAndClose = () => {
  // if (props.ai == null) {
  //   projectStore.setData(props.questionId, formInput.value);
  // }
  emit("saved", formInput.value);
  closeDrawer();
};

watch(
  props,
  (newProps) => {
    config.value.visible = newProps.isVisible;

    if (newProps.isVisible) {
      gptResponse.value.answer = null;

      if (newProps.ai == null) {
        formInput.value = projectStore.getData(newProps.questionId);
      } else {
        formInput.value = newProps.ai.defaultValue;
      }

      submitContextAndPrompt();

      logEvent(getAnalytics(), "activity_performed", {
        project_name: useProjectStore().projectName,
        activity_name: "ai_suggestion_panel_open",
      });
    }
  },
  { deep: true }
);

function acceptSuggestion() {
  const answer = gptResponse.value.answer;
  if ((answer || "").length == 0) {
    return;
  }
  formInput.value = formInput.value + "\n\n" + answer;

  notification.info({ message: "Suggestion has been added to the text box" });

  logEvent(getAnalytics(), "activity_performed", {
    project_name: useProjectStore().projectName,
    activity_name: "ai_suggestion_accepted",
  });
  store.trackUsage(gptResponse.value.id, "accepted");
}
</script>

<template>
  <!-- TODO: change to ant drawer -->
  <Drawer
    v-model:open="config.visible"
    :mask-closable="false"
    width="80vw"
    @close="closeDrawer"
  >
    <!-- <div class="level">
      <div class="level-left"></div>
      <div class="level-right mt-2 mr-4"> -->

    <template #extra>
      <Space>
        <Button type="primary" @click="saveAndClose()"> Save and Close </Button>

        <Button @click="closeDrawer"> Cancel </Button>
      </Space>
    </template>
    <!--
      </div>
    </div> -->

    <Row>
      <div class="mt-2">
        <!-- Display loading indicator -->
        <div v-if="store.loading == true">
          <PulseLoaderVue :loading="store.loading"></PulseLoaderVue>

          <span>Getting AI suggestions, please wait...</span>
        </div>

        <div v-else>
          <p v-if="gptResponse.error != null" style="color: red">
            {{ gptResponse.error }}
          </p>
          <p v-else style="white-space: pre-wrap">
            {{
              gptResponse?.answer ||
              "No suggestions available. Click on the refresh button to get new suggestions"
            }}
          </p>
        </div>

        <div class="field is-grouped mt-3">
          <div class="control">
            <!-- FIXME: hide this button if chatgpt throws error -->
            <Button
              type="primary"
              @click="acceptSuggestion()"
              :class="{
                disabled: store.loading || gptResponse?.answer == undefined,
              }"
              :disabled="store.loading || gptResponse?.answer == undefined"
            >
              <CheckOutlined />

              Accept
            </Button>
          </div>

          <div class="control">
            <Button
              @click="submitContextAndPrompt(true)"
              :class="{ 'is-loading disabled': store.loading }"
              :disabled="store.loading"
            >
              Refresh
            </Button>
          </div>
        </div>
      </div>
    </Row>

    <Row>
      <Col :span="24" style="margin-top: 50px">
        <Form layout="vertical">
          <FormItem :label="moduleQuestion?.q2u">
            <Textarea v-model:value="formInput" :rows="23" :cols="10"></Textarea>
          </FormItem>
        </Form>
      </Col>
    </Row>
  </Drawer>
</template>
