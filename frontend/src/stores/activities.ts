import { defineStore } from "pinia";
import { useUserStore } from "./user";
import * as api from "../apis/lambda";
import { ApiRequest } from "@/apis/api";

export class Activity {
  id: number;
  name: string;
  project_id: number;
  prj_id: number;
  intervention_id: number;
  parent_id: number;
  editing_user_id: number;
  toc_indicator_id: number;
  owner_id: number;
  status_id: number;
  notes: string = "";
  url: string = "";

  driver_ids: number[] = [];
}

const init_objects = {
  activities: {
    id: 0,
    name: "",
    parent_id: 0,
    intervention_id: 0,
    driver_ids: [],
    editing_user_id: 0,
    owner_id: 0,
    status_id: 0,
    notes: "",
    url: "",
  },
  schedules: {
    id: 0,
    editing_user_id: 0,
    activity_id: 0,
    planned_date_from: new Date(2007, 9, 26),
    planned_date_to: new Date(2022, 9, 26),
    actual_date_from: new Date(2007, 9, 26),
    actual_date_to: new Date(2022, 9, 26),
    dependency_ids: [],
    owner_id: 0,
    participant_id: 0,
    status_id: 0,
    notes: "",
    url: "",
  },
};

export const useActivityStore = defineStore({
  id: "activities",
  state: () => ({
    activities: [],
    schedules: [],
  }),
  getters: {
    driverInActivities: (state) => (driverId) =>
      state.activities.filter((a) => a.driver_ids.includes(driverId)).length >
      0,
    activityById: (state) => (activityId) =>
      state.activities.find((a) => a.id == activityId),
    topLevelActivities: (state) =>
      state.activities.filter((a) => a.parent_id == null),
    subActivitiesByActivityId: (state) => (activityId) =>
      state.activities.filter((a) => a.parent_id == activityId),
    schedulesByActivityId: (state) => (activityId) =>
      state.schedules.filter((s) => s.activity_id == activityId),
    fromDate: (state) => (activityId) => {
      const schedules = state.schedules.filter(
        (s) => s.activity_id == activityId
      );
      let date = "";
      if (schedules.length > 0) {
        date = schedules.reduce((prev, cur) =>
          cur.planned_date_from < prev.planned_date_from ? cur : prev
        ).planned_date_from;
      }
      return date;
    },
    toDate: (state) => (activityId) => {
      const schedules = state.schedules.filter(
        (s) => s.activity_id == activityId
      );
      let date = "";
      if (schedules.length > 0) {
        date = schedules.reduce((prev, cur) =>
          cur.planned_date_to > prev.planned_date_to ? cur : prev
        ).planned_date_to;
      }
      return date;
    },
  },
  actions: {
    clear() {
      for (const property of Object.keys(this.$state)) {
        this.$state[property] = [];
      }
    },
    download() {
      api.downloadObjects(init_objects, this, "", true);
    },

    async addActivity(activity) {
      delete activity.id;
      const table = "activities";
      // const newId = await api.insert(table, { ...activity }); //const newId = 99; //
      const resp = await ApiRequest.post("activity", { ...activity });
      console.warn("created activity");
      console.warn(resp);
      // activity.id = newId;
      this.activities.push(activity);
    },

    updateActivity(activity) {
      // console.log(activity);
      let idx = this.activities.findIndex((a) => a.id == activity.id);
      this.activities.splice(idx, 1, activity);
      api.update("activities", activity.id, { ...activity });
    },

    async deleteActivity(activityId, deleteChildren = false) {
      // find activity to be deleted
      const activity = this.activities.find((a) => a.id === activityId);

      // handle children of the to-be-deleted activity
      const children = this.activities.filter(
        (a) => a.parent_id === activityId
      );
      const deleteIds = [].push(activity).push(children);
      // console.log('deleteIds:');
      // console.log(deleteIds);
      const table = "activities";
      api.remove(table, deleteIds);
      if (deleteChildren)
        this.activities = this.activities.filter((a) => !children.includes(a));
      else children.forEach((c) => (c.parent_id = activity.parent_id));
      this.activities = this.activities.filter((a) => a != activity);
    },

    async deleteIntervention(interventionId) {
      // Delete an activity from an intervention id ONLY IF:
      //    - it has no schedules
      //    - it has no notes
      //    - it has no child activities
      // If these conditions are not met, return false.  deleteActivity() should be used instead.

      // find all activities linked to the intervention
      const removeActivities = this.activities.filter(
        (a, idx, arr) =>
          a.intervention_id === interventionId &&
          this.schedules.filter((s) => s.activity_id == a.id).length == 0 &&
          (!a.notes || a.notes == "") &&
          !arr.filter((b) => b.parent_id == a.id).length
      );
      const deleteIds = removeActivities.map((a) => a.id);
      // console.log('deleteIds:');
      // console.log(deleteIds);
      const table = "activities";
      api.remove(table, deleteIds);

      this.activities = this.activities.filter(
        (a) => !removeActivities.includes(a)
      );
    },
  },
});
