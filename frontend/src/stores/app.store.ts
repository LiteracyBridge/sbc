// @ts-check

import { defineStore } from "pinia";
import { useTheoryOfChangeStore } from "./theory_of_change";
import { useProjectStore } from "./projects";
import { useLookupStore } from "./lookups";
import { ApiRequest } from "@/apis/api";
import { Activity, Project, Risk, TheoryOfChange } from "@/types";

export const AppStore = defineStore({
  id: "app_store",
  state: () => ({
    is_loading: true,
  }),
  getters: {
    isLoading: (state) => state.is_loading,
  },
  actions: {
    setLoading(loading: boolean) {
      this.$state.is_loading = loading;
    },
    async downloadObjects() {
      this.setLoading(true);

      return await useProjectStore()
        .download()
        .then(async () => {
          return await ApiRequest.get<{
            theory_of_change: TheoryOfChange[];
            activities: Activity[];
            project: Project;
            risks: Risk[];
          }>(`/bulk/${useProjectStore().prj_id}`).then(([resp]) => {
            useLookupStore().download();

            // TODO: refactor to save project store data
            // useProjectStore().current_project = resp.project;
            useTheoryOfChangeStore().theory_of_change = resp.theory_of_change;
            useTheoryOfChangeStore().risks = resp.risks;

            return;
          });
        })
        // return await useProjectStore()
        //   .download()
        //   .then(async () => {
        //     useLookupStore().download();
        //     await useTheoryOfChangeStore().download();
        //     return;
        //   })
        .finally(() => this.setLoading(false));
    },
  },
});
