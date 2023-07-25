<script lang="ts" setup>
import { ref, computed, watch } from "vue";

import { useProjectDataStore } from "@/stores/projectData";
import * as lambda from "@/apis/lambda";
import PulseLoaderVue from "./spinners/PulseLoader.vue";
import { Drawer, Form, Button, Space, FormItem, Textarea, Row, Col } from "ant-design-vue";
import { CheckOutlined } from "@ant-design/icons-vue";

const emit = defineEmits<{
  (e: "isClosed"): void;
  (e: "saved", data: string): string;
}>();

const props = defineProps<{
  module?: string;
  questionId?: number;
  ai?: {
    prompt: string;
    context: string;
    format: string;
  };
  isVisible: boolean;
}>();

const projectStore = useProjectDataStore();

const gptResponse = ref({ answer: null, isLoading: false });
const formInput = ref("");
const config = ref({
  visible: props.isVisible,
});

const moduleQuestion = computed(() => {
  return projectStore
    .questionsForTopic(props.module)
    .find((i) => i.id == props.questionId);
});

// FIXME: Rewrite submitContextAndPrompt function with more clarity
async function submitContextAndPrompt() {
  const { questionId: id } = props;

  const _gptResp = gptResponse.value || { id: id, answer: "", isLoading: true };
  _gptResp.isLoading = true;
  gptResponse.value = _gptResp;

  let ai_answer = null;
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

    ai_answer = await lambda.gptCompletion(qToFill.q2ai, context, qToFill.f4ai);
  } else {
    ai_answer = await lambda.gptCompletion(
      props.ai.prompt,
      props.ai.context,
      props.ai.format
    );
  }

  gptResponse.value.answer = ai_answer;
  gptResponse.value.isLoading = false;
}

const closeButton = () => {
  gptResponse.value.answer = null;
  formInput.value = "";

  emit("isClosed");
};

watch(
  props,
  (newProps) => {
    config.value.visible = newProps.isVisible;
    gptResponse.value.answer = null;

    submitContextAndPrompt();

    if (newProps.ai == null) {
      formInput.value = projectStore.getData(newProps.questionId);
    }
  },
  { deep: true }
);

function onInputChange(event: any) {
  formInput.value = event.target.value;
}
</script>

<template>
  <!-- TODO: change to ant drawer -->
  <Drawer
    v-model:open="config.visible"
    :mask-closable="false"
    width="80vw"
    @close="closeButton"
  >
    <!-- <div class="level">
      <div class="level-left"></div>
      <div class="level-right mt-2 mr-4"> -->

    <template #extra>
      <Space>
        <Button
          type="primary"
          @click="
            projectStore.setData(props.questionId, formInput);
            closeButton();
          "
        >
          <!-- <span class="icon mr-1">
                <i class="fas fa-save"></i>
              </span> -->

          Save and Close
        </Button>

        <Button @click="closeButton">
          <!-- <span class="icon mr-1">
                <i class="fas fa-times"></i>
              </span> -->
          Cancel
        </Button>
      </Space>
    </template>
    <!--
      </div>
    </div> -->

    <Row :gutter="8">
      <Col :span="10">
        <div class="mt-2">
          <!-- Display loading indicator -->
          <div v-if="gptResponse?.isLoading == true">
            <PulseLoaderVue :loading="gptResponse?.isLoading"></PulseLoaderVue>

            <span>Getting AI suggestions, please wait...</span>
          </div>

          <p v-else style="white-space: pre-wrap">
            {{
              gptResponse?.answer ||
              "No suggestions available. Click on the light bulb to see suggestions"
            }}
          </p>

          <div class="field is-grouped mt-3">
            <div class="control">
              <!-- FIXME: hide this button if chatgpt throws error -->
              <Button
                type="primary"
                @click="formInput = formInput + '\n\n' + gptResponse?.answer"
                :class="{
                  disabled: gptResponse.isLoading || gptResponse?.answer == undefined,
                }"
                :disabled="gptResponse.isLoading || gptResponse?.answer == undefined"
              >
                <CheckOutlined />

                Accept
              </Button>
            </div>

            <div class="control">
              <Button
                @click="submitContextAndPrompt()"
                :class="{ 'is-loading disabled': gptResponse.isLoading }"
                :disabled="gptResponse.isLoading"
              >
                Refresh
              </Button>
            </div>
          </div>
        </div>
      </Col>

      <Col :span="14">
        <Form layout="vertical">
          <FormItem :label="moduleQuestion?.q2u">
            <Textarea v-model:value="formInput" rows="15" cols="10"></Textarea>
          </FormItem>
        </Form>
      </Col>
    </Row>
  </Drawer>
</template>
