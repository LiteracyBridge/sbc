<script lang="ts" setup>

import { ref, reactive, watch } from "vue";
import { useActivityStore } from "../stores/activities";
import { useLookupStore } from "../stores/lookups";
import { useProjectStore } from "../stores/projects";
import { useInterventionStore } from "../stores/interventions";
import { useDriverStore } from "../stores/drivers"
import { useUserStore } from "@/stores/user";
import { useParticipantStore } from "../stores/participants";
import { Button, Col, Form, FormItem, Input, Modal, Row, Select, SelectOption, type FormInstance, Textarea } from "ant-design-vue";
import { Activity } from "@/types";


const props = defineProps<{ draftActivity: Activity, modelValue: boolean }>();

const activityStore = useActivityStore();
const userStore = useUserStore();
const lookupStore = useLookupStore();
const projectStore = useProjectStore();
const interventionStore = useInterventionStore();
const participantStore = useParticipantStore();
const driverStore = useDriverStore();

const driverValues = ref(props.draftActivity.driver_ids);
const driverOptions = ref(driverStore.driversInProject);
const formRef = ref<FormInstance>();

const emit = defineEmits(["update:modelValue", "save"]);

const cancelButton = () => {
  formRef.value.resetFields();
  emit("update:modelValue", false);
};

const saveForm = () => {
  formRef.value
    .validateFields()
    .then(values => {
      props.draftActivity.driver_ids = [...driverValues.value];

      // Update editing user
      props.draftActivity.editing_user_id = userStore.user.id;

      // Set project id
      if (props.draftActivity.prj_id == null) {
        props.draftActivity.prj_id = projectStore.projectId;
      }

      if (props.draftActivity.id == null) {
        activityStore.addActivity(props.draftActivity);
      } else {
        activityStore.updateActivity(props.draftActivity);
      }
      emit("update:modelValue", false);
    });
};

</script>

<template>
  <Modal v-model:visible="props.modelValue" @cancel="cancelButton()" width="750px" ok-text="Save" cancel-text="Cancel"
    :mask-closable="false" @ok="saveForm">
    <template #title>
      <!-- TODO: show add/update activity depending on item state -->
      <span>Add Activity</span>
    </template>

    <template #footer>
      <Button @click="cancelButton()" type="ghost">Cancel</Button>
      <Button @click="saveForm" type="primary">Save</Button>
    </template>

    <Form name="activity-form" ref="formRef" :model="draftActivity" layout="vertical">

      <Row :gutter="6">
        <Col :span="12">
        <FormItem label="Name" name="name" :rules="[{ required: true, message: 'Please activity name!' }]">
          <Input v-model:value="draftActivity.name" />
        </FormItem>
        </Col>

        <Col :span="12">
        <FormItem name="owner_id" label="Owner" has-feedback
          :rules="[{ required: true, message: 'Please select an owner!' }]">
          <Select v-model:value="draftActivity.owner_id" placeholder="Select owner" :show-search="true">
            <SelectOption v-for="user in projectStore.users_in_project" :value="user.user_id" :key="user.user_id">{{
              user.name }}</SelectOption>
          </Select>
        </FormItem>
        </Col>
      </Row>

      <Row :gutter="6">
        <Col :span="12">
        <FormItem name="parent_id" label="Group Parent" has-feedback
          :rules="[{ required: true, message: 'Please select a group parent!' }]">

          <Select v-model:value="draftActivity.parent_id" placeholder="Select group" :show-search="true">
            <SelectOption :value="null">Not part of a group</SelectOption>

            <SelectOption v-for="activity in activityStore.activities.filter((a) => a.id != draftActivity.id)"
              :value="activity.id" :key="activity.id">
              {{ activity.name }}
            </SelectOption>
          </Select>

        </FormItem>
        </Col>

        <Col :span="12">
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
        </Col>
      </Row>

      <FormItem name="driverValues" label="Supported Drivers" has-feedback :rules="[{ required: false }]">

        <Select v-model:value="driverValues" placeholder="Please owner" :show-search="true" mode="multiple">
          <SelectOption v-for="i in driverOptions" :value="i.id" :key="i.id">
            {{ i.name }}
          </SelectOption>

        </Select>
      </FormItem>

      <Row :gutter="6">
        <Col :span="12">
        <FormItem name="status_id" label="Activity status" has-feedback
          :rules="[{ required: true, message: 'Please select an activity status!' }]">

          <Select v-model:value="draftActivity.status_id" placeholder="Select activity status" :show-search="true">
            <SelectOption :value="null">None</SelectOption>
            <SelectOption v-for="status in lookupStore.activity_status" :value="status.id" :key="status.id">
              {{ status.name }}
            </SelectOption>

          </Select>
        </FormItem>
        </Col>

        <Col :span="12">
        <FormItem name="url" label="URL" has-feedback :rules="[{ required: false }]">

          <Input type="url" v-model:value="draftActivity.url"></Input>
        </FormItem>
        </Col>
      </Row>


      <Row :gutter="6">

        <Col :span="24">
        <FormItem name="notes" label="Notes" has-feedback :rules="[{ required: false }]">

          <Textarea v-model:value="draftActivity.notes" :rows="3"></Textarea>
        </FormItem>
        </Col>

      </Row>

      <table class="table">
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
          <template v-for="(schedule, i) in activityStore.schedulesByActivityId(draftActivity.id)">
            <tr :class="(i % 2) ? 'has-background-white' : 'has-background-light'">
              <td>{{ schedule.id }}</td>
              <td>{{ schedule.planned_date_from }}</td>
              <td>{{ schedule.planned_date_to }}</td>
              <td><!--{{schedule.owner_id}}-->
                <div class="control">
                  <div class="select">
                    <select v-model="schedule.owner_id">
                      <option v-for="user in projectStore.users_in_project" :value="user.user_id" :key="user.user_id">
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
                      <option v-for="status in lookupStore.activity_status" :value="status.id" :key="status.id">
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
                      <option v-for="participant in participantStore.participants" :value="participant.id"
                        :key="participant.id">
                        {{ participant.name }}
                      </option>
                    </select>
                  </div>
                </div>
              </td>
            </tr>
            <tr :class="(i % 2) ? 'has-background-white' : 'has-background-light'">
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
  </Modal>
</template>
