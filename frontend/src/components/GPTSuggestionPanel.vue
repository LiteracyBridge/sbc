<script lang="ts" setup>
import { ref, reactive, onMounted, onBeforeUnmount, computed } from "vue";

import { useProjectDataStore } from "@/stores/projectData";
import * as lambda from "@/apis/lambda";
import PulseLoaderVue from "./spinners/PulseLoader.vue";


const projectStore = useProjectDataStore();
const emit = defineEmits(['isClosed']);

const gptResponse = ref({ answer: null, isLoading: false });
const iconRefs = ref();

const HOURGLASS_ICON = "/images/hourglass.svg"
const BULB_ICON = "/images/lightbulb.png"


const props = defineProps({
  module: {
    type: String,
    required: true,
  },
  questionId: {
    type: Number,
    required: true,
  },
  isVisible: {
    type: Boolean,
    required: true,
  }
});

const moduleQuestion = computed(() => {
  return projectStore.questionsForTopic(props.module).find(i => i.id == props.questionId);
})

async function submitContextAndPrompt() {
  const { questionId: id, module: topic } = props;

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

  console.log("submitContextAndPrompt:");
  // console.log(qToFill.q2ai, context, qToFill.f4ai);
  // const bulbCount = projectStore.countBulbs(id, topic);
  // console.log("bulbCount", bulbCount);

  iconRefs.value.src = HOURGLASS_ICON;

  // this.$refs[`icon-${id}`].src = HOURGLASS_ICON;
  const ai_answer = await lambda.gptCompletion(qToFill.q2ai, context, qToFill.f4ai);
  iconRefs.value.src = BULB_ICON;

  console.error("AI answer", ai_answer)

  gptResponse.value.answer = ai_answer;
  gptResponse.value.isLoading = false;
  // gptResponses.value = gptResponses.value.concat({id: id, answer: ai_answer});
  // projectDataStore.setData(qToFill.id, ai_answer);
}

const isOpened = computed(() => props.isVisible)

// const selectedIndicatorGroups = computed(() => {
//   if (selectedIndicatorType?.value == null) {
//     return [];
//   }

//   return INDICATOR_TYPES.filter(i => i.parentId == selectedIndicatorType.value.id);
// });

// const getMainIndicators = computed(() => {
//   return INDICATOR_TYPES.filter(i => i.parentId == null);
// });

// const groupIndicators = computed(() => {
//   if (selectedGroup.value?.id == null) {
//     return [];
//   }

//   return INDICATORS.filter(i => i.groupId == selectedGroup.value?.id);
// })

function onIndicatorSelected(item: any, _: any) {
  console.log(item)
}

const closeButton = () => {
  // isOpened.value = false;

  console.error("emitted")
  emit("isClosed", true);
};

onMounted(() => {
  // selectedGroup.value = getMainIndicators.value[0];
})

function onInputChange(event: any) {
  console.log("EVENT:", event.target.value);
  projectStore.setData(props.questionId, event.target.value);
}

</script>

<template>
  <VueSidePanel v-model="isOpened" :hide-close-btn="true" :no-close="true" lock-scroll width="100vw"
    transition-name="slide-right">
    <div class="level">
      <div class="level-left"></div>
      <div class="level-right mt-2 mr-2">
        <button class="button is-close" @click.prevent="closeButton">
          <span class="icon mr-1">
            <i class="fas fa-times"></i>
          </span>
          Close
        </button>
      </div>
    </div>

    <div class="columns my-5 mx-5">

      <div class="column">

        <!-- <strong>{{ count + 1 }}. {{ q.q2u }} </strong><br />
        <img v-if="q.bulb" :src="BULB_ICON" ref="iconRefs" @click="submitContextAndPrompt()"
          class="image is-32x32" />
        <textarea @change="updateData($event, q.id)" :value="projectDataStore.getData(q.id)" rows="4" cols="80" /><br />
        <br /><br /> -->

        <div class="field">
          <label class="label" :for="`input`">{{ moduleQuestion?.q2u }}</label>

          <div class="control">
            <img v-if="moduleQuestion?.bulb" :src="BULB_ICON" ref="iconRefs" @click="submitContextAndPrompt()"
              class="image is-32x32" />
          </div>
          <div class="control">
            <!-- <img v-if="q.bulb" :src="BULB_ICON" ref="iconRefs" @click="submitContextAndPrompt(q.id, topic)"
        class="image is-32x32" /> -->
            <textarea class="textarea" @change="onInputChange($event)" :value="projectStore.getData(moduleQuestion?.id)"
              rows="30" cols="10"></textarea>
            <!-- <input class="input" type="text" placeholder="e.g Alex Smith"> -->
          </div>

        </div>
      </div>

      <div class="column is-4 mt-6">
        <!-- Display loading indicator -->
        <!-- TODO: implement displaying of suggestions -->
        <div class="mt-6">
          <div v-if="gptResponse?.isLoading == true">
            <PulseLoaderVue :loading="gptResponse?.isLoading"></PulseLoaderVue>

            <span>Getting AI suggestions, please wait...</span>
          </div>

          <p v-else>
            {{ gptResponse?.answer || 'No suggestions available. Click on the light bulb to see suggestions' }}
          </p>

          <div class="field is-grouped mt-3" v-if="gptResponse?.answer != undefined && gptResponse?.isLoading != true">
            <p class="control">
              <button class="button is-small is-dark"
                @click="projectStore.setData(props.questionId, projectStore.getData(props.questionId) + '\n\n' + gptResponse?.answer);">

                <span class="icon is-small mr-1">
                  <i class="fas fa-check"></i>
                </span>

                Accept
              </button>
            </p>

            <p class="control">
              <button class="button is-outlined is-small">
                Cancel
              </button>
            </p>
          </div>
        </div>

      </div>

    </div>

  </VueSidePanel>
</template>

<style>
textarea {
  width: 100%;
  -webkit-box-sizing: border-box;
  /* Safari/Chrome, other WebKit */
  -moz-box-sizing: border-box;
  /* Firefox, other Gecko */
  box-sizing: border-box;
  /* Opera/IE 8+ */
}
</style>
