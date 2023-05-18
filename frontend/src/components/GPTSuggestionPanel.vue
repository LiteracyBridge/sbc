<script lang="ts" setup>
import { ref, reactive, onMounted, onBeforeUnmount, computed } from "vue";
import { Multiselect } from 'vue-multiselect'
import { AccordionList, AccordionItem } from "vue3-rich-accordion";

import { useProjectStore } from "../stores/projects";
import { INDICATORS, INDICATOR_TYPES } from "../constants/indicators";
import type { IIndicatorType } from '../constants/indicators'
import { useProjectDataStore } from "@/stores/projectData";

const projectStore = useProjectDataStore();

const emit = defineEmits(['isClosed']);

const props = defineProps({
  module: {
    type: String,
    required: true,
  },
  questionId: {
    type: Number,
    required: true,
  },
  // modelValue: {
  //   type: Boolean,
  //   required: true,
  // },
  isVisible: {
    type: Boolean,
    required: true,
  }
});

const moduleQuestion = computed(() => {
  return projectStore.questionsForTopic(props.module).find(i => i.id == props.questionId);
})

const selectedIndicatorType = ref<{ id: number, name: string }>();
const selectedGroup = ref<IIndicatorType>();

const isOpened = computed(() => props.isVisible)

const selectedIndicatorGroups = computed(() => {
  if (selectedIndicatorType?.value == null) {
    return [];
  }

  return INDICATOR_TYPES.filter(i => i.parentId == selectedIndicatorType.value.id);
});

const getMainIndicators = computed(() => {
  return INDICATOR_TYPES.filter(i => i.parentId == null);
});

const groupIndicators = computed(() => {
  if (selectedGroup.value?.id == null) {
    return [];
  }

  return INDICATORS.filter(i => i.groupId == selectedGroup.value?.id);
})

function onIndicatorSelected(item: any, _: any) {
  console.log(item)
}

const closeButton = () => {
  // isOpened.value = false;

  console.error("emitted")
  emit("isClosed", true);
};

onMounted(() => {
  selectedGroup.value = getMainIndicators.value[0];
})

function onInputChange(event: any) {
  console.log("EVENT:", event.target.value);
  projectStore.setData(props.questionId, event.target.value);
}

</script>

<template>
  <VueSidePanel v-model="isOpened" :hide-close-btn="false" :no-close="true" lock-scroll width="100vw"
    transition-name="slide-right">

    <div class="columns my-5 mx-5">

      <div class="column">

        <!-- <strong>{{ count + 1 }}. {{ q.q2u }} </strong><br />
  <img v-if="q.bulb" :src="BULB_ICON" ref="iconRefs" @click="submitContextAndPrompt(q.id, topic)"
    class="image is-32x32" />
  <textarea @change="updateData($event, q.id)" :value="projectDataStore.getData(q.id)" rows="4" cols="80" /><br />
  <br /><br /> -->

        <div class="field">
          <label class="label" :for="`input`">{{ moduleQuestion?.q2u }}</label>

          <!-- <div class="control">
            <img v-if="q.bulb" :src="BULB_ICON" ref="iconRefs" @click="submitContextAndPrompt(q.id, topic)"
              class="image is-32x32" />
          </div> -->
          <div class="control">
            <!-- <img v-if="q.bulb" :src="BULB_ICON" ref="iconRefs" @click="submitContextAndPrompt(q.id, topic)"
        class="image is-32x32" /> -->
            <textarea class="textarea" @change="onInputChange($event)" :value="projectStore.getData(moduleQuestion?.id)"
              rows="30" cols="10"></textarea>
            <!-- <input class="input" type="text" placeholder="e.g Alex Smith"> -->
          </div>

        </div>
      </div>

      <div class="column  is-4">
        <!-- <p>{{ gptResponses.find(i => i.id == q.id)?.answer || '' }}</p> -->

        <!-- Display loading indicator -->
        <!-- TODO: implement displaying of suggestions -->
        <!-- <div v-if="gptResponses[`${q.id}`]?.isLoading == true">
          <PulseLoaderVue :loading="gptResponses[`${q.id}`]?.isLoading"></PulseLoaderVue>

          <span>Getting AI suggestions, please wait...</span>
        </div>

        <p v-else>
          {{ gptResponses[`${q.id}`]?.answer || 'No suggestions available. Click on the light bulb to see suggestions' }}
        </p> -->

        <!-- <div class="field is-grouped mt-3"
          v-if="gptResponses[`${q.id}`]?.answer != undefined && gptResponses[`${q.id}`]?.isLoading != true">
          <p class="control">
            <button class="button is-small is-dark"
              @click="projectDataStore.setData(q.id, projectDataStore.getData(q.id) + '\n\n' + gptResponses[`${q.id}`]?.answer);">

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
        </div> -->

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
