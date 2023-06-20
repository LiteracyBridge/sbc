<script lang="ts" setup>

import { ref, onMounted, computed, watch } from "vue";
import { useTheoryOfChangeStore } from "@/stores/theory_of_change";
import { IndicatorType, LuIndiKit, ProjectIndicator, TheoryOfChange, TheoryOfChangeItem } from "@/types";
import { Collapse, CollapsePanel, Empty, Row, Col, Form, Drawer, Button, Space, Divider, AutoComplete, Select, FormItem, Input, Typography, Avatar, List, ListItem, ListItemMeta } from "ant-design-vue";
import { PlusOutlined, DeleteOutlined } from "@ant-design/icons-vue";
import { markAsUntransferable } from "worker_threads";

const emit = defineEmits<{
  (e: 'isClosed', status: boolean): boolean
  (e: 'isSaved', resp: TheoryOfChange | TheoryOfChange[]): TheoryOfChange
}>()

const props = defineProps<{ tocItem: TheoryOfChange, isVisible: boolean }>();

const theoryOfChangeStore = useTheoryOfChangeStore();

const
  collapseKey = ref<string[]>([]),
  selectedMainIndicatorType = ref<number>(null),
  selectedGroupType = ref<IndicatorType>(),
  isFetchingIndicators = ref(false),
  config = ref<{
    isLoading: boolean,
    selectedIndiKit: Record<string, boolean>,
    customIndicator: string,
    selectedIndicator: ProjectIndicator | null,
    reqBody: {
      removed: number[],
      removed_custom: number[],
      added: Array<{ id?: number, name: string, indi_kit_id?: number }>,
    },
    // newCustomIndicators: Array<{ name: string, id?: number }>,
  }>({
    isLoading: false,
    selectedIndiKit: {},
    customIndicator: '',
    selectedIndicator: null,
    reqBody: {
      removed: [],
      removed_custom: [],
      added: [],
    },
    // newCustomIndicators: [],
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
  config.value.selectedIndiKit = {};
  emit("isClosed", true);
};

const buildIndicatorsTree = (indicators?: any[]) => {
  console.log(props.tocItem?.indicators)

  indicators ??= [];
  const tree: Record<string, boolean> = {};

  for (const item of indicators) {
    tree[`${item.indicator_id}`] = true
  }

  config.value.selectedIndiKit = tree;
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
    selectedMainIndicatorType.value = _find?.id
  }
}, { deep: true });


const saveIndicators = async () => {
  config.value.isLoading = true;

  // const removed = Object.keys(config.value.selectedIndiKit).filter(i => {
  //   return !config.value.selectedIndiKit[i]
  // })

  // const added = Object.keys(config.value.selectedIndiKit).filter(i => {
  //   return config.value.selectedIndiKit[i]
  // }).filter(i => props.tocItem.indicators.find(ind => ind.indicator_id == +i) == null)

  theoryOfChangeStore.saveIndicators({ tocId: props.tocItem.id, data: config.value.reqBody })
    .then(resp => {
      emit("isSaved", theoryOfChangeStore.theory_of_change);
      closePanel();
    }).finally(() => {
      config.value.isLoading = false;
    });
}

const getTocIndicators = computed(() => {
  const _temp = (props.tocItem.indicators ?? []).flatMap(i => {
    return { id: i.id, name: i.indicator?.name ?? i.indicator?.indi_kit?.name ?? '', indi_kit_id: i.indicator?.indi_kit_id };
  });

  const all = config.value.reqBody.added.concat(_temp);

  // Filter out removed indicators
  return all.filter(i => {
    return config.value.reqBody.removed.find(r => r == i.id) == null
  });
  // return theoryOfChangeStore.project_indicators.map(i => {
  //   return { ...i, label: i.name, value: i.name }
  // })
});


// Custom indicator handlers
const getProjectIndicators = computed(() => {
  return theoryOfChangeStore.project_indicators.map(i => {
    return { ...i, label: i.name, value: i.name }
  })
});

const makeIndicatorAsDeleted = (name: string, customIn?: number, indi_kit_id?: number) => {
  // If id is not provided, it means it's a new custom indicator
  if (customIn == null) {
    const _temp = config.value.reqBody.added
    const index = _temp.findIndex(i => i.id == null && i.name == name);

    _temp.splice(index, 1);
    config.value.reqBody.added = _temp;
    return;
  }

  if (indi_kit_id != null) {
    config.value.reqBody.removed = [...config.value.reqBody.removed, indi_kit_id];
    return;
  }


  config.value.reqBody.removed_custom = [...config.value.reqBody.removed_custom, customIn];
}

