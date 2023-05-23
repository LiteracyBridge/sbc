<script lang="ts" setup>
import { ref, reactive, onMounted, onBeforeUnmount, computed } from "vue";
import { Multiselect } from 'vue-multiselect'
import { AccordionList, AccordionItem } from "vue3-rich-accordion";

import { useProjectStore } from "@/stores/projects";
import { ApiRequest } from "@/apis/api";

const projectStore = useProjectStore();

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
  theoryOfChangeId: {
    type: Number,
    required: true,
  },
  isVisible: {
    type: Boolean,
    required: true,
  }
});

const selectedIndicatorType = ref<{ id: number, name: string }>(),
  selectedGroup = ref<IndicatorType>(),
  isFetchingIndicators = ref(false),
  indicatorTypes = ref<IndicatorType[]>([]),
  indicatorsList = ref<IndicatorGroup[]>([]);

const isOpened = computed(() => props.isVisible)

const selectedIndicatorGroups = computed(() => {
  console.log(selectedIndicatorType.value);

  if (selectedIndicatorType?.value == null) {
    return [];
  }

  return indicatorTypes.value.filter(i => i.parent_id == selectedIndicatorType.value.id);
});

const getMainIndicators = computed(() => {
  return indicatorTypes.value.filter(i => i.parent_id == null);
});

const groupIndicators = computed(() => {
  if (selectedGroup.value?.id == null) {
    return [];
  }

  return indicatorsList.value.filter(i => i.group_id == selectedGroup.value?.id);
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
  // selectedGroup.value = getMainIndicators.value[0];

  isFetchingIndicators.value = true;
  Promise.all([
    ApiRequest.get<IndicatorType[]>("indicators/types")
      .then((resp) => {
        console.log(resp)
        if (resp != null) {
          indicatorTypes.value = resp;
        }
      }),

    ApiRequest.get<IndicatorGroup[]>("indicators")
      .then((resp) => {
        console.log(resp)

        if (resp != null) {
          indicatorsList.value = resp;
        }
      })
  ]).then((resp) => console.log(resp))
    .finally(() => isFetchingIndicators.value = false);
})

const saveIndicator = (id: number) => {
  // theory-of-change
}

</script>

<template>
  <VueSidePanel v-model="isOpened" :hide-close-btn="true" :no-close="true" lock-scroll width="80vw"
    transition-name="slide-right">

    <div class="columns">
      <div class="column is-one-fifth mx-5 my-5">

        <!-- TODO: add label -->
        <label class="label">Select Indicator</label>

        <Multiselect v-model="selectedIndicatorType" :options="getMainIndicators" :close-on-select="true"
          :clear-on-select="false" placeholder="Select indicator" label="name" track-by="value"
          @select="onIndicatorSelected" />
        <hr>

        <aside class="menu">
          <p class="menu-label">
            {{ selectedIndicatorType?.name || 'No indicatory type selected' }}
          </p>

          <ul class="menu-list">
            <li v-for="indicator in selectedIndicatorGroups" :key="indicator.id">
              <a @click.prevent="selectedGroup = indicator">{{ indicator.name }}</a>
            </li>
          </ul>
        </aside>

      </div>

      <div class="column mx-1 my-5">
        <div class="level">


          <div class="level-left">
            <div class="level-item">

              <!-- <div class="container mb-4"> -->
              <h3 class="has-text-weight-bold">{{ selectedGroup?.name || '' }}</h3>
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

        <!-- TODO: show a helper text in center if nothing is selected -->
        <AccordionList>

          <AccordionItem v-for="item in groupIndicators" :key="item.id">
            <template #summary>{{ item.name }}</template>

            <!-- Main content -->
            <div class="card is-shadowless is-small">
              <div class="card-content">
                <div class="columns">
                  <div class="column is-2">
                    <strong>Indicator Phrasing</strong>
                  </div>
                  <div class="column">
                    <p>{{ item.phrasing }}</p>
                  </div>
                </div>
                <hr>

                <div class="columns">
                  <div class="column is-2">
                    <strong>What is its purpose?</strong>
                  </div>
                  <div class="column">
                    <p>{{ item.purpose }}</p>
                    <a :href="item.link" target="_blank">Click to learn more about learn more the indicatory</a>
                  </div>
                </div>
              </div>

              <footer class="card-footer">
                <p class="card-footer-item">
                  <button class="button is-primary">
                    <span class="icon mr-1">
                      <i class="fas fa-plus"></i>
                    </span>
                    Add Indicator
                  </button>
                </p>
                <p class="card-footer-item">
                  <button class="button is-danger">
                    <span class="icon mr-1">
                      <i class="fas fa-trash"></i>
                    </span>
                    Remove Indicator
                  </button>
                </p>
              </footer>
            </div>
          </AccordionItem>
        </AccordionList>

      </div>

    </div>

  </VueSidePanel>
</template>

<style>
.text-with-line-breaks {
  white-space: pre-line;
}
</style>
