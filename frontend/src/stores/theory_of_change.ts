import { defineStore } from "pinia";
import { ApiRequest } from "@/apis/api";
import {
  TheoryOfChange,
  IndicatorGroup,
  IndicatorType,
  LuIndiKit,
  ProjectIndicator,
  Risk,
} from "@/types";
import { useProjectStore } from "./projects";
import { message } from "ant-design-vue";
import { uniqBy } from "lodash-es";

export const useTheoryOfChangeStore = defineStore({
  id: "theory_of_change",
  state: () => ({
    theory_of_change: [] as TheoryOfChange[],
    risks: [] as Risk[],
    isLoading: false,
  }),
  getters: {
    data: (state) => state.theory_of_change,
    getByTocId: (state) => {
      return (id: number) => state.theory_of_change.find((i) => i.id == id);
    },

    // Project Indicator
    getTocItemIndicators: (state) => {
      return (tocId: number) => {
        if (state.theory_of_change.length == 0) return [];

        if (tocId == null) return [];

        return (
          state.theory_of_change.find((i) => i.id == tocId)?.indicators ?? []
        ).flatMap((i) => {
          return {
            id: i.id,
            name: i?.name ?? i?.indikit?.name ?? "",
            indi_kit_id: i?.indikit_id,
          };
        });
      };
    },
    allTocIndicators: (state) => {
      return (
        state.theory_of_change?.flatMap((toc) => {
          return toc.indicators.flatMap((i) => {
            return {
              id: i.id,
              name: i?.name ?? i?.indikit?.name ?? "",
              indikit_id: i?.indikit_id,
            };
          });
        }) ?? []
      );
    },
  },
  actions: {
    async saveIndicators(opts: {
      tocId: number;
      data: Array<{
        id?: number;
        name: string;
        indikit_id?: number;
        is_new: boolean;
        is_deleted: boolean;
        is_updated?: boolean;
      }>;
    }) {
      this.$state.isLoading = true;

      return ApiRequest.post<TheoryOfChange>(
        `theory-of-change/${opts.tocId}/indicators`,
        { data: opts.data }
      )
        .then((resp) => {
          this.$state.theory_of_change = resp;
          return resp;
        })
        .catch((err) => {
          message.error(err.message);
          throw err;
        })
        .finally(() => (this.$state.isLoading = false));
    },
    async fetchTheoryOfChange() {
      this.$state.isLoading = true;
      return await ApiRequest.get<TheoryOfChange>(
        `theory-of-change/${useProjectStore().projectId}`
      )
        .then((resp) => {
          console.log(resp);
          this.$state.theory_of_change = resp;
        })
        .catch((err) => message.error(err.message))
        .finally(() => (this.$state.isLoading = false));
    },
    async fetchRisks() {
      this.$state.isLoading = true;
      return await ApiRequest.get<Risk>(
        `theory-of-change/${useProjectStore().projectId}/risks`
      )
        .then((resp) => {
          this.$state.risks = resp;
          return resp;
        })
        .catch((err) => message.error(err.message))
        .finally(() => (this.$state.isLoading = false));
    },
    async download() {
      return await Promise.all([this.fetchTheoryOfChange(), this.fetchRisks()]);
    },
    async saveRisk(form: any) {
      this.$state.isLoading = true;
      return await ApiRequest.post<Risk>(
        `theory-of-change/${useProjectStore().prj_id}/risks`,
        form
      )
        .then((resp) => {
          this.$state.risks = resp;
          message.success("Risk saved successfully!");
          return resp;
        })
        .catch((err) => {
          message.error(err.message);
          throw err;
        })
        .finally(() => (this.$state.isLoading = false));
    },
    async addTocItem(
      form: Partial<
        TheoryOfChange & {
          intervention_id: number;
          editing_user_id: number;
          driver_ids: number[];
          new_indicators: any[]
        }
      >
    ) {
      this.$state.isLoading = true;
      return ApiRequest.post<TheoryOfChange>(
        `theory-of-change/${useProjectStore().prj_id}/item`,
        form
      )
        .then((resp) => {
          this.$state.theory_of_change = resp;
          message.success(
            `Theory of change item ${
              form.id != null ? "updated" : "added"
            } successfully`
          );
          return resp;
        })
        .finally(() => (this.$state.isLoading = false));
    },
  },
});
