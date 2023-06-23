<script lang="ts" setup>

import { useTheoryOfChangeStore } from '@/stores/theory_of_change';
import { Monitoring } from '@/types';
import { Modal, Form, FormItem, Button, Select, SelectOption, Spin, type FormInstance, message, Space } from 'ant-design-vue';
import { ref, watch } from 'vue';
import IndicatorBrowserPanel from '@/views/theory-of-change/IndicatorBrowserPanel.vue'
import { useCommunicationStore } from '@/stores/communication.store';


const props = defineProps<{ visible: boolean }>();
const emit = defineEmits<{
  (e: 'isClosed', status: boolean): boolean,
  // (e: 'isUpdated', status: boolean): void,
}>()


const theoryOfChangeStore = useTheoryOfChangeStore(),
  store = useCommunicationStore();

const newIndicatorFormRef = ref<FormInstance>(),
  config = ref({
    visible: props.visible,
    form: {
      toc_item_id: null,
      indicator_id: null,
    },
    browser: {
      visible: false,
      theoryOfChange: null,
    }
  });


watch((props), (newProps) => {
  config.value.visible = newProps.visible;
}, { deep: true })

function closeModal() {
  newIndicatorFormRef.value.resetFields();
  config.value.visible = false;

  emit('isClosed', true);
}

function onPanelClosed() {
  config.value.browser.visible = false;
  config.value.browser.theoryOfChange = null;
  store.download();

  closeModal();
}

const onTheoryOfChangeSelected = (value: number, _option: any) => {

  const item = useTheoryOfChangeStore().getByTocId(+value);

  if (item == undefined) {
    message.error('An error occurred while fetching theory of change item');
    return;
  }

  config.value.browser.theoryOfChange = item;
}

function save() {
  newIndicatorFormRef.value
    .validateFields()
    .then(_ => {
      // TODO: rewrite adding monitoring item

      // theoryOfChangeStore.saveIndicators({
      //   tocItemId: config.value.form.toc_item_id,
      //   added: [config.value.form.indicator_id],
      //   removed: [],
      // })
      //   .then((_resp) => {
      //     message.success('Indicator added successfully!');
      //     emit('isUpdated', true);

      //     closeModal();
      //   })
      //   .catch((error) => {
      //     message.error(error.message);
      //   });
    });
}


</script>

<template>
  <Modal v-model:visible="config.visible" title="Add New Indicator" @cancel="closeModal()" :mask-closable="false">

    <!-- IndiKit Browser Panel -->
    <IndicatorBrowserPanel v-if="config.browser.theoryOfChange != null" :is-visible="config.browser.visible"
      @is-closed="onPanelClosed()" :toc-item="config.browser.theoryOfChange">
    </IndicatorBrowserPanel>

    <template #footer>
      <Space>
        <Button @click="closeModal()">Cancel</Button>
        <Button type="primary" @click="config.browser.visible = true"
          :disabled="config.browser.theoryOfChange == null || config.form.toc_item_id == null">Next</Button>
      </Space>
    </template>

    <Spin :spinning="theoryOfChangeStore.isLoading">

      <Form layout="vertical" :model="config.form" name="progress_tracking_form" ref="newIndicatorFormRef">

        <!-- TODO: exclude already tracked periods from dropdown -->
        <FormItem name="toc_item_id" label="Select theory of change item" has-feedback
          :rules="[{ required: true, message: 'Please select theory of change!' }]">
          <Select v-model:value="config.form.toc_item_id" placeholder="Please theory of change item" :show-search="true"
            :allow-clear="true" @change="onTheoryOfChangeSelected">
            <SelectOption v-for="i in theoryOfChangeStore.theory_of_change" :value="i.id" :key="i.id">{{ i.name }}
            </SelectOption>
          </Select>
        </FormItem>

        <!-- <FormItem name="indicator_id" label="Select indicator" has-feedback
          :rules="[{ required: true, message: 'Please select indicator!' }]">
          <Select v-model:value="config.form.indicator_id" placeholder="Please indicator" :show-search="true"
            :allow-clear="true">
            <SelectOption v-for="i in theoryOfChangeStore.indicatorGroups" :value="i.id" :key="i.id"> {{
              i.name }}
            </SelectOption>
          </Select>
        </FormItem> -->
      </Form>

    </Spin>
  </Modal>
</template>
