<script setup lang="ts">
import { Button } from 'ant-design-vue';
import { ref } from 'vue';

import BroadcastModal from './BroadcastModal.vue';
import MessageModal from './MessageModal.vue';

const props = defineProps<{
  module: string;
}>();

const config = ref({
  broadcastModal: false,
  messagesModal: false,
})
</script>

<template>
  <BroadcastModal :visible="config.broadcastModal" :module="props.module" @close="config.broadcastModal = false">
  </BroadcastModal>

  <div class="buttons-container is-fixed is-absolute is-flex is-flex-direction-column is-align-items-flex-end m-4 mr-6">
    <Button @click="config.broadcastModal = true">
      Broadcast
    </Button>

    <Button @click="config.messagesModal = true">
      Messages
    </Button>
  </div>

  <Suspense>
    <MessageModal v-if="config.messagesModal" :topic="props.module" v-model="config.messagesModal" />
  </Suspense>
</template>
