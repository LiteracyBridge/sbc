<script setup lang="ts">
import { useProjectDataStore } from '@/stores/projectData';
import { Button, Modal, Spin } from 'ant-design-vue';
import { ref, watch } from 'vue';

const props = defineProps<{
  module: string;
  visible: boolean;
}>();
const emit = defineEmits<{
  (e: 'close'): void;
}>();

const store = useProjectDataStore();

const config = ref({
  visible: false,
})

function broadcast() {
  store.broadcastPage(props.module);
  emit('close');
}

function cancel() {
  config.value.visible = false;
  emit('close');
}

watch(props, (newProps) => {
  config.value.visible = newProps.visible
});

</script>

<template>
  <Modal title="Are you sure to broadcast this message?" :visible="config.visible" @cancel="cancel()">
    <template #footer>
      <Button type="primary" :danger="true" @click="broadcast()" :loading="store.loading">Broadcast</Button>
      <Button :disabled="store.loading" @click="cancel()">Cancel</Button>
    </template>

    <Spin :spinning="store.loading">
      <p class="preserve-whitespace">{{ store.buildBroadcastMessage(props.module) }}</p>
    </Spin>

  </Modal>
</template>
