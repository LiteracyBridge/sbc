<script setup>
import { ref, reactive, onMounted, onBeforeUnmount } from "vue";
import { onClickOutside } from "@vueuse/core";
import { useLookupStore } from "../stores/lookups";
import { useProjectStore } from "../stores/projects";
import { useMessageStore } from "../stores/messages";
const projectStore = useProjectStore();
const messages = reactive(useMessageStore().messages);
const componentKey = ref(0);
await useMessageStore().getLatestMessages(props.topic, messages);

const props = defineProps({
  topic: {
    type: String,
    required: true,
  },
  modelValue: {
    type: Boolean,
    required: true,
  },
});

onMounted(() => {
  console.log(`the component is now mounted.`);
  window.addEventListener("keydown", onEscapeKey);
});

onBeforeUnmount(() => {
  window.removeEventListener("keydown", onEscapeKey);
});

// async function onBeforeMount() {
//   await messageStore.getLatestMessages(props.topic);
// }

const emit = defineEmits(["update:modelValue", "save"]);

const closeButton = () => {
  emit("update:modelValue", false);
};

async function refreshButton() {
  await useMessageStore().getLatestMessages(props.topic, messages);
  componentKey.value += 1;
}

function onEscapeKey(event) {
  if (event.keyCode === 27) {
    // do something when escape key is pressed
    console.log("Escape key pressed");
    closeButton();
  }
}

const modalRef = ref(null);
const child = ref(false);

onClickOutside(modalRef, closeButton);
</script>

<template>
  <div class="modal is-active p-2" @keydown.esc="closeModalLogin" tabindex="0">
    <div class="modal-background"></div>
    <div ref="modalRef" class="modal-card">
      <header class="modal-card-head">
        <p class="modal-card-title">Message Browser</p>
        <button @click="closeButton" class="delete" aria-label="close"></button>
      </header>
      <section class="modal-card-body" :key="componentKey">
        <div v-for="(message,dx) in messages[topic]" :key="message.id">
          <u>
            <i>
              {{ projectStore.userById(message.user_id).address_as }},
              {{ message.time.substring(0, 19).replace(" ", " at ") }}
            </i>
          </u>
          <br />
          <div class="text-with-line-breaks" v-text="message.message"/>
          <br />
          <b v-if="message.replies.length != 0">Replies:</b>
          <div class="ml-4" v-for="reply in message.replies" :key="reply.id">
            <u>
              {{ projectStore.userById(reply.user_id).address_as }},
              {{ reply.time.substring(0, 19).replace(" ", " at ") }}
            </u>
            <br />
            {{ reply.message }}
          </div>
          <br />
          <br />
          <br />
        </div>
      </section>
      <footer class="modal-card-foot is-justify-content-flex-end">
        <button @click="closeButton" class="button">Close</button>
        <button @click="refreshButton" class="button">Refresh</button>
      </footer>
    </div>
  </div>
</template>

<style>
.text-with-line-breaks {
  white-space: pre-line;
}
</style>