const isIndicatorDeleted = computed(() => {
  return (indiKitId: number) => {
    return getTocIndicators.value.indexOf((i: { id?: number; name: string; indi_kit_id?: number; }
    ) => i.indi_kit_id == indiKitId) < 0
  };
})

const removeIndicator = (indicator: ProjectIndicator) => {
  config.value.reqBody.removed = [...config.value.reqBody.removed, indicator.id];
  config.value.selectedIndiKit[`${indicator.id}`] = false;
}

const onProjectIndicatorSelected = (label: string, option: ProjectIndicator) => {
  label = label.trim();
  config.value.selectedIndicator = option;
  console.log(label, option);

  // 1. Check if indicator already exists in project indicators
  // if true, add it to the toc indicators list
  const exits = theoryOfChangeStore.project_indicators.find(i => i.name.trim() == label);
  if (exits != null) {
    config.value.reqBody.added = [...config.value.reqBody.added, { id: exits.id, name: exits.name, id: null, indi_kit_id: null}];
    return;
  }

  // 2. If not, add it to the project indicators list and then add it to the toc indicators list
  config.value.reqBody.added = [...config.value.reqBody.added, { name: label, id: null, indi_kit_id: null }];
}

const addIndiKitIndicator = (item: LuIndiKit) => {
  console.log("adding")
  const exists = config.value.reqBody.added.find(i => i.indi_kit_id == item.id);

  if (exists != null) return;

  config.value.reqBody.added = [...config.value.reqBody.added, { name: item.name, indi_kit_id: item.id, id:null }];
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
      <p>Indicator library is powered by
        <Avatar src="https://www.indikit.net/favicon/android-chrome-192x192.png" />
        <a target="_blank" href="https://www.indikit.net">IndiKit</a>, guidance on SMART indicators for relief and
        development projects.
      </p>
    </template>

    <Form layout="vertical">
      <Row>
        <Col :span="12">
        <FormItem label="Can't find indicator in library? Add you own">
          <AutoComplete v-model:value="config.customIndicator" :options="getProjectIndicators" size="small"
            placeholder="Enter indicator name" style="width: 100%;" @select="onProjectIndicatorSelected">
          </AutoComplete>
          <!-- <Input placeholder="Enter indicator name" /> -->
        </FormItem>
        </Col>

        <Col :span="4">
        <Button type="primary" style="margin-top: 28px; margin-left: 10px;" :ghost="true">Add</Button>
        </Col>

        <!-- TODO: display list of indicators pending to be saved -->

        <List item-layout="horizontal">
          <ListItem v-for="indicator in getTocIndicators" :key="indicator.id">
            {{ indicator.name }}

            <template #actions>
              <Button size="small" type="primary" :ghost="true" :danger="true"
                @click="makeIndicatorAsDeleted(indicator.name, indicator.id, indicator.indi_kit_id)">
                <DeleteOutlined /> Remove
              </Button>
            </template>

          </ListItem>
        </List>

      </Row>
    </Form>

    <Divider>
      <Typography.Title :level="5">or browse our library</Typography.Title>
    </Divider>

    <Row :gutter="7">
      <Col :span="8">

      <FormItem label="Select Indicator Sector" layout="vertical" :required="true">
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

      </Col>

      <Col :span="16">
      <!-- <TypographyTitle :level="4">
          {{ selectedGroupType?.name || '' }}
        </TypographyTitle> -->

      <!-- <Divider></Divider> -->

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
                <!-- TODO: add function for adding indicators -->
                <Button :danger="config.selectedIndiKit[`${item.id}`]" type="primary"
                  @click="config.selectedIndiKit[`${item.id}`] = !config.selectedIndiKit[`${item.id}`]; addIndiKitIndicator(item)">
                  <!-- <span class="icon mr-1">
                    <i class="fas"
                      :class="{ 'fa-trash': config.indicators[`${item.id}`], 'fa-plus': !config.indicators[`${item.id}`] }"></i>
                  </span>
                   -->
                  <template #icon>
                    <DeleteOutlined v-if="config.selectedIndiKit[`${item.id}`]" />
                    <PlusOutlined v-else />
                  </template>

                  {{ config.selectedIndiKit[`${item.id}`] ? 'Remove ' : 'Add ' }} Indicator
                </Button>
              </p>
            </footer>
          </div>
        </CollapsePanel>

      </Collapse>

      </Col>

    </Row>

  </Drawer>
</template>
