import { defineStore } from "pinia";
import { useUserStore } from "./user";
import * as api from "../apis/lambda";
import { ApiRequest } from "@/apis/api";
import { Activity, Schedule } from "@/types";

const init_objects: { activities: Activity; schedules: Schedule } = {
  activities: new Activity(),
  schedules: new Schedule(),
};

export const useActivityStore = defineStore({
  id: "activities",
  state: () => ({
    activities: [],
    schedules: [],
  }),
  getters: {
    driverInActivities: (state) => (driverId: number) =>
      state.activities.filter((a) => a.driver_ids.includes(driverId)).length >
      0,
    activityById: (state) => (activityId: number) =>
      state.activities.find((a) => a.id == activityId),
    topLevelActivities: (state) =>
      state.activities.filter((a) => a.parent_id == null),
    subActivitiesByActivityId: (state) => (activityId: number) =>
      state.activities.filter((a) => a.parent_id == activityId),
    schedulesByActivityId: (state) => (activityId: number) =>
      state.schedules.filter((s) => s.activity_id == activityId),
    fromDate: (state) => (activityId: number) => {
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
    toDate: (state) => (activityId: number) => {
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
        (this.$state as any)[property] = [];
      }
    },
    download() {
      api.downloadObjects(init_objects, this, "", true);
    },

    async addActivity(activity: Activity) {
      delete activity.id;
      const table = "activities";
      // const newId = await api.insert(table, { ...activity }); //const newId = 99; //
      const resp = await ApiRequest.post("activity", { ...activity });
      console.warn("created activity");
      console.warn(resp);
      // activity.id = newId;
      this.activities.push(activity);
    },

    updateActivity(activity: Partial<Activity>) {
      // console.log(activity);
      let idx = this.activities.findIndex((a) => a.id == activity.id);
      this.activities.splice(idx, 1, activity);
      api.update("activities", activity.id, { ...activity });

      // TODO: implement updating activity via api
    },

    async deleteActivity(activityId: number, deleteChildren: boolean = false) {
      // find activity to be deleted
      const activity = this.activities.find((a) => a.id === activityId);

      // handle children of the to-be-deleted activity
      const children = this.activities.filter(
        (a) => a.parent_id === activityId
      );
      const deleteIds = [];
      deleteIds.push(activity);
      deleteIds.push(children);

      // console.log('deleteIds:');
      // console.log(deleteIds);
      const table = "activities";
      api.remove(table, deleteIds);
      if (deleteChildren)
        this.activities = this.activities.filter((a) => !children.includes(a));
      else children.forEach((c) => (c.parent_id = activity.parent_id));
      this.activities = this.activities.filter((a) => a != activity);
    },

    async deleteIntervention(interventionId: number) {
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
