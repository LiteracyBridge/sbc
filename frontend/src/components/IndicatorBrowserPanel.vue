<script lang="ts" setup>
import { ref, reactive, onMounted, onBeforeUnmount, computed } from "vue";
import { Multiselect } from 'vue-multiselect'
import { AccordionList, AccordionItem } from "vue3-rich-accordion";

import { onClickOutside } from "@vueuse/core";
import { useLookupStore } from "../stores/lookups";
import { useProjectStore } from "../stores/projects";
import { useMessageStore } from "../stores/messages";
import { INDICATORS, INDICATOR_TYPES } from "../constants/indicators";
import type { IIndicatorType } from '../constants/indicators'

const indicators = INDICATORS
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

// const isOpened = ref(props.isVisible);

// console.log(isOpened.value, props.isVisible)
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

const selectedIndicatorType = ref<{ id: number, name: string }>();
const selectedGroup = ref<IIndicatorType>();

const isOpened = computed(() => props.isVisible)

const selectedIndicatorGroups = computed(() => {
  if (selectedIndicatorType?.value == null) {
    return [];
  }

  return INDICATOR_TYPES.filter(i => i.parentId == selectedIndicatorType.value.id);

  // return [
  //   { label: "Indicator 1", value: 1 },
  //   { label: "Indicator 2", value: 2 },
  //   { label: "Indicator 3", value: 3 },
  //   { label: "Indicator 4", value: 4 },
  //   { label: "Indicator 5", value: 5 },
  // ]
  // return allUsers.value.map((user) => {
  //     return {
  //       value: user.email,
  //       label: user.name != '' ? `${user.name} (${user.email})` : user.email,
  //     };
  //   });
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

function onIndicatorSelected(item: any, _) {
  console.log(item)
  // const user = allUsers.value.find(user => user.email == item.value)

  // newUserEmail.value = user.email
  // newUserName.value = user.name ?? 'N/A'
  // newUserAddressAs.value = user.address_as
}

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
  <VueSidePanel v-model="isOpened" :hide-close-btn="true" :no-close="true" lock-scroll width="80vw"
    transition-name="slide-right">

    <div class="columns">
      <div class="column is-one-fifth mx-5 my-5">

        <!-- TODO: add label -->
        <Multiselect v-model="selectedIndicatorType" :options="getMainIndicators" :close-on-select="true"
          :clear-on-select="false" placeholder="Select user" label="name" track-by="value"
          @select="onIndicatorSelected" />
        <hr>

        <aside class="menu">
          <p class="menu-label">
            {{ selectedIndicatorType?.name || 'No indicatory type selected' }}
          </p>

          <ul class="menu-list">
            <li v-for="indicator in selectedIndicatorGroups" :key="indicator.id">
              <a @click.prevent="selectedGroup = indicator">{{ indicator.category }}</a>
            </li>
          </ul>
        </aside>

      </div>

      <div class="column mx-1 my-5">
        <div class="level">


          <div class="level-left">
            <div class="level-item">

              <!-- <div class="container mb-4"> -->
              <p>{{ selectedGroup?.category || '' }}</p>
              <!-- </div> -->
            </div>
          </div>

          <div class="level-right">
            <div class="level-item">
              <!-- <button class="button is-primary">
                Save
              </button>
            -->
              <button class="button mr-2" @click.prevent="closeButton">
                Close
              </button>
            </div>
          </div>



        </div>
        <hr>

        <AccordionList>

          <AccordionItem v-for="item in groupIndicators" :key="item.id">
            <template #summary>{{ item.name }}</template>
            <!-- <template #icon>
              <button class="button is-danger">Remove</button>
              <button class="button is-primary">Add</button>
            </template> -->

            <!-- Main content -->
            <div class="card is-shadowless is-small">
              <div class="card-content">
                <p>{{ item.notes }}
                </p>
              </div>

              <footer class="card-footer">
                <p class="card-footer-item">
                  <button class="is-small button is-primary">
                    Add Indicator
                  </button>
                </p>
                <p class="card-footer-item">
                  <span>
                    Remove
                  </span>
                </p>
              </footer>
            </div>
          </AccordionItem>
        </AccordionList>

      </div>

    </div>

    <!-- <div style="padding-top: 70px; color: #f14668">
      <h2 v-for="item in 50" :key="item"
        :style="{ fontSize: '58px', fontWeight: 700, opacity: item * 2 / 100, lineHeight: '43px' }">
        This is scrolled body!
      </h2>

      <button @click.prevent="closeButton" class="button is-primary">Close</button>
    </div> -->

  </VueSidePanel>
</template>

<style>
.text-with-line-breaks {
  white-space: pre-line;
}
</style>
