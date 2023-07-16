<script setup lang="ts">
import { Button, Space } from "ant-design-vue";
import { ref } from "vue";

import BroadcastModal from "./BroadcastModal.vue";
import MessagesDrawer from "./MessagesDrawer.vue";

const props = defineProps<{
  module: string;
}>();

const config = ref({
  broadcastModal: false,
  messagesModal: false,
});
</script>

<template>
  <BroadcastModal
    :visible="config.broadcastModal"
    :module="props.module"
    @close="config.broadcastModal = false"
  >
  </BroadcastModal>

  <MessagesDrawer
    v-if="config.messagesModal"
    :topic="props.module"
    :visible="config.messagesModal"
    @close="config.messagesModal = false"
  ></MessagesDrawer>

  <div
    class="buttons-container is-fixed is-absolute is-flex is-flex-direction-column is-align-items-flex-end m-4 mr-6"
  >
    <Space direction="vertical">
      <Button @click.prevent="config.broadcastModal = true" type="primary" :ghost="true">
        Broadcast
      </Button>

      <Button @click.prevent="config.messagesModal = true" type="primary" :ghost="true">
        Messages
      </Button>
    </Space>
  </div>
</template>
