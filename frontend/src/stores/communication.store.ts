import { defineStore } from "pinia";
import { useUserStore } from "./user";
import * as api from "../apis/lambda";
import { useProjectStore } from "./projects";
import { ApiRequest } from "@/apis/api";
import { Communication, ProjectData } from "@/types";
import { message } from "ant-design-vue";
import { useProjectDataStore } from "./projectData";

export const useCommunicationStore = defineStore({
  id: "communications",
  state: () => ({
    loading: false,
    data: [] as Communication[],
  }),
  getters: {
    projectObjectives: (state) => {
      return (communicationId: number): ProjectData[] => {
        const comm = state.data.filter((c) => c.id == communicationId);

        return useProjectDataStore().specificObjectives.filter((o) =>
          comm.some((c) =>
            c.project_objectives.some((p) => p.objective_id == o.id)
          )
        );
      };
    },
    targetAudiences: (state) => {
      return (communicationId: number): ProjectData[] => {
        const comm = state.data.filter((c) => c.id == communicationId);

        return useProjectDataStore().audiences.filter((o) =>
          comm.some((c) =>
            c.target_audiences.some((p) => p.audience_id == o.id)
          )
        );
      };
    },

  },
  actions: {
    async create(form: any) {
      this.$state.loading = true;
      return ApiRequest.post<Communication>(
        `communications/${useProjectStore().prj_id}`,
        form
      )
        .then((resp) => {
          this.$state.data = resp;

          message.success("Communication created successfully!");
          return resp;
        })
        .catch((err) => {
          message.error(err.message);
          throw err;
        })
        .finally(() => (this.$state.loading = false));
    },
    async download() {
      this.$state.loading = true;
      ApiRequest.get<Communication>(
        `communications/${useProjectStore().prj_id}`
      )
        .then((resp) => {
          this.$state.data = resp;
          return resp;
        })
        .catch((err) => {
          message.error(err.message);
          throw err;
        })
        .finally(() => (this.$state.loading = false));
    },
  },
});
