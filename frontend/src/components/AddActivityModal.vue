<script setup>
import { ref, reactive } from "vue";
import { onClickOutside } from "@vueuse/core";
import { useActivityStore } from "../stores/activities";
import { useLookupStore } from "../stores/lookups";
import { useProjectStore } from "../stores/projects";
import { useInterventionStore } from "../stores/interventions";
import { useDriverStore } from "../stores/drivers"
import Multiselect from '@vueform/multiselect'
import { useParticipantStore } from "../stores/participants";

const activityStore = useActivityStore();
const lookupStore = useLookupStore();
const projectStore = useProjectStore();
const interventionStore = useInterventionStore();
const participantStore = useParticipantStore();
const driverStore = useDriverStore();
const driverValues = ref(props.draftActivity.driver_ids);
const driverOptions = ref(driverStore.driversInProject);

const props = defineProps({
  draftActivity: {
    type: Object,
    required: true
  },
  modelValue: {
    type: Boolean,
    required: true,
  }
})

const emit = defineEmits(["update:modelValue", "save"]);

const cancelButton = () => {
  emit("update:modelValue", false);
};

const saveButton = () => {
  props.draftActivity.driver_ids = [...driverValues.value];
  if (props.draftActivity.id == null) {
    activityStore.addActivity(props.draftActivity);
  } else {
    activityStore.updateActivity(props.draftActivity);
  }
  emit("update:modelValue", false);
};

const modalRef = ref(null);
const child = ref(false);

onClickOutside(modalRef, cancelButton);
</script>

<template>
  <div class="modal is-active p-2">
    <div class="modal-background"></div>
    <div ref="modalRef" class="modal-card">
      <header class="modal-card-head">
        <p class="modal-card-title">Add Activity</p>
        <button @click="cancelButton" class="delete" aria-label="close"></button>
      </header>
      <section class="modal-card-body">
        <form>
          <div class="field">
            <label class="label">Name</label>
            <div class="control">
              <input v-model="draftActivity.name" class="input" type="text" placeholder="Text input">
            </div>
          </div>

          <div class="field">
            <label class="label">Owner</label>
            <div class="control">
              <div class="select">
                <select v-model="draftActivity.owner_id">
                  <option
                    v-for="user in projectStore.users_in_project"
                    :value="user.user_id"
                    :key="user.user_id">
                    {{user.name}}
                  </option>
                </select>
              </div>
            </div>
          </div>

          <div class="field">
            <label class="label">Status</label>
            <div class="control">
              <div class="select">
                <select v-model="draftActivity.status_id">
                  <option
                    v-for="status in lookupStore.activity_status"
                    :value="status.id"
                    :key="status.id">
                    {{status.name}}
                  </option>
                </select>
              </div>
            </div>
          </div>

          <div class="field">
            <label class="label">Group Parent</label>
            <div class="control">
              <div class="select">
                <select v-model="draftActivity.parent_id">
                  <option :value="null">Not part of a group</option>
                  <option
                    v-for="activity in activityStore.activities.filter((a)=>a.id != draftActivity.id)"
                    :value="activity.id"
                    :key="activity.id">
                        {{activity.name}}
                  </option>
                </select>
              </div>
            </div>
          </div>

          <div class="field">
            <label class="label">Supported Intervention</label>
            <div class="control">
              <div class="select">
                <select v-model="draftActivity.intervention_id">
                  <option :value="null">None</option>
                  <option
                    v-for="intervention in interventionStore.interventions"
                    :value="intervention.id"
                    :key="intervention.id">
                    {{intervention.name}}
                  </option>
                </select>
              </div>
            </div>
          </div>

          <div>
            <label class="label">Supported Drivers</label>
            <Multiselect
              v-model="driverValues"
              :options="driverOptions"
              mode="tags"
              valueProp="id"
              nameProp="name"
              label="name"
              placeholder=""
            />
          </div>

          <div class="field">
            <label class="label">Notes</label>
            <div class="control">
              <textarea v-model="draftActivity.notes" class="textarea" placeholder="Textarea"></textarea>
            </div>
          </div>

          <div class="field">
            <label class="label">URL</label>
            <div class="control">
              <input v-model="draftActivity.url" class="input" type="text" placeholder="Text input">
            </div>
          </div>
          <hr/>
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
              <template v-for="(schedule,i) in activityStore.schedulesByActivityId(draftActivity.id)">
                <tr :class="(i % 2) ? 'has-background-white' : 'has-background-light'">
                  <td>{{schedule.id}}</td>
                  <td>{{schedule.planned_date_from}}</td>
                  <td>{{schedule.planned_date_to}}</td>
                  <td><!--{{schedule.owner_id}}-->
                    <div class="control">
                      <div class="select">
                        <select v-model="schedule.owner_id">
                          <option
                            v-for="user in projectStore.users_in_project"
                            :value="user.user_id"
                            :key="user.user_id">
                            {{user.name}}
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
                            :key="status.id">
                            {{status.name}}
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
                            :key="participant.id">
                            {{participant.name}}
                          </option>
                        </select>
                      </div>
                    </div>
                  </td>
                </tr>
                <tr :class="(i % 2) ? 'has-background-white' : 'has-background-light'">
                  <td colspan="9"><input size="70" v-model="schedule.notes"/></td>
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


        </form>
      </section>
      <footer class="modal-card-foot is-justify-content-flex-end">
        <button @click="cancelButton" class="button">Cancel</button>
        <button @click="saveButton" class="button is-success">Save</button>
      </footer>
    </div>
  </div>
</template>
