<script lang="ts" setup>

import { useTheoryOfChangeStore } from '@/stores/theory_of_change';
import { Monitoring } from '@/types';
import { Modal, Form, FormItem, Input, Select, SelectOption, Spin, type FormInstance, message } from 'ant-design-vue';
import { ref, watch } from 'vue';


const props = defineProps<{ visible: boolean }>();
const emit = defineEmits<{
  (e: 'isClosed', status: boolean): boolean,
  (e: 'isUpdated', status: boolean): void,
}>()

const theoryOfChangeStore = useTheoryOfChangeStore();
const newIndicatorFormRef = ref<FormInstance>(),
  config = ref({
    visible: props.visible,
    isLoading: false,
    form: {
      toc_item_id: null,
      indicator_id: null,
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

function save() {
  newIndicatorFormRef.value
    .validateFields()
    .then(_ => {
      theoryOfChangeStore.saveIndicators({
        tocItemId: config.value.form.toc_item_id,
        added: [config.value.form.indicator_id],
        removed: [],
      })
        .then((_resp) => {
          message.success('Indicator added successfully!');
          emit('isUpdated', true);

          closeModal();
        })
        .catch((error) => {
          message.error(error.message);
        });
    });
}


</script>

<template>
  <Modal v-model:visible="config.visible" title="Add New Indicator" ok-text="Save Indicator" cancel-text="Cancel"
    @cancel="closeModal()" :mask-closable="false" @ok="save">

    <Spin :spinning="config.isLoading || theoryOfChangeStore.isLoading">

      <Form layout="vertical" :model="config.form" name="progress_tracking_form" ref="newIndicatorFormRef">

        <!-- TODO: exclude already tracked periods from dropdown -->
        <FormItem name="toc_item_id" label="Select theory of change item" has-feedback
          :rules="[{ required: true, message: 'Please select theory of change item!' }]">
          <Select v-model:value="config.form.toc_item_id" placeholder="Please theory of change item" :show-search="true"
            :allow-clear="true">
            <SelectOption v-for="i in theoryOfChangeStore.theory_of_change.graph" :value="i.id"
              :key="i.id">{{ i.name }}
            </SelectOption>
          </Select>
        </FormItem>

        <FormItem name="indicator_id" label="Select indicator" has-feedback
          :rules="[{ required: true, message: 'Please select indicator!' }]">
          <Select v-model:value="config.form.indicator_id" placeholder="Please indicator" :show-search="true"
            :allow-clear="true">
            <SelectOption v-for="i in theoryOfChangeStore.indicatorGroups" :value="i.id" :key="i.id"> {{
              i.name }}
            </SelectOption>
          </Select>
        </FormItem>
      </Form>

    </Spin>
  </Modal>
</template>
