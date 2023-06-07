import { defineStore } from "pinia";
import { useActivityStore } from "./activities";
import { downloadObjects } from "@/apis/lambda.js";

const init_objects = {
  interventions: { id: 0, name: "", text_short: "", text_long: "" },
};

export const useInterventionStore = defineStore({
  id: "interventions",
  state: () => ({
    interventions: [],
  }),
  getters: {
    interventionById: (state) => (interventionId) =>
      state.interventions.find((i) => i.id == interventionId),
    interventionNameById: (state) =>
      function (interventionId) {
        let name = "";
        const intervention = state.interventions.find(
          (i) => i.id == interventionId
        );
        if (intervention) {
          name = intervention.name;
        }
        return name;
      },
    interventionsByDriver: (state) => (driver) =>
      driver.intervention_ids
        ? state.interventions.filter((i) =>
            driver.intervention_ids.some((id) => id === i.id)
          )
        : null,
    activityIds: (state) =>
      function (interventionId) {
        const activityStore = useActivityStore();
        return activityStore.activities.reduce(
          (prev, current) =>
            current.intervention_id === interventionId
              ? prev.concat(current.id)
              : prev,
          []
        );
      },
  },
  actions: {
    clear() {
      for (const property of Object.keys(this.$state)) {
        this.$state[property] = [];
      }
    },
    download() {
      downloadObjects(init_objects, this, "lu_");
    },
  },
});
