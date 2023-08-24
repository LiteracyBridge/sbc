<script setup lang="ts">
import { Button, Space } from "ant-design-vue";
import { computed, ref } from "vue";

import BroadcastModal from "./BroadcastModal.vue";
import MessagesDrawer from "./MessagesDrawer.vue";
import { InboxOutlined, ShareAltOutlined } from "@ant-design/icons-vue";

const props = defineProps<{
  module: string;
  direction?: "horizontal" | "vertical";
}>();

const config = ref({
  broadcastModal: false,
  messagesModal: false,
});

const layoutDirection = computed(() => props.direction || "vertical");
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
    class="buttons-container is-fixed is-absolute is-flex is-flex-direction-column is-align-items-flex-end"
  >
    <Space :direction="layoutDirection">
      <Button @click="config.broadcastModal = true">
        <ShareAltOutlined />
        Broadcast
      </Button>

      <Button @click.prevent="config.messagesModal = true">
        <InboxOutlined />
        Messages
      </Button>
    </Space>
  </div>
</template>
