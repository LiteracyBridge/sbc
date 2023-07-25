<script setup lang="ts">
import { onMounted, ref } from "vue";
import { useUserStore } from "@/stores/user";
import { useProjectDataStore } from "@/stores/projectData";
import { useRouter } from "vue-router";
import GPTSuggestionPanel from "./GPTSuggestionPanel.vue";
import BroadcastComponent from "./BroadcastComponent.vue";

const userStore = useUserStore();
const projectDataStore = useProjectDataStore();
const suggestionsPanelHandler = ref({ questionId: null, isOpened: false, module: null });

// GPT prompt
const context = ref("Respond only with a list and without any other text.");
const iconRefs = ref([]);
const BULB_ICON = "/images/lightbulb.png";

const props = defineProps({
  topic: {
    type: String,
    required: true,
  },
});

const qAndAs = ref([
  {
    topic: "intro",
    id: 1,
    bulb: false,
    q: "What is the name of your SBC Program?",
    label: "Program Name",
    a: "Women's Land Rights",
  },
  {
    topic: "intro",
    id: 2,
    bulb: false,
    q:
      "Where is the geographic area for your SBC program activities? (e.g. Jirapa District, Ghana)",
    label: "Location",
    a: "West Nile Sub-Region, Uganda",
  },
  {
    topic: "intro",
    id: 3,
    bulb: false,
    q:
      "Who is the primary audience for your program? (e.g. new mothers, soybean farmers, adolescent girls)",
    label: "Primary Audience",
    a: "Women farmers in rural communities",
  },
  {
    topic: "intro",
    id: 4,
    bulb: false,
    q: "What desired behavior is difficult to complete and what is the reason?",
    label: "Behavior Challenge",
    a: "",
  },
  {
    topic: "intro",
    id: 5,
    bulb: true,
    q: "What challenging social issue do people face and why?",
    label: "Social Challenge",
    a: "",
  },
  {
    topic: "intro",
    id: 7,
    bulb: true,
    q:
      "What is the high-level objective of your SBC program? (e.g. reduce malaria, encourage family planning, shift views on women’s land rights)",
    label: "Program Objective",
    a: "",
  },
  {
    topic: "toc",
    id: 1,
    bulb: true,
    q: "Propose some outcomes for this program",
    label: "Program Outcomes",
    a: "",
  },
  {
    topic: "toc",
    id: 2,
    bulb: true,
    q: "Propose some outputs for this program",
    label: "Program Outputs",
    a: "",
  },
  {
    topic: "toc",
    id: 3,
    bulb: true,
    q: "Propose some activities for this program",
    label: "Program Activities",
    a: "",
  },
  {
    topic: "toc",
    id: 4,
    bulb: true,
    q: "Propose some inputs for this program",
    label: "Program Inputs",
    a: "",
  },
]);

const answers = ref(projectDataStore.project_data);

function updateData(event: any, id: number) {
  console.log("EVENT:", event.target.value);
  projectDataStore.setData(id, event.target.value);
}

onMounted(() => {
  userStore.loggedIn ? null : useRouter().push({ path: "/login" });
  console.log("topic:" + props.topic);
});

function showPanel(id: number, topic: string, loadSuggestions = true) {
  suggestionsPanelHandler.value.questionId = id;
  suggestionsPanelHandler.value.module = topic;
  suggestionsPanelHandler.value.isOpened = true;
}

async function submitContextAndPrompt(id: number, topic: string) {
  showPanel(id, topic);
  return;
}
</script>

<template>
  <div>
    <BroadcastComponent :module="topic"></BroadcastComponent>

    <GPTSuggestionPanel
      :is-visible="suggestionsPanelHandler.isOpened"
      @is-closed="suggestionsPanelHandler.isOpened = false"
      :question-id="suggestionsPanelHandler.questionId"
      :module="suggestionsPanelHandler.module"
    >
    </GPTSuggestionPanel>

    <div
      v-for="(q, count) in projectDataStore.questionsForTopic(topic)"
      :key="q.id"
      class="columns mx-4 is-vcentered"
    >
      <div class="column is-8">
        <!-- <strong>{{ count + 1 }}. {{ q.q2u }} </strong><br />
        <img v-if="q.bulb" :src="BULB_ICON" ref="iconRefs" @click="submitContextAndPrompt(q.id, topic)"
          class="image is-32x32" />
        <textarea @change="updateData($event, q.id)" :value="projectDataStore.getData(q.id)" rows="4" cols="80" /><br />
        <br /><br /> -->

        <div class="field">
          <label class="label" :for="`input-${count + 1}`"
            >{{ count + 1 }}. {{ q.q2u }}</label
          >

          <div class="control">
            <img
              v-if="q.bulb"
              :src="BULB_ICON"
              ref="iconRefs"
              @click="submitContextAndPrompt(q.id, topic)"
              class="image is-32x32"
            />
          </div>

          <div class="control">
            <textarea
              class="textarea"
              @change="updateData($event, q.id)"
              :value="projectDataStore.getData(q.id)"
              rows="7"
              cols="80"
            ></textarea>
          </div>
        </div>
      </div>
    </div>

    <hr />
  </div>
</template>

<style>
.vertical-center {
  margin: 2rem;
}
</style>
