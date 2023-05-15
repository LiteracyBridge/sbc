<script setup>
import { ref, reactive, onMounted, onBeforeUnmount, computed } from "vue";
import { onClickOutside } from "@vueuse/core";
import { useLookupStore } from "../stores/lookups";
import { useProjectStore } from "../stores/projects";
import { useMessageStore } from "../stores/messages";

const projectStore = useProjectStore();
// const messages = reactive(useMessageStore().messages);
const componentKey = ref(0);
// await useMessageStore().getLatestMessages(props.topic, messages);

const emit = defineEmits(['isClosed']);

const props = defineProps({
  // topic: {
  //   type: String,
  //   required: true,
  // },
  // modelValue: {
  //   type: Boolean,
  //   required: true,
  // },
  isVisible: {
    type: Boolean,
    required: true,
  }
});

const isOpened = ref(props.isVisible);

console.log(isOpened.value, props.isVisible)
// onMounted(() => {
//   isOpened.value = props.isVisible;
//   // console.log(`the component is now mounted.`);
//   // window.addEventListener("keydown", onEscapeKey);
// });

// onBeforeUnmount(() => {
//   window.removeEventListener("keydown", onEscapeKey);
// });

// // async function onBeforeMount() {
// //   await messageStore.getLatestMessages(props.topic);
// // }

// const emit = defineEmits(["update:modelValue", "save"]);
const normalizedSize = computed(() => props.isVisible)

const closeButton = () => {
  isOpened.value = false;

  console.error("emitted")
  emit("isClosed", true);
};

// async function refreshButton() {
//   await useMessageStore().getLatestMessages(props.topic, messages);
//   componentKey.value += 1;
// }

// function onEscapeKey(event) {
//   if (event.keyCode === 27) {
//     // do something when escape key is pressed
//     console.log("Escape key pressed");
//     closeButton();
//   }
// }

// const modalRef = ref(null);
// const child = ref(false);

// onClickOutside(modalRef, closeButton);
</script>

<template>
  <VueSidePanel v-model="normalizedSize" :hide-close-btn="true" :no-close="true" lock-scroll width="100vw"
    transition-name="slide-right">
    <div style="padding-top: 70px; color: #f14668">
      <h2 v-for="item in 50" :key="item"
        :style="{ fontSize: '58px', fontWeight: 700, opacity: item * 2 / 100, lineHeight: '43px' }">
        This is scrolled body!
      </h2>

      <button @click.prevent="closeButton" class="button is-primary">Close</button>
    </div>

  </VueSidePanel>
</template>

<style>
.text-with-line-breaks {
  white-space: pre-line;
}
</style>
