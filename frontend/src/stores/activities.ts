import { defineStore } from "pinia";
import { useUserStore } from "./user";
import * as api from "../apis/lambda";
import { ApiRequest } from "@/apis/api";
import { Activity, Schedule } from "@/types";
import { useProjectStore } from "./projects";
import { message } from "ant-design-vue";

const init_objects: { activities: Activity; schedules: Schedule } = {
  activities: new Activity(),
  schedules: new Schedule(),
};

export const useActivityStore = defineStore({
  id: "activities",
  state: () => ({
    activities: [] as Activity[],
    schedules: [],
    isLoading: false,
  }),
  getters: {
    driverInActivities: (state) => (driverId: number) =>
      state.activities.filter((a) => a.driver_ids.includes(driverId)).length >
      0,
    activityById: (state) => (activityId: number) =>
      state.activities.find((a) => a.id == activityId),
    topLevelActivities: (state) =>
      state.activities.filter((a) => a.parent_id == null),
    totalSubActivities: (state) => {
      return state.activities.filter((a) => a.parent_id != null).length;
    },
    subActivitiesByActivityId: (state) => (activityId: number) =>
      state.activities.filter((a) => a.parent_id == activityId) ?? [],
    schedulesByActivityId: (state) => (activityId: number) =>
      state.schedules.filter((s) => s.activity_id == activityId) ?? [],
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
      this.$state.isLoading = true;
      ApiRequest.get<Activity>(`activity/${useProjectStore().prj_id}`)
        .then((resp) => {
          this.$state.activities = resp;
        })
        .catch((err) => message.error(err.message))
        .finally(() => (this.$state.isLoading = false));

      // api.downloadObjects(init_objects, this, "", true);
    },
    async updateOrCreate(activity: Activity): Promise<Activity | null> {
      activity.prj_id ??= useProjectStore().prj_id;
      activity.editing_user_id = useUserStore().id;

      this.$state.isLoading = true;
      return await ApiRequest.post<Activity>("activity/", {
        ...activity,
        is_task: activity.parent_id != null,
      })
        .then((resp) => {
          this.$state.activities = resp;
          message.success("Activity created successfully!");
          return resp;
        })
        .catch((err) => {
          message.error(err.message);
          return null;
        })
        .finally(() => (this.$state.isLoading = false));
    },

    // async updateActivity(activity: Partial<Activity>) {
    //   // console.log(activity);
    //   // TODO: implement updating activity via api
    //   let idx = this.activities.findIndex((a) => a.id == activity.id);
    //   api.update("activities", activity.id, { ...activity });
    //   this.activities.splice(idx, 1, activity as any);

    //   return activity;
    // },

    async deleteActivity(activityId: number) {
      this.$state.isLoading = true;
      return await ApiRequest.delete<Activity>(
        `activity/${useProjectStore().prj_id}/${activityId}`
      )
        .then((resp) => {
          this.$state.activities = resp;
          message.success("Activity deleted successfully!");
          return resp;
        })
        .catch((err) => {
          message.error(err.message);
          throw err;
        })
        .finally(() => (this.$state.isLoading = false));
    },

    async deleteIntervention(interventionId: number) {
      const activity = this.activities.find(
        (i) => i.intervention_id == interventionId
      );

      if (activity == null) {
        message.error("An activity with this intervention does not exist!");
        return;
      }

      return this.deleteActivity(activity.id);
    },
  },
});
