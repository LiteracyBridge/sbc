<script lang="ts" setup>
import { ref, onMounted, computed, watch } from "vue";
import { useTheoryOfChangeStore } from "@/stores/theory_of_change";
import { IndicatorType, LuIndiKit, ProjectIndicator, TheoryOfChange } from "@/types";
import {
  Collapse,
  CollapsePanel,
  Empty,
  Row,
  Col,
  Form,
  Drawer,
  Button,
  Space,
  Divider,
  AutoComplete,
  Select,
  FormItem,
  Input,
  Typography,
  Avatar,
  List,
  ListItem,
  Popconfirm,
  Descriptions,
  DescriptionsItem,
  Card,
} from "ant-design-vue";
import { PlusOutlined, DeleteOutlined } from "@ant-design/icons-vue";
import { uniqBy } from "lodash-es";
import { useLookupStore } from "@/stores/lookups";

const emit = defineEmits<{
  (e: "isClosed", status: boolean): boolean;
  (e: "isSaved", resp: TheoryOfChange[]): TheoryOfChange;
}>();

const props = defineProps<{ tocItem: TheoryOfChange; isVisible: boolean }>();

const theoryOfChangeStore = useTheoryOfChangeStore(),
  lookup = useLookupStore();

const collapseKey = ref<string[]>([]),
  selectedMainIndicatorType = ref<string>(null),
  selectedGroupType = ref<string>(),
  config = ref({
    tocItem: props.tocItem,
    visible: props.isVisible,
    isLoading: false,
    selectedIndiKit: {} as Record<string, boolean>,
    customIndicator: "",
    selectedIndicator: null,
    // reqBody: {
    //   removed: [],
    //   removed_custom: [],
    //   added: [] as Array<{ id?: number; name: string; indi_kit_id?: number }>,
    // },
  });

const tracker = ref<
  {
    id?: number;
    name: string;
    indikit_id?: number;
    is_new: boolean;
    is_deleted: boolean;
    is_updated?: boolean;
  }[]
>([]);

const groupIndicators = computed(() => {
  if (selectedGroupType.value == null) {
    return [];
  }

  return lookup.indikit[selectedMainIndicatorType.value][selectedGroupType.value];
});

const filterIndicatorSectors = (input: string, option: any) => {
  return option.sector.toLowerCase().indexOf(input?.toLowerCase() ?? "") >= 0;
};

const closePanel = () => {
  config.value = {
    isLoading: false,
    tocItem: new TheoryOfChange(),
    visible: false,
    selectedIndiKit: {},
    customIndicator: "",
    selectedIndicator: null,
    // reqBody: {
    //   removed: [],
    //   removed_custom: [],
    //   added: [],
    // },
  };
  tracker.value = [];
  emit("isClosed", true);
};

const buildIndicatorsTree = (indicators?: any[]) => {
  indicators ??= [];
  const tree: Record<string, boolean> = {};

  for (const item of indicators) {
    tree[`${item.indicator_id}`] = true;
  }

  config.value.selectedIndiKit = tree;
  tracker.value = (config.value.tocItem.indicators ?? []).flatMap((i) => {
    return {
      id: i.id,
      name: i?.name ?? i?.indikit?.name ?? "",
      indi_kit_id: i?.indikit_id,
      is_new: false,
      is_deleted: false,
      is_updated: false,
    };
  });
};

onMounted(() => {
  buildIndicatorsTree(config.value.tocItem?.indicators ?? []);

  config.value.isLoading = true;

  theoryOfChangeStore
    .fetchIndiKit()
    .then((resp) => {
      buildIndicatorsTree(config.value.tocItem?.indicators ?? []);
    })
    .finally(() => (config.value.isLoading = false));
});

watch(
  props,
  (newProp) => {
    config.value.visible = newProp.isVisible;
    config.value.tocItem = newProp.tocItem;

    // Update panel with ToC item existing indicator
    const _indicators = newProp.tocItem?.indicators ?? [];
    buildIndicatorsTree(_indicators);

    // if (_indicators.length > 0) {
    //   const indicator = theoryOfChangeStore.indicatorGroups.find(
    //     (i) => i.id == _indicators[0].id
    //   );
    //   const indicatorType = theoryOfChangeStore.indicatorTypes.find(
    //     (i) => i.id == indicator?.group_id
    //   );

    //   selectedGroupType.value = indicatorType;
    //   const _find = theoryOfChangeStore.indicatorTypes.find(
    //     (i) => i.id == indicatorType?.parent_id
    //   );
    //   selectedMainIndicatorType.value = _find?.id;
    // }
  },
  { deep: true }
);

