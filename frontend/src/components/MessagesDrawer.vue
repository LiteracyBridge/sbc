<script setup lang="ts">
import { ref, reactive, onMounted, onBeforeUnmount, watch } from "vue";
import { onClickOutside } from "@vueuse/core";
import { useProjectStore } from "../stores/projects";
import { useMessageStore } from "../stores/messages";
import {
  Button,
  Comment,
  Empty,
  Space,
  Drawer,
  Avatar,
  Tooltip,
  Spin,
} from "ant-design-vue";
import { UserOutlined } from "@ant-design/icons-vue";
import dayjs from "dayjs";
import { ApiRequest } from "@/apis/api";
import { MessageSent } from "@/types";

const emit = defineEmits(["close"]);

const props = defineProps({
  topic: {
    type: String,
    required: true,
  },
  visible: {
    type: Boolean,
    required: true,
  },
});

const projectStore = useProjectStore();
const config = ref({
  visible: props.visible,
  loading: false,
  messages: [] as MessageSent[],
});

const closeButton = () => {
  config.value.visible = false;
  emit("close", false);
};

function flattenMessage(message: any): any {
  return {
    ...message,
    replies: Object.values(message.replies ?? {}).map((r) => flattenMessage(r)),
  };
}

function fetchMessages() {
  config.value.loading = true;

  ApiRequest.get<MessageSent>(
    `twilio?prj_id=${useProjectStore().prj_id}&related_item=${props.topic}`
  )
    .then((resp) => {
      console.log(resp);
      config.value.messages = resp;
    })
    .finally(() => (config.value.loading = false));

  // useMessageStore()
  //   .getLatestMessages(props.topic, {})
  //   .then((resp) => {
  //     config.value.messages = Object.values(resp).map((val) => flattenMessage(val));
  //     console.log(resp);
  //     // messages = useMessageStore().messages;
  //   })
  //   .finally(() => (config.value.loading = false));
}

watch(props, (newProps) => {
  config.value.visible = newProps.visible;
  fetchMessages();
});

onMounted(() => {
  fetchMessages();
});
</script>

<template>
  <Drawer
    :visible="config.visible"
    @close="closeButton"
    @keydown.esc="closeButton"
    @cancel="closeButton"
    width="40vw"
    title="Messages"
  >
    <template #extra>
      <Space>
        <Button @click="fetchMessages()" :loading="config.loading" type="primary"
          >Refresh</Button
        >

        <Button @click="closeButton">Close</Button>
      </Space>
    </template>

    <Spin :spinning="config.loading">
      <Empty v-if="config.messages?.length == 0" description="No messages yet." />

      <div v-else>
        <Comment v-for="(message, dx) in config.messages" :key="message.id">
          <template #datetime>
            <Tooltip :title="dayjs().format('YYYY-MM-DD HH:mm:ss')">
              <span>{{ dayjs(message.sent_time) }}</span>
            </Tooltip>
          </template>

          <!-- <template #actions>
        <span key="comment-nested-reply-to">Reply to</span>
      </template> -->
          <template #author>
            {{ message.user?.address_as || message.user?.name }},
          </template>

          <template #avatar>
            <Avatar>
              <template #icon>
                <UserOutlined></UserOutlined>
              </template>
            </Avatar>
          </template>

          <template #content>
            <p>
              {{ message.message }}
            </p>
          </template>

          <!-- Message replies -->
          <Comment
            v-for="reply in (message.replies || []).filter(
              (r) => r.message.toLowerCase() != 'yes - send update'
            )"
            :key="reply.id"
          >
            <template #datetime>
              <Tooltip :title="dayjs().format('YYYY-MM-DD HH:mm:ss')">
                <span>{{ dayjs(reply.created_at) }}</span>
              </Tooltip>
            </template>

            <template #author>
              {{ reply.user?.address_as || reply.user?.name || reply.stakeholder?.name }},
            </template>

            <template #avatar>
              <Avatar>
                <template #icon>
                  <UserOutlined></UserOutlined>
                </template>
              </Avatar>
            </template>

            <template #content>
              <p>
                {{ reply.message }}
              </p>
            </template>
          </Comment>
        </Comment>
      </div>
    </Spin>
  </Drawer>
</template>

<style>
.text-with-line-breaks {
  white-space: pre-line;
}
</style>
