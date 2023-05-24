<script lang="ts" setup>
import { ref, reactive, onMounted, onBeforeUnmount, computed, watch } from "vue";
import { Multiselect } from 'vue-multiselect'
import { AccordionList, AccordionItem } from "vue3-rich-accordion";

import { useProjectStore } from "@/stores/projects";
import { ApiRequest } from "@/apis/api";
import { type IndicatorGroup, type IndicatorType, TheoryOfChangeItem } from "@/types";

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
  tocItem: {
    type: TheoryOfChangeItem,
    required: true,
  },
  // theoryOfChange: {
  //   type: TheoryOfChange,
  //   required: true,
  // },
  isVisible: {
    type: Boolean,
    required: true,
  },
});

const selectedIndicatorType = ref<{ id: number, name: string }>(),
  selectedGroup = ref<IndicatorType>(),
  isFetchingIndicators = ref(false),
  indicatorTypes = ref<IndicatorType[]>([]),
  indicatorsList = ref<IndicatorGroup[]>([]),
  config = reactive<{
    isLoading: boolean, indicatorsAdded: number[],
    indicatorsRemoved: number[],
    indicators: Record<string, boolean>
  }>({
    isLoading: false,
    indicatorsAdded: [],
    indicatorsRemoved: [],
    indicators: {

    },
    // added: {

    // }
  });

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

const tocIte = computed(() => {
  if (selectedGroup.value?.id == null) {
    return [];
  }

  return indicatorsList.value.filter(i => i.group_id == selectedGroup.value?.id);
})

function onIndicatorSelected(item: any, _: any) {
  // const temp = indicatorsAdded.value;
  // temp.push(item.id)

  // indicatorsAdded.value = temp;
  // console.log(temp)
}

const closeButton = () => {
  // isOpened.value = false;

  console.error("emitted")
  emit("isClosed", true);
};


const buildIndicatorsTree = (indicators?: any[], configIndicators?: Record<string, boolean>) => {
  const tree: Record<string, boolean> = configIndicators || config.indicators;

  for (const item of indicators || props.tocItem.indicators) {
    tree[`${item.indicator_id}`] = true
  }

  config.indicators = tree;
}

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
  ]).then((resp) => {
    buildIndicatorsTree()
  })
    .finally(() => isFetchingIndicators.value = false);
})

watch(config, (newConfig, _oldConfig) => {
  buildIndicatorsTree(undefined, newConfig.indicators)
}, { deep: true });

watch(props.tocItem, (newVal, old) => {
  buildIndicatorsTree(newVal.indicators)
}, { deep: true });

const removeIndicator = (indicatorId: number) => {
  const temp = config.indicatorsRemoved
  temp.push(indicatorId)

  config.indicatorsRemoved = temp;

  const _temp2 = config.indicatorsAdded;
  const index = _temp2.findIndex(i => i == indicatorId);
  if (index > -1) {
    _temp2.splice(index, 1)
    config.indicatorsAdded = _temp2
  }

  buildIndicatorsTree()
}

// const itemExists = (indicatorId: number) => {
//   console.log(indicatorId)

//   const index = config.indicatorsAdded.findIndex(i => i == indicatorId);
//   if (index > -1) {
//     config.added[`${indicatorId}`] = true
//   }
//   if (!index) {
//     return props.tocItem.indicators
//       .find((i) => i.indicator_id == indicatorId) != null;
//   }

//   return index;
// }

const saveIndicators = async () => {
  config.isLoading = true;

  const removed = Object.keys(config.indicators).filter(i => {
    return !config.indicators[i]
  })

  const added = Object.keys(config.indicators).filter(i => {
    return config.indicators[i]
  }).filter(i => props.tocItem.indicators.find(ind => ind.indicator_id == i) == null)
  // Filter out duplicate indicators
  // const uniqueAdded = props.tocItem.indicators.fi

  console.log(added, removed)
  // TODO: if item is not new, then update it

  await ApiRequest.post(`theory-of-change/${props.tocItem.theory_of_change_id}/indicators`, {
    added: added,
    removed: removed,
  }).then(resp => {
    console.log(resp)

    // emit("onItemAdded", resp);
    // closeModal();
    emit("isClosed", true);
  }).finally(() => {
    config.isLoading = false;
  });
}

// TODO: watch for config.indicators changes and update UI
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
              <button class="button mr-2 is-primary" :class="{ 'is-loading': config.isLoading }"
                :disabled="config.isLoading" @click.prevent="saveIndicators">
                Save
              </button>

              <button class="button mr-2" @click.prevent="closeButton">
                Cancel
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
                <!-- <p class="card-footer-item" v-if="!config.indicators[`${item.id}`] == false">
                                <button class="button is-primary" @click="config.indicators[`${item.id}`] = true">
                                  <span class="icon mr-1">
                                    <i class="fas fa-plus"></i>
                                  </span>
                                  Add Indicator
                                </button>
                              </p> -->

                <p class="card-footer-item">
                  <button class="button"
                    :class="{ 'is-danger': config.indicators[`${item.id}`], 'is-primary': !config.indicators[`${item.id}`] }"
                    @click.prevent="config.indicators[`${item.id}`] = !config.indicators[`${item.id}`]">
                    <span class="icon mr-1">
                      <i class="fas"
                        :class="{ 'fa-trash': config.indicators[`${item.id}`], 'fa-plus': !config.indicators[`${item.id}`] }"></i>
                    </span>
                    {{ config.indicators[`${item.id}`] ? 'Remove ' : 'Add ' }} Indicator
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
