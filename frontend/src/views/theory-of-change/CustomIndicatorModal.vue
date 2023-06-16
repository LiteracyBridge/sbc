<script lang="ts"  setup>

import { ref, computed, watch } from "vue";
import { ProjectIndicator, Risk, TheoryOfChange, TheoryOfChangeItem } from "@/types";
import { AutoComplete, Modal, Row } from "ant-design-vue";
import { useTheoryOfChangeStore } from "@/stores/theory_of_change";

const emit = defineEmits<{
  (e: 'closed', status: boolean): boolean
  (e: 'saved', resp: TheoryOfChange[]): TheoryOfChange[]
}>()

const props = defineProps<{ visible: boolean, theoryOfChange: TheoryOfChange }>()

const config = ref({
  visible: props.visible,
  customIndicator: '',
  loading: false,
  selectedIndicator: null as ProjectIndicator | null,
})

const theoryOfChangeStore = useTheoryOfChangeStore();

watch(props, (newProps) => {
  config.value.visible = newProps.visible;
});

const closeModal = (redraw = true) => {
  config.value.visible = false;
  emit('closed', true);
};

const onIndicatorSelected = (label: string, option: ProjectIndicator) => {
 config.value.selectedIndicator = option;
  console.log(label, option);
}

const getProjectIndicators = computed(() => {
  return theoryOfChangeStore.project_indicators.map(i => {
    return { ...i, label: i.name, value: i.name }
  })
});

function saveIndicator(){
  let indicator = theoryOfChangeStore.project_indicators.find(i => i.name?.toLowerCase() == config.value.customIndicator);

  // TODO: create indicator if not exists
  if (indicator == null) {
    indicator = config.value.selectedIndicator;
  }

  // let indicator = config.value.selectedIndicator;
}
</script>

<template>
  <Modal v-model:visible="config.visible" title="Add Indicator" @cancel="closeModal()" @ok="saveIndicator()">
    <Row>
      <AutoComplete v-model:value="config.customIndicator" :options="getProjectIndicators" size="small"
        placeholder="Add indicator" style="width: 100%;" @select="onIndicatorSelected">
      </AutoComplete>
    </Row>
  </Modal>
</template>
