<script setup lang="ts">

import { ref, reactive, onMounted, onBeforeUnmount, watch } from "vue";
import { onClickOutside } from "@vueuse/core";
import { useProjectStore } from "../stores/projects";
import { useMessageStore } from "../stores/messages";
import { Button, Modal, Space } from "ant-design-vue";

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

const visible = ref(props.modelValue);
const projectStore = useProjectStore();
const messages = reactive(useMessageStore().messages);
const componentKey = ref(0);
await useMessageStore().getLatestMessages(props.topic, messages);


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

const emit = defineEmits(["closed", "save"]);

const closeButton = () => {
  visible.value = false;
  emit("closed", false);
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

watch(props, (newProps) => {
  visible.value = newProps.modelValue;
})
// const modalRef = ref(null);

// onClickOutside(modalRef, closeButton);
</script>

<template>
  <Modal :visible="visible" @close="closeButton" @keydown.esc="closeButton" tabindex="0">
    <template #title>
      Message Browser
    </template>


    <template #footer>
      <Space>
        <Button @click="closeButton">Close</Button>
        <Button @click="refreshButton" type="primary" :ghost="true">Refresh</Button>
      </Space>
    </template>

    <!-- <div class="modal-background"></div>
    <div ref="modalRef" class="modal-card"> -->
    <!-- <header class="modal-card-head">
        <p class="modal-card-title">Message Browser</p>
        <button @click="closeButton" class="delete" aria-label="close"></button>
      </header> -->

    <section class="modal-card-body" :key="componentKey">
      <div v-for="(message, dx) in messages[topic]" :key="message.id">
        <u>
          <i>
            {{ projectStore.userById(message.user_id).address_as }},
            {{ message.time.substring(0, 19).replace(" ", " at ") }}
          </i>
        </u>
        <br />
        <div class="text-with-line-breaks" v-text="message.message" />
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

    <!-- </div> -->
  </Modal>
</template>

<style>
.text-with-line-breaks {
  white-space: pre-line;
}
</style>
