<script lang="ts" setup>

import { ref, onMounted, computed, watch } from "vue";
import { useTheoryOfChangeStore } from "@/stores/theory_of_change";
import { IndicatorType, TheoryOfChange, TheoryOfChangeItem } from "@/types";

const emit = defineEmits<{
  (e: 'isClosed', status: boolean): boolean
  (e: 'isSaved', resp: TheoryOfChange | TheoryOfChange[]): TheoryOfChange
}>()

const props = defineProps<{ tocItem: TheoryOfChangeItem, isVisible: boolean }>();

const theoryOfChangeStore = useTheoryOfChangeStore();

const
  collapseKey = ref<string[]>([]),
  selectedMainIndicatorType = ref<number>(null),
  selectedGroupType = ref<IndicatorType>(),
  isFetchingIndicators = ref(false),
  config = ref<{
    isLoading: boolean,
    indicators: Record<string, boolean>,
  }>({
    isLoading: false,
    indicators: {},
  });

const isOpened = computed(() => props.isVisible)

const getMainSectors = computed(() => {
  return theoryOfChangeStore.indicatorTypes.filter(i => i.parent_id == null);
});

const selectedIndicatorGroups = computed(() => {
  console.log(selectedMainIndicatorType.value);

  if (selectedMainIndicatorType?.value == null) {
    return [];
  }

  return theoryOfChangeStore.indicatorTypes.filter(i => i.parent_id == selectedMainIndicatorType.value as unknown as number);
});

const groupIndicators = computed(() => {
  if (selectedGroupType.value?.id == null) {
    return [];
  }

  return theoryOfChangeStore.indiKitSubSectorIndicators(selectedGroupType.value?.id);
  // return theoryOfChangeStore.indicatorGroups.filter(i => i.group_id == selectedGroupType.value?.id);
})

const filterIndicatorSectors = (input: string, option: any) => {
  return option.sector.toLowerCase().indexOf(input?.toLowerCase() ?? '') >= 0;
};

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

  theoryOfChangeStore.fetchIndiKit().then(resp => {
    buildIndicatorsTree(props.tocItem?.indicators ?? [])
  }).finally(() => isFetchingIndicators.value = false);
})


watch(props, (newProp) => {
  buildIndicatorsTree(newProp.tocItem.indicators)

  // Update panel with ToC item existing indicator
  const _indicators = newProp.tocItem?.indicators ?? [];
  if (_indicators.length > 0) {
    const indicator = theoryOfChangeStore.indicatorGroups.find(i => i.id == _indicators[0].indicator_id);
    const indicatorType = theoryOfChangeStore.indicatorTypes.find(i => i.id == indicator?.group_id);

    selectedGroupType.value = indicatorType;
    const _find = theoryOfChangeStore.indicatorTypes.find(i => i.id == indicatorType?.parent_id);
    selectedMainIndicatorType.value =  _find?.id
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

  theoryOfChangeStore.saveIndicators({ tocItemId: props.tocItem.id, added: added, removed: removed })
    .then(resp => {
      emit("isSaved", theoryOfChangeStore.theory_of_change);
      closePanel();
    }).finally(() => {
      config.value.isLoading = false;
    });
}

</script>

<template>
  <Drawer width="70vw" title="Indicators Browser" :visible="isOpened" :body-style="{ paddingBottom: '80px' }"
    :footer-style="{ textAlign: 'right' }" @close="closePanel()">

    <template #extra>
      <Space>
        <Button type="primary" :loading="config.isLoading" :disabled="config.isLoading" @click="saveIndicators">
          Save
        </Button>

        <Button @click="closePanel">
          Cancel
        </Button>
      </Space>
    </template>

    <template #footer>
      <p>Indicator library is powered by IndiKit {add ref}</p>
    </template>

    <Form layout="vertical">
      <Row>
        <Col :span="12">
        <FormItem label="Can't find indicator in library? Add you own">
          <Input placeholder="Enter indicator name" />
        </FormItem>
        </Col>

        <Col :span="4">
        <Button type="primary" style="margin-top: 28px; margin-left: 10px;" :ghost="true">Add</Button>
        </Col>

        <!-- TODO: display list of indicators pending to be saved -->

      </Row>
    </Form>

    <Divider>
      <Typography.Title :level="5">or browse our library</Typography.Title>
    </Divider>

    <div class="columns">
      <div class="column is-one-fifth mr-5 mb-5">

        <!-- TODO: add label -->
        <label class="label"></label>
        <FormItem label="Select Indicator Sector">
          <Select v-model:value="selectedMainIndicatorType" show-search placeholder="Select an indicator sector"
            style="width: 200px" :allow-clear="true" :options="theoryOfChangeStore.indi_kit_library"
            :field-names="{ label: 'sector', value: 'id' }" :filter-option="filterIndicatorSectors">
          </Select>
        </FormItem>

        <Divider></Divider>


        <aside class="menu">
          <p class="menu-label">
            <span v-if="selectedMainIndicatorType != null">
              {{ theoryOfChangeStore.getIndiKitItemById(selectedMainIndicatorType)?.name }}
            </span>

            <span v-else>
              <!-- TODO: use alert component -->
              No indicatory sector selected!
            </span>
          </p>

          <ul class="menu-list">
            <li v-for="indicator in theoryOfChangeStore.indiKitSubSectors(selectedMainIndicatorType)" :key="indicator.id">
              <a @click.prevent="selectedGroupType = indicator">{{ indicator.sub_sector }}</a>
            </li>
          </ul>
        </aside>

      </div>

      <div class="column mb-5">
        <TypographyTitle :level="4">
          {{ selectedGroupType?.name || '' }}
        </TypographyTitle>

        <Divider></Divider>

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
                    <p>{{ item.wording_english }}</p>
                  </div>
                </div>
                <hr>

                <div class="columns">
                  <div class="column is-2">
                    <strong>What is its purpose?</strong>
                  </div>
                  <div class="column">
                    <p>{{ item.purpose }}</p>
                    <a :href="item.guidance" target="_blank">Click to learn more about learn more the indicatory</a>
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

  </Drawer>
</template>