const saveIndicators = async () => {
  config.value.isLoading = true;

  theoryOfChangeStore
    .saveIndicators({
      tocId: config.value.tocItem.id,
      data: tracker.value,
    })
    .then((resp) => {
      config.value.tocItem = resp.find((i) => i.id == config.value.tocItem.id);
      emit("isSaved", theoryOfChangeStore.theory_of_change);
      closePanel();
    })
    .finally(() => {
      config.value.isLoading = false;
    });
};

const getTocIndicators = computed(() => {
  // const _temp = (config.value.tocItem.indicators ?? []).flatMap((i) => {
  //   return {
  //     id: i.id,
  //     name: i?.name ?? i?.indikit?.name ?? "",
  //     indi_kit_id: i?.indikit_id,
  //     is_new: false,
  //     is_deleted: false,
  //     is_updated: false,
  //   };
  // });

  // const all = (.concat(_temp);

  return tracker.value.filter((i) => !(i.is_deleted ?? false)) ?? [];
  // Filter out removed indicators
  // return all.filter((i) => {
  //   return config.value.reqBody.removed.find((r) => r == i.id) == null;
  // });
});

// Custom indicator handlers
const getProjectIndicators = computed(() => {
  return uniqBy(
    theoryOfChangeStore.theoryOfChangeItemIndicators(props.tocItem.id).map((i) => {
      return { ...i, label: i.name, value: i.name };
    }),
    "name"
  );
});

const makeIndicatorAsDeleted = (
  name: string,
  customId?: number,
  indi_kit_id?: number
) => {
  // If id is not provided, then it's a new custom indicator
  if (customId != null) {
    // const _temp = tracker.value;
    // const index = _temp.findIndex((i) => i.id == null && i.name == name);

    // _temp.splice(index, 1);
    // config.value.reqBody.added = _temp;
    tracker.value = tracker.value.map((i) => {
      if (i.name == name && i.id == customId) {
        i.is_deleted = true;
      }
      return i;
    });
    return;
  }

  if (indi_kit_id != null) {
    tracker.value = tracker.value.map((i) => {
      if (i.name == name && i.indikit_id == indi_kit_id) {
        i.is_deleted = true;
      }
      return i;
    });
    // config.value.reqBody.removed = [...config.value.reqBody.removed, indi_kit_id];
    return;
  }

  // Fallback to project indicators using the name to find the indicator
  if (name != null) {
    // const _temp = tracker.value;
    // const index = _temp.findIndex((i) => i.id == null && i.name == name);

    // _temp.splice(index, 1);
    // config.value.reqBody.added = _temp;
    tracker.value = tracker.value.map((i) => {
      if (i.name == name) {
        i.is_deleted = true;
      }
      return i;
    });
    return;
  }

  // config.value.reqBody.removed = [...config.value.reqBody.removed, customId];
};

const onProjectIndicatorSelected = (label: string, option?: ProjectIndicator) => {
  console.log(label, option);

  label = label.trim();
  if (option != null) {
    config.value.selectedIndicator = option;
  }

  // 1. Check if indicator already exists in project indicators
  // if true, add it to the toc indicators list
  // const exits = theoryOfChangeStore.allTocIndicators.find((i) => i.name.trim() == label);
  // if (exits != null) {
  tracker.value = [
    ...tracker.value,
    { name: label, id: null, indikit_id: null, is_new: true, is_deleted: false },
  ];
  // config.value.reqBody.added = [
  //   ...config.value.reqBody.added,
  //   { id: exits.id, name: exits.name, indi_kit_id: null },
  // ];
  // return;
  // }

  // 2. If not, add it to the project indicators list and then add it to the toc indicators list
  // config.value.reqBody.added = [
  //   ...config.value.reqBody.added,
  //   { name: label, id: null, indi_kit_id: null },
  // ];
};

const addIndiKitIndicator = (item: LuIndiKit) => {
  // console.log("adding");
  // const exists = config.value.reqBody.added.find((i) => i.indi_kit_id == item.id);

  // if (exists != null) return;

  // config.value.reqBody.added = [
  //   ...config.value.reqBody.added,
  //   { name: item.name, indi_kit_id: item.id, id: null },
  // ];
  tracker.value = [
    ...tracker.value,
    { name: item.name, indikit_id: item.id, id: null, is_new: true, is_deleted: false },
  ];
};

const getSectors = computed(() => {
  return Object.keys(lookup.indikit).map((key) => {
    return { label: key, value: key };
  });
});
</script>

