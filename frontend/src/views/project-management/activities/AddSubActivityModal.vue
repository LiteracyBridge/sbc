<script lang="ts" setup>

import { computed, ref, watch } from "vue";
import  dayjs from "dayjs";
import  type {Dayjs} from "dayjs";
import { useActivityStore } from "@/stores/activities";
import { useLookupStore } from "@/stores/lookups";
import { useProjectStore } from "@/stores/projects";
import { useInterventionStore } from "@/stores/interventions";
import { useDriverStore } from "@/stores/drivers"
import { useUserStore } from "@/stores/user";
import { useParticipantStore } from "@/stores/participants";
import { Button, Col, Form, FormItem, Input, Modal, Row, Select, SelectOption, type FormInstance, Textarea, Spin, DatePicker, RangePicker } from "ant-design-vue";
import { Activity } from "@/types";

const props = defineProps<{
  draftActivity: Activity,
  visible: boolean,
  parentActivity: Activity
}>();

const emit = defineEmits(["closed", "save"]);

const activityStore = useActivityStore();
const userStore = useUserStore();
const lookupStore = useLookupStore();
const projectStore = useProjectStore();
const participantStore = useParticipantStore();

const config = ref({
  visible: props.visible,
  duration: [dayjs(props.draftActivity?.start_date), dayjs(props.draftActivity.end_date)] as [Dayjs | null, Dayjs | null],
});

const driverValues = ref(props.draftActivity.driver_ids);
const taskFormRef = ref<FormInstance>();

/**
 * 'Activity' here means the item is a top-level activity
 * 'Task/sub activity' here means the item is a sub-activity
 */
const isActivity  = computed(() => props.draftActivity.parent_id == null && props.draftActivity.id != null);

const closeModal = () => {
  taskFormRef.value.resetFields();
  config.value.visible = false;
  emit("closed", true);
};

const saveForm = () => {
  taskFormRef.value
    .validateFields()
    .then(values => {
      // Update duration
      if(isActivity.value) {
        props.draftActivity.start_date = config.value.duration[0];
        props.draftActivity.end_date = config.value.duration[1];
      } else {
        props.draftActivity.parent_id ??= props.parentActivity.id;
      }

      props.draftActivity.driver_ids = [...driverValues.value];

      // Update editing user
      props.draftActivity.editing_user_id = userStore.user.id;

      // Set project id
      if (props.draftActivity.prj_id == null) {
        props.draftActivity.prj_id = projectStore.prj_id;
      }

      // if (props.draftActivity.id == null) {
        activityStore.updateOrCreate(props.draftActivity)
          .then((resp) => {
            console.log(resp)
            if (resp != null) closeModal();
          });
      // } else {
      //   // FIXME: test activity update
      //   activityStore.updateActivity(props.draftActivity)
      //     .then((resp) => {
      //       if (resp != null) closeModal();
      //     })
      // }
    });
};

watch(props, (newProps) => {
  config.value.visible = newProps.visible;

  config.value.duration = [
    dayjs(newProps.draftActivity.start_date),
    dayjs(newProps.draftActivity.end_date)
  ];
}, {deep: true});
</script>

