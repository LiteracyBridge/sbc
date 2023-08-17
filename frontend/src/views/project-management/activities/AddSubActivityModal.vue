<script lang="ts" setup>
import { computed, ref, watch } from "vue";
import dayjs from "dayjs";
import type { Dayjs } from "dayjs";
import { useActivityStore } from "@/stores/activities";
import { useLookupStore } from "@/stores/lookups";
import { useProjectStore } from "@/stores/projects";
import { useInterventionStore } from "@/stores/interventions";
import { useDriverStore } from "@/stores/drivers";
import { useUserStore } from "@/stores/user";
import {
  Button,
  Col,
  Form,
  FormItem,
  Input,
  Modal,
  Row,
  Select,
  SelectOption,
  Textarea,
  Spin,
  DatePicker,
  RangePicker,
} from "ant-design-vue";
import type { FormInstance } from "ant-design-vue";
import { Activity } from "@/types";

const props = defineProps<{
  draftActivity: Activity;
  visible: boolean;
  parentActivity: Activity;
}>();

const emit = defineEmits(["closed", "save"]);

const activityStore = useActivityStore();
const userStore = useUserStore();
const lookupStore = useLookupStore();
const projectStore = useProjectStore();

const config = ref({
  visible: props.visible,
  duration: [
    dayjs(props.draftActivity?.start_date),
    dayjs(props.draftActivity.end_date),
  ] as [Dayjs | null, Dayjs | null],
});

const taskFormRef = ref<FormInstance>();

const isEditing = computed(() => props.draftActivity?.id != null);

/**
 * 'Activity' here means the item is a top-level activity
 * 'Task/sub activity' here means the item is a sub-activity
 */
const isActivity = computed(
  () => props.draftActivity.parent_id == null && props.draftActivity.id != null
);

const closeModal = () => {
  taskFormRef.value.resetFields();
  config.value.visible = false;
  emit("closed", true);
};

const saveForm = () => {
  taskFormRef.value.validateFields().then((values) => {
    // Update duration
    if (isActivity.value) {
      props.draftActivity.start_date = config.value.duration[0];
      props.draftActivity.end_date = config.value.duration[1];
    } else {
      props.draftActivity.parent_id ??= props.parentActivity.id;
    }

    // props.draftActivity.driver_ids = [...driverValues.value];

    // Update editing user
    props.draftActivity.editing_user_id = userStore.user.id;

    // Set project id
    if (props.draftActivity.prj_id == null) {
      props.draftActivity.prj_id = projectStore.prj_id;
    }

    activityStore.updateOrCreate(props.draftActivity).then((resp) => {
      console.log(resp);
      if (resp != null) closeModal();
    });
  });
};

watch(
  props,
  (newProps) => {
    config.value.visible = newProps.visible;

    config.value.duration = [
      dayjs(newProps.draftActivity.start_date),
      dayjs(newProps.draftActivity.end_date),
    ];
  },
  { deep: true }
);
</script>

<template>
  <Modal
    v-model:open="config.visible"
    @cancel="closeModal()"
    width="750px"
    ok-text="Save"
    cancel-text="Cancel"
    :mask-closable="false"
    @ok="saveForm()"
  >
    <template #title>
      <span
        >{{ isEditing ? "Update" : "Add" }} {{ isActivity ? "Activity" : "Task" }}</span
      >
    </template>

    <template #footer>
      <Button @click="closeModal()" type="ghost">Cancel</Button>
      <Button @click="saveForm()" type="primary">Save</Button>
    </template>

    <Spin :spinning="activityStore.isLoading">
      <Form
        name="activity-form"
        ref="taskFormRef"
        :model="draftActivity"
        layout="vertical"
      >
        <Row :gutter="6">
          <Col :span="12">
            <FormItem
              label="Task Name"
              name="name"
              :rules="[{ required: true, message: 'Please enter activity name!' }]"
            >
              <Input v-model:value="draftActivity.name" :disabled="isActivity" />
            </FormItem>
          </Col>

          <Col :span="12">
            <FormItem
              name="owner_id"
              label="Owner"
              has-feedback
              :rules="[{ required: true, message: 'Please select an owner!' }]"
            >
              <Select
                v-model:value="draftActivity.owner_id"
                placeholder="Select owner"
                :show-search="true"
              >
                <SelectOption
                  v-for="user in projectStore.users_in_project"
                  :value="user.user_id"
                  :key="user.user_id"
                  >{{ user.name }}</SelectOption
                >
              </Select>
            </FormItem>
          </Col>
        </Row>

        <Row :gutter="6">
          <Col :span="12">
            <FormItem
              name="status_id"
              label="Task Status"
              has-feedback
              :rules="[{ required: true, message: 'Please select an activity status!' }]"
            >
              <Select
                v-model:value="draftActivity.status_id"
                placeholder="Select activity status"
                :show-search="true"
              >
                <SelectOption :value="null">None</SelectOption>
                <SelectOption
                  v-for="status in lookupStore.activity_status"
                  :value="status.id"
                  :key="status.id"
                >
                  {{ status.name }}
                </SelectOption>
              </Select>
            </FormItem>
          </Col>

          <Col :span="12" v-if="!isActivity">
            <FormItem
              name="end_date"
              label="Deadline"
              has-feedback
              :rules="[{ required: false }]"
            >
              <DatePicker type="date" v-model:value="draftActivity.end_date"></DatePicker>
            </FormItem>
          </Col>

          <Col :span="12" v-else>
            <FormItem
              name="duration"
              label="Duration"
              has-feedback
              :rules="[{ required: false }]"
            >
              <RangePicker
                v-model:value="config.duration"
                :allow-clear="true"
                :allow-empty="[true, true]"
              ></RangePicker>
            </FormItem>
          </Col>
        </Row>

        <Row :gutter="6">
          <Col :span="24">
            <FormItem
              name="notes"
              label="Notes"
              has-feedback
              :rules="[{ required: false }]"
            >
              <Textarea v-model:value="draftActivity.notes" :rows="3"></Textarea>
            </FormItem>
          </Col>
        </Row>
      </Form>
    </Spin>
  </Modal>
</template>
