<script lang="ts" setup>
import { ref, reactive, onMounted, onBeforeUnmount, computed, watch } from "vue";

import { useProjectDataStore } from "@/stores/projectData";
import * as lambda from "@/apis/lambda";
import PulseLoaderVue from "./spinners/PulseLoader.vue";
import { Drawer, Button, Space } from "ant-design-vue";

const emit = defineEmits(['isClosed']);


const props = defineProps({
  module: {
    type: String,
    required: true,
  },
  questionId: {
    type: Number,
    required: false,
  },
  isVisible: {
    type: Boolean,
    required: true,
  }
});

const projectStore = useProjectDataStore();

const gptResponse = ref({ answer: null, isLoading: false });
const formInput = ref("");
const config = ref({
  visible: props.isVisible
})

const moduleQuestion = computed(() => {
  return projectStore.questionsForTopic(props.module).find(i => i.id == props.questionId);
})

// FIXME: Rewrite submitContextAndPrompt function with more clarity
async function submitContextAndPrompt() {
  const { questionId: id } = props;

  const _gptResp = gptResponse.value || { id: id, answer: "", isLoading: true };
  _gptResp.isLoading = true;
  gptResponse.value = _gptResp;


  let context = "";
  let qToFill = null;
  for (var q of projectStore.questions) {
    const a = projectStore.getData(q.id);
    if (q.id == id) {
      qToFill = q
    }
    else if (!(a == null || a == "")) {
      context += q.label + ":" + a + "\n";
    }
  }

  const ai_answer = await lambda.gptCompletion(qToFill.q2ai, context, qToFill.f4ai);

  gptResponse.value.answer = ai_answer;
  gptResponse.value.isLoading = false;
}

const closeButton = () => {
  gptResponse.value.answer = null;
  formInput.value = "";

  emit("isClosed", true);
};

watch(props, (newProps) => {
  config.value.visible = newProps.isVisible;

  submitContextAndPrompt();

  formInput.value = projectStore.getData(newProps.questionId);
  gptResponse.value.answer = null;
}, { deep: true });


function onInputChange(event: any) {
  formInput.value = event.target.value;
}

</script>

<template>
  <!-- TODO: change to ant drawer -->
  <Drawer :visible="config.visible" :mask-closable="false" width="80vw" transition-name="slide-right" @close="closeButton">
    <!-- <div class="level">
      <div class="level-left"></div>
      <div class="level-right mt-2 mr-4"> -->

    <template #extra>
      <Space>

        <Button type="primary" @click="projectStore.setData(props.questionId, formInput); closeButton()">
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

    <div class="columns my-3 mx-5">


      <div class="column is-4 mt-2">
        <div class="mt-2">
          <!-- Display loading indicator -->
          <div v-if="gptResponse?.isLoading == true">
            <PulseLoaderVue :loading="gptResponse?.isLoading"></PulseLoaderVue>

            <span>Getting AI suggestions, please wait...</span>
          </div>

          <p v-else style="white-space: pre-wrap">
            {{ gptResponse?.answer || 'No suggestions available. Click on the light bulb to see suggestions' }}
          </p>

          <div class="field is-grouped mt-3">
            <div class="control">
              <!-- FIXME: hide this button if chatgpt throws error -->
              <Button type="primary" @click="formInput = formInput + '\n\n' + gptResponse?.answer;"
                :class="{ 'disabled': gptResponse.isLoading || gptResponse?.answer == undefined }"
                :disabled="gptResponse.isLoading || gptResponse?.answer == undefined">
                <span class="icon is-small mr-1">
                  <i class="fas fa-check"></i>
                </span>

                Accept
              </Button>
            </div>

            <div class="control">
              <Button @click="submitContextAndPrompt()" :class="{ 'is-loading disabled': gptResponse.isLoading }"
                :disabled="gptResponse.isLoading">
                Refresh
              </Button>
            </div>
          </div>
        </div>
      </div>

      <div class="column">
        <div class="field">
          <label class="label" :for="`input`">{{ moduleQuestion?.q2u }}</label>

          <div class="control">
            <textarea class="textarea" @change="onInputChange($event)" :value="formInput" rows="15" cols="10"></textarea>
          </div>
        </div>
      </div>

    </div>

  </Drawer>
</template>
