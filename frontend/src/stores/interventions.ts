import { defineStore } from "pinia";
import { useActivityStore } from "./activities";
import { downloadObject, downloadObjects } from "@/apis/lambda.js";
import { useDriverStore } from "./drivers";
import { useProjectStore } from "./projects";
import { ApiRequest } from "@/apis/api";

const init_objects = {
  interventions: { id: 0, name: "", text_short: "", text_long: "" },
};

export const useInterventionStore = defineStore({
  id: "interventions",
  state: () => ({
    interventions: [],
  }),
  getters: {
    interventionById: (state) => (interventionId: number) =>
      state.interventions.find((i) => i.id == interventionId),
    interventionNameById: (state) =>
      function (interventionId: number) {
        let name = "";
        const intervention = state.interventions.find(
          (i) => i.id == interventionId
        );
        if (intervention) {
          name = intervention.name;
        }
        return name;
      },
    interventionsByDriver: (state) => (driver: any) =>
      driver.intervention_ids
        ? state.interventions.filter((i) =>
            driver.intervention_ids.some((id: number) => id === i.id)
          )
        : null,
    activityIds: (state) =>
      function (interventionId: number) {
        const activityStore = useActivityStore();
        return activityStore.activities.reduce(
          (prev, current) =>
            current.intervention_id === interventionId
              ? prev.concat(current.id)
              : prev,
          []
        );
      },
    groupedByDrivers: (state) => {
      const $drivers = useDriverStore().drivers_in_prj;

      console.log($drivers);
    },
  },
  actions: {
    clear() {
      this.$state.interventions = [];
      // for (const property of Object.keys(this.$state)) {
      //   this.$state.[property] = [];
      // }
    },
    download() {
      downloadObjects(init_objects, this, "lu_");
    },
    // Download data
    downloadProjectDrivers() {
      ApiRequest.get(`project/drivers/${useProjectStore().prj_id}`).then(
        (drivers) => {
          console.warn("downloading project drivers");
          console.warn(drivers);
        }
      );
    },
  },
});
