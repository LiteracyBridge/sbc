<script lang="ts" setup>
import { useUserStore } from "@/stores/user";
import { InfoCircleOutlined, UserOutlined } from "@ant-design/icons-vue";
import { Modal , Spin, Form, type FormInstance,
   FormItem, Row, Col, Input,
    Avatar,
Tooltip} from "ant-design-vue";
import { ref, watch } from "vue";

const props = defineProps<{
  visible: boolean;
}>();
const emit = defineEmits<{ (e: "close"): void }>();

const store = useUserStore();

const config = ref({
  visible: false,
  loading: false,
});
const profileForm = ref<FormInstance>();
const labelColSpan = {span: 8}

function closeModal() {
  config.value.visible = false;
  emit("close");
}

function updateProfile() {
  config.value.loading = true;
  store.updateProfile().then(() => {
    config.value.loading = false;
    closeModal();
  });
}

watch(props, (newProps)=> {
  config.value.visible = newProps.visible;
});
</script>

<template>
  <Modal
    v-model:visible="config.visible"
    title="Update Profile"
    @cancel="closeModal()"
    ok-text="Update Profile"
    cancel-text="Cancel"
    width="720px"
    :mask-closable="false"
    @ok="updateProfile()"
  >
    <Spin :spinning="config.loading">
      <Row :gutter="8">
        <Col :span="7">
          <Avatar :size="128" style="margin: 0 auto; display: block">
            <template #icon>
              <UserOutlined />
            </template>
          </Avatar>
        </Col>

        <Col :span="17">
          <Form
            name="profileForm"
            ref="profileForm"
            :model="store.$state"
            layout="horizontal"
          >
            <FormItem label="Email" name="email" :label-col="labelColSpan" :colon="false">
              <Input v-model:value="store.user.email" :disabled="true" />
            </FormItem>

            <FormItem
              label="Full Name"
              name="name"
              :rules="[{ required: true, message: 'Full name is required!' }]"
              :label-col="labelColSpan"
              :colon="false"
            >
              <Input v-model:value="store.user.name" />
            </FormItem>

            <FormItem
              label="Address As"
              name="address_as"
              :rules="[{ required: false, message: 'Full name is required!' }]"
              :label-col="labelColSpan"
              :colon="false"
            >
              <Input v-model:value="store.user.address_as">
                <template #suffix>
                  <Tooltip
                    title="This is the name that will be used to address you in the project."
                  >
                    <InfoCircleOutlined />
                  </Tooltip>
                </template>
              </Input>
            </FormItem>

            <FormItem
              label="SMS Phone Number"
              name="sms"
              :label-col="labelColSpan"
              :colon="false"
            >
              <Input v-model:value="store.user.sms" type="tel">
                <template #suffix>
                  <Tooltip title="This number will be used to send you SMS notifications">
                    <InfoCircleOutlined />
                  </Tooltip>
                </template>
              </Input>
            </FormItem>

            <FormItem
              label="WhatsApp Number"
              name="whatsapp"
              :label-col="labelColSpan"
              :colon="false"
            >
              <Input v-model:value="store.user.whatsapp" type="tel">
                <template #suffix>
                  <Tooltip
                    title="This number will be used to send you Whatsapp notifications"
                  >
                    <InfoCircleOutlined />
                  </Tooltip>
                </template>
              </Input>
            </FormItem>
          </Form>
        </Col>
      </Row>
    </Spin>
  </Modal>
</template>