<template>
  <Modal
    v-model:visible="config.visible"
    @cancel="closeModal()"
    width="750px"
    ok-text="Save"
    cancel-text="Cancel"
    :mask-closable="false"
    @ok="saveForm()"
  >
    <template #title>
      <!-- TODO: show add/update activity depending on item state -->
      <span>Add Task</span>
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

        <!-- <Row :gutter="6"> -->
        <!-- <Col :span="12">
        <FormItem name="parent_id" label="Group Parent" has-feedback
          :rules="[{ required: false, message: 'Please select a group parent!' }]">

          <Select v-model:value="draftActivity.parent_id" placeholder="Select group" :show-search="true">
            <SelectOption :value="null">Not part of a group</SelectOption>

            <SelectOption v-for="activity in activityStore.activities.filter((a) => a.id != draftActivity.id)"
              :value="activity.id" :key="activity.id">
              {{ activity.name }}
            </SelectOption>
          </Select>

        </FormItem>
        </Col> -->
        <!--
          <Col :span="12">
          <FormItem name="driverValues" label="Supported Drivers" has-feedback :rules="[{ required: false }]">

            <Select v-model:value="driverValues" placeholder="Please owner" :show-search="true" mode="multiple">
              <SelectOption v-for="i in driverOptions" :value="i.id" :key="i.id">
                {{ i.name }}
              </SelectOption>

            </Select>
          </FormItem>
          </Col> -->

        <!-- <Col :span="12">
          <FormItem name="intervention_id" label="Supported Intervention" has-feedback
            :rules="[{ required: false, message: 'Please select an intervention!' }]">

            <Select v-model:value="draftActivity.intervention_id" placeholder="Select intervention" :show-search="true"
              :allow-clear="true">
              <SelectOption :value="null">None</SelectOption>
              <SelectOption v-for="intervention in interventionStore.interventions" :value="intervention.id"
                :key="intervention.id">
                {{ intervention.name }}
              </SelectOption>

            </Select>
          </FormItem>
          </Col> -->
        <!-- </Row> -->

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

        <table
          class="table"
          v-if="activityStore.schedulesByActivityId(draftActivity.id)?.length > 0"
        >
          <thead>
            <tr>
              <th>ID</th>
              <th>From</th>
              <th>To</th>
              <th>Owner</th>
              <th>Status</th>
              <th>Participant</th>
            </tr>
          </thead>
          <tbody>
            <template
              v-for="(schedule, i) in activityStore.schedulesByActivityId(
                draftActivity.id
              )"
            >
              <tr :class="i % 2 ? 'has-background-white' : 'has-background-light'">
                <td>{{ schedule.id }}</td>
                <td>{{ schedule.planned_date_from }}</td>
                <td>{{ schedule.planned_date_to }}</td>
                <td>
                  <!--{{schedule.owner_id}}-->
                  <div class="control">
                    <div class="select">
                      <select v-model="schedule.owner_id">
                        <option
                          v-for="user in projectStore.users_in_project"
                          :value="user.user_id"
                          :key="user.user_id"
                        >
                          {{ user.name }}
                        </option>
                      </select>
                    </div>
                  </div>
                </td>
                <td>
                  <div class="control">
                    <div class="select">
                      <select v-model="schedule.status_id">
                        <option
                          v-for="status in lookupStore.activity_status"
                          :value="status.id"
                          :key="status.id"
                        >
                          {{ status.name }}
                        </option>
                      </select>
                    </div>
                  </div>
                </td>
                <td>
                  <div class="control">
                    <div class="select">
                      <select v-model="schedule.participant_id">
                        <option
                          v-for="participant in participantStore.participants"
                          :value="participant.id"
                          :key="participant.id"
                        >
                          {{ participant.name }}
                        </option>
                      </select>
                    </div>
                  </div>
                </td>
              </tr>
              <tr :class="i % 2 ? 'has-background-white' : 'has-background-light'">
                <td colspan="9"><input size="70" v-model="schedule.notes" /></td>
              </tr>
            </template>
          </tbody>
        </table>

        <!-- <div class="field is-grouped">
            <div class="control">
              <button class="button is-link">Submit</button>
            </div>
            <div class="control">
              <button class="button is-link is-light">Cancel</button>
            </div>
          </div>         -->

        <!-- <div class="field">
            <label class="label">Username</label>
            <div class="control has-icons-left has-icons-right">
              <input class="input is-success" type="text" placeholder="Text input" value="bulma">
              <span class="icon is-small is-left">
                <i class="fas fa-user"></i>
              </span>
              <span class="icon is-small is-right">
                <i class="fas fa-check"></i>
              </span>
            </div>
            <p class="help is-success">This username is available</p>
          </div> -->

        <!-- <div class="field">
            <label class="label">Email</label>
            <div class="control has-icons-left has-icons-right">
              <input class="input is-danger" type="email" placeholder="Email input" value="hello@">
              <span class="icon is-small is-left">
                <i class="fas fa-envelope"></i>
              </span>
              <span class="icon is-small is-right">
                <i class="fas fa-exclamation-triangle"></i>
              </span>
            </div>
            <p class="help is-danger">This email is invalid</p>
          </div> -->

        <!-- <div class="field">
            <div class="control">
              <label class="checkbox">
                <input type="checkbox">
                I agree to the <a href="#">terms and conditions</a>
              </label>
            </div>
          </div> -->

        <!-- <div class="field" v-if="activityStore.activities.length > 0">
            <div class="control">
              <label class="radio">Part of a group?
                <input v-model="child" type="radio" name="question" value="yes">
                Yes
              </label>
              <label class="radio">
                <input v-model="child" type="radio" name="question" value="no">
                No
              </label>
            </div>
          </div> -->
      </Form>
    </Spin>
  </Modal>
</template>
