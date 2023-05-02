<script setup>
import { onMounted, ref } from "vue";
import { useUserStore } from "@/stores/user";
import { useProjectDataStore } from '@/stores/projectData'
import { useRouter } from "vue-router";
import * as lambda from "@/apis/lambda";
import MessageModal from '../components/MessageModal.vue';

const showMessageModal = ref(false);
const userStore = useUserStore();
const projectDataStore = useProjectDataStore();

// GPT prompt
const context = ref("Respond only with a list and without any other text.");
const format = ref("");
const prompt = ref("");
const start = ref("1.");
const stop = ref("");

const iconRefs = ref([]);
const promptResp = ref("");
const BULB_ICON = "/images/lightbulb.png"
const HOURGLASS_ICON = "/images/hourglass.svg"
const bulbIcon = ref(BULB_ICON);
const projectData = ref(projectDataStore.project_data);

const props = defineProps({
  topic: {
    type: String,
    required: true
  }
})


const qAndAs = ref([
  {"topic":"intro","id":1,"bulb":false,"q":"What is the name of your SBC Program?","label":"Program Name","a":"Women's Land Rights"},
  {"topic":"intro","id":2,"bulb":false,"q":"Where is the geographic area for your SBC program activities? (e.g. Jirapa District, Ghana)","label":"Location","a":"West Nile Sub-Region, Uganda"},
  {"topic":"intro","id":3,"bulb":false,"q":"Who is the primary audience for your program? (e.g. new mothers, soybean farmers, adolescent girls)","label":"Primary Audience","a":"Women farmers in rural communities"},
  {"topic":"intro","id":4,"bulb":false,"q":"What desired behavior is difficult to complete and what is the reason?","label":"Behavior Challenge","a":""},
  {"topic":"intro","id":5,"bulb":true,"q":"What challenging social issue do people face and why?","label":"Social Challenge","a":""},
  {"topic":"intro","id":7,"bulb":true,"q":"What is the high-level objective of your SBC program? (e.g. reduce malaria, encourage family planning, shift views on women’s land rights)","label":"Program Objective","a":""},
  {"topic":"toc","id":1,"bulb":true,"q":"Propose some outcomes for this program","label":"Program Outcomes","a":""},
  {"topic":"toc","id":2,"bulb":true,"q":"Propose some outputs for this program","label":"Program Outputs","a":""},
  {"topic":"toc","id":3,"bulb":true,"q":"Propose some activities for this program","label":"Program Activities","a":""},
  {"topic":"toc","id":4,"bulb":true,"q":"Propose some inputs for this program","label":"Program Inputs","a":""}
])

const answers = ref(projectDataStore.project_data);

function updateData(event, id) {
  console.log("EVENT:",event.target.value);
  projectDataStore.setData(id, event.target.value);
}

onMounted(() => {
  userStore.loggedIn ? null : useRouter().push({ path: "/login" });
  console.log("topic:"+props.topic);
}
);

async function submitContextAndPrompt(id,topic) {
  let context = "";
  let qToFill = null;
  for (var q of projectDataStore.questions) {
    const a = projectDataStore.getData(q.id);
    if (q.id == id)
      qToFill = q
    else if (!(a === null || a == ""))
      context += q.label + ":" + a + "\n";
  }
  console.log("submitContextAndPrompt:");
  // console.log(qToFill.q2ai, context, qToFill.f4ai);
  const bulbCount = projectDataStore.countBulbs(id,topic);
  console.log("bulbCount",bulbCount);
  iconRefs.value[bulbCount-1].src = HOURGLASS_ICON;
  // this.$refs[`icon-${id}`].src = HOURGLASS_ICON;
  const ai_answer = await lambda.gptCompletion(qToFill.q2ai, context, qToFill.f4ai);
  iconRefs.value[bulbCount-1].src = BULB_ICON;
  projectDataStore.setData(qToFill.id,ai_answer);
}

async function submitPrompt() {
  promptResp.value = '';
  promptResp.value = await lambda.gptCompletion(prompt.value,context.value,format.value,start.value,stop.value);
}

async function openMessageModal() {
  showMessageModal.value = true;
}

async function broadcastPage() {
  let message = "";
  for (var q of projectDataStore.questionsForTopic(props.topic)) {
    const a = projectDataStore.getData(q.id);
    if (a != "")
      message += q.label + "\n" + a + "\n\n";
  }
  console.log("Message: "+message);
  lambda.twilioBroadcast(message,props.topic)
}

</script>

<template>
  <div>
    <div class="buttons-container is-fixed is-absolute is-flex is-flex-direction-column is-align-items-flex-end m-4 mr-6">
      <button class="button is-link mb-2" :disabled="showMessageModal" @click.prevent="broadcastPage">
        <span>Broadcast</span>
      </button>
      <button class="button is-link" :disabled="showMessageModal" @click.prevent="showMessageModal = true">
        <span>Messages</span>
      </button>
    </div>
    <Suspense>
      <MessageModal v-if="showMessageModal" :topic="topic" v-model="showMessageModal"/>
    </Suspense>
    <br/>
    <div v-for="(q,count) in projectDataStore.questionsForTopic(topic)" :key="q.id">
      <strong>{{count+1}}. {{ q.q2u }} </strong><br/>
      <img v-if="q.bulb" :src="BULB_ICON" ref="iconRefs" @click="submitContextAndPrompt(q.id,topic)" class="image is-32x32"/>
      <textarea @change="updateData($event, q.id)" :value="projectDataStore.getData(q.id)" rows="4" cols="80"/><br/>
      <br/><br/>
    </div>   
    <hr/>
  </div>
</template>


<style>
.vertical-center {
  margin: 2rem;
}
</style>