<template>
  <Drawer
    width="70vw"
    title="Indicators Browser"
    :visible="config.visible"
    :body-style="{ paddingBottom: '80px' }"
    :footer-style="{ textAlign: 'right' }"
    @close="closePanel()"
  >
    <template #extra>
      <Space>
        <Button
          type="primary"
          :loading="config.isLoading"
          :disabled="config.isLoading"
          @click="saveIndicators"
        >
          Save
        </Button>

        <Button @click="closePanel"> Cancel </Button>
      </Space>
    </template>

    <template #footer>
      <p>
        Indicator library is powered by
        <Avatar src="https://www.indikit.net/favicon/android-chrome-192x192.png" />
        <a target="_blank" href="https://www.indikit.net">IndiKit</a>, guidance on SMART
        indicators for relief and development projects.
      </p>
    </template>

    <!-- Display list of project indicators -->
    <Row v-if="getTocIndicators.length > 0" style="margin-bottom: 20px">
      <Col :span="14">
        <List item-layout="horizontal">
          <ListItem v-for="indicator in getTocIndicators" :key="indicator.id">
            {{ indicator.name }}

            <template #actions>
              <Popconfirm
                title="Are you sure? Corresponding monitoring item(s) will be deleted!"
                ok-text="Yes"
                cancel-text="No"
                @confirm="
                  makeIndicatorAsDeleted(
                    indicator.name,
                    indicator.id,
                    indicator.indikit_id
                  )
                "
              >
                <Button size="small" type="primary" :ghost="true" :danger="true"
                  >Remove
                </Button>
              </Popconfirm>
            </template>
          </ListItem>
        </List>
      </Col>
    </Row>

    <Form layout="vertical">
      <Row>
        <Col :span="12">
          <FormItem label="Can't find indicator in library? Add your own">
            <AutoComplete
              v-model:value="config.customIndicator"
              :options="getProjectIndicators"
              size="small"
              placeholder="Enter indicator name"
              style="width: 100%; height: 60px;"
              @select="onProjectIndicatorSelected"
            >
            </AutoComplete>
          </FormItem>
        </Col>

        <Col :span="4">
          <Button
            type="primary"
            style="margin-top: 28px; margin-left: 10px"
            :ghost="true"
            @click="onProjectIndicatorSelected(config.customIndicator)"
            >Add</Button
          >
        </Col>
      </Row>
    </Form>

    <Divider>
      <Typography.Title :level="5">Browse Indicators Library</Typography.Title>
    </Divider>

    <Row :gutter="0">
      <Col :span="7">
        <label>Select Indicator Sector:</label> <br />
        <Select
          v-model:value="selectedMainIndicatorType"
          show-search
          placeholder="Select an indicator sector"
          style="width: 330px"
          class="mt-2"
          :allow-clear="true"
          :options="getSectors"
          :filter-option="filterIndicatorSectors"
        >
        </Select>

        <Divider></Divider>

        <aside class="menu">
          <p class="menu-label">
            <span v-if="selectedMainIndicatorType != null">
              {{ selectedMainIndicatorType }}
            </span>

            <span v-else>
              <!-- TODO: use alert component -->
              No indicatory sector selected!
            </span>
          </p>

          <ul class="menu-list">
            <li
              v-for="sub_sector in Object.keys(
                lookup.getSubSectors(selectedMainIndicatorType)
              )"
              :key="sub_sector"
            >
              <a @click.prevent="selectedGroupType = sub_sector">{{ sub_sector }}</a>
            </li>
          </ul>
        </aside>
      </Col>

      <Col :span="16">
        <div
          v-if="groupIndicators?.length == 0"
          style="margin-top: auto; position: fixed; top: 50%; left: 55%"
        >
          <Empty description="Choose indicator from the dropdown list"></Empty>
        </div>

        <Collapse v-model:activeKey="collapseKey" v-else>
          <CollapsePanel
            v-for="item in groupIndicators"
            :key="item.id"
            :header="item.name"
          >
            <template #extra>
              <Button
                :danger="config.selectedIndiKit[`${item.id}`]"
                type="primary"
                size="small"
                @click="
                  config.selectedIndiKit[`${item.id}`] = !config.selectedIndiKit[
                    `${item.id}`
                  ];
                  addIndiKitIndicator(item);
                "
              >
                <template #icon>
                  <PlusOutlined v-if="!config.selectedIndiKit[`${item.id}`]" />
                </template>

                {{ config.selectedIndiKit[`${item.id}`] ? "Remove " : "Add " }}
              </Button>
            </template>

            <Row :gutter="2">
              <Col :span="4">
                <strong>Indicator Phrasing</strong>
              </Col>
              <Col :span="18">
                <p>{{ item.wording_english }}</p>
              </Col>
            </Row>

            <Row :gutter="2" class="mt-3">
              <Col :span="4">
                <strong>Purpose</strong>
              </Col>
              <Col :span="18">
                <p>{{ item.purpose }}</p>
              </Col>
            </Row>

            <Row :gutter="2" class="mt-3">
              <Col :span="4">
                <strong>Guidance</strong>
              </Col>
              <Col :span="18">
                <a :href="item.guidance" target="_blank"
                  >Click to learn more about learn more the indicator on IndiKit</a
                >
              </Col>
            </Row>
          </CollapsePanel>
        </Collapse>
      </Col>
    </Row>
  </Drawer>
</template>
