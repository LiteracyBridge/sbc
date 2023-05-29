<script lang="ts" setup>

import { ref, onMounted, computed, watch } from "vue";
import { Multiselect } from 'vue-multiselect'
import { AccordionList, AccordionItem } from "vue3-rich-accordion";
import { ApiRequest } from "@/apis/api";
import { type IndicatorGroup, type IndicatorType, TheoryOfChangeItem, TheoryOfChange } from "@/types";
import { Collapse, CollapsePanel, Empty } from "ant-design-vue";


const emit = defineEmits<{
  (e: 'isClosed', status: boolean): boolean
  (e: 'isSaved', resp: TheoryOfChange | TheoryOfChange[]): TheoryOfChange | TheoryOfChange[]
}>()

const props = defineProps<{ tocItem: TheoryOfChangeItem, isVisible: boolean }>();

const
  collapseKey = ref<string[]>([]),
  selectedMainIndicatorType = ref<{ id: number, name: string }>(),
  selectedGroupType = ref<IndicatorType>(),
  isFetchingIndicators = ref(false),
  mainIndicators = ref<IndicatorType[]>([]),
  indicatorsList = ref<IndicatorGroup[]>([]),
  config = ref<{
    isLoading: boolean,
    indicators: Record<string, boolean>,
  }>({
    isLoading: false,
    indicators: {},
  });

const isOpened = computed(() => props.isVisible)

const getMainIndicators = computed(() => {
  return mainIndicators.value.filter(i => i.parent_id == null);
});

const selectedIndicatorGroups = computed(() => {
  console.log(selectedMainIndicatorType.value);

  if (selectedMainIndicatorType?.value == null) {
    return [];
  }

  return mainIndicators.value.filter(i => i.parent_id == selectedMainIndicatorType.value.id);
});

const groupIndicators = computed(() => {
  if (selectedGroupType.value?.id == null) {
    return [];
  }

  return indicatorsList.value.filter(i => i.group_id == selectedGroupType.value?.id);
})

const closePanel = () => {
  config.value.indicators = {};
  emit("isClosed", true);
};

const buildIndicatorsTree = (indicators: any[]) => {
  const tree: Record<string, boolean> = {};

  for (const item of indicators) {
    tree[`${item.indicator_id}`] = true
  }

  config.value.indicators = tree;
}

onMounted(() => {
  buildIndicatorsTree(props.tocItem?.indicators ?? []);

  isFetchingIndicators.value = true;
  Promise.all([
    ApiRequest.get<IndicatorType[]>("indicators/types")
      .then((resp) => {
        console.log(resp)
        if (resp != null) {
          mainIndicators.value = resp;
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
    buildIndicatorsTree(props.tocItem?.indicators ?? [])
  })
    .finally(() => isFetchingIndicators.value = false);
})


watch(props, (newProp) => {
  buildIndicatorsTree(newProp.tocItem.indicators)

  // Update panel with ToC item existing indicator
  const _indicators = newProp.tocItem?.indicators ?? [];
  if (_indicators.length > 0) {
    const indicator = indicatorsList.value.find(i => i.id == _indicators[0].indicator_id);
    const indicatorType = mainIndicators.value.find(i => i.id == indicator?.group_id);

    selectedGroupType.value = indicatorType;
    selectedMainIndicatorType.value = mainIndicators.value.find(i => i.id == indicatorType?.parent_id);
  }
}, { deep: true });


const saveIndicators = async () => {
  config.value.isLoading = true;

  const removed = Object.keys(config.value.indicators).filter(i => {
    return !config.value.indicators[i]
  })

  const added = Object.keys(config.value.indicators).filter(i => {
    return config.value.indicators[i]
  }).filter(i => props.tocItem.indicators.find(ind => ind.indicator_id == +i) == null)

  await ApiRequest.post<TheoryOfChange>(`theory-of-change/${props.tocItem.id}/indicators`, {
    added: added,
    removed: removed,
  }).then(resp => {
    emit("isSaved", resp);
    closePanel();
  }).finally(() => {
    config.value.isLoading = false;
  });
}

</script>

<template>
  <VueSidePanel v-model="isOpened" :hide-close-btn="true" :no-close="true" lock-scroll width="80vw"
    transition-name="slide-right">

    <div class="columns">
      <div class="column is-one-fifth mx-5 my-5">

        <!-- TODO: add label -->
        <label class="label">Select Indicator</label>

        <Multiselect v-model="selectedMainIndicatorType" :options="getMainIndicators" :close-on-select="true"
          :clear-on-select="false" placeholder="Select indicator" label="name" track-by="value" />
        <hr>

        <aside class="menu">
          <p class="menu-label">
            {{ selectedMainIndicatorType?.name || 'No indicatory type selected' }}
          </p>

          <ul class="menu-list">
            <li v-for="indicator in selectedIndicatorGroups" :key="indicator.id">
              <a @click.prevent="selectedGroupType = indicator">{{ indicator.name }}</a>
            </li>
          </ul>
        </aside>

      </div>

      <div class="column mx-1 my-5">
        <div class="level">


          <div class="level-left">
            <div class="level-item">

              <!-- <div class="container mb-4"> -->
              <h3 class="has-text-weight-bold">{{ selectedGroupType?.name || '' }}</h3>
              <!-- </div> -->
            </div>
          </div>

          <div class="level-right">
            <div class="level-item">

              <button class="button mr-2 is-primary" :class="{ 'is-loading': config.isLoading }"
                :disabled="config.isLoading" @click.prevent="saveIndicators">
                Save
              </button>

              <button class="button mr-2" @click.prevent="closePanel">
                Cancel
              </button>
            </div>
          </div>

        </div>
        <hr>

        <div v-if="groupIndicators?.length == 0" style="margin-top: auto; position: fixed; top: 50%; left: 55%;">
          <Empty description="Choose indicator from the dropdown list"></Empty>
        </div>

        <Collapse v-model:activeKey="collapseKey" v-else>
          <CollapsePanel v-for="item in groupIndicators" :key="item.id" :header="item.name">
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
          </CollapsePanel>

        </Collapse>

      </div>

    </div>

  </VueSidePanel>
</template>

<style>
.text-with-line-breaks {
  white-space: pre-line;
}
</style>
