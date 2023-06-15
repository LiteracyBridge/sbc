import { defineStore } from "pinia";
import { ApiRequest } from "@/apis/api";
import {
  Activity,
  Schedule,
  TheoryOfChange,
  IndicatorGroup,
  IndicatorType,
  LuIndiKit,
  ProjectIndicator,
} from "@/types";
import { useProjectStore } from "./projects";
import { message } from "ant-design-vue";

export const useTheoryOfChangeStore = defineStore({
  id: "theory_of_change",
  state: () => ({
    theory_of_change: [] as TheoryOfChange[],
    project_indicators: [] as ProjectIndicator[],
    indicator_groups: [] as IndicatorGroup[],
    indicator_types: [] as IndicatorType[],
    isLoading: false,
  }),
  getters: {
    indicatorTypes: (state) => state.indicator_types,
    indicatorGroups: (state) => state.indicator_groups,
  },
  actions: {
    clear() {
      this.$state.theory_of_change = [] as TheoryOfChange[];
    },
    async fetchIndiKit() {
      this.$state.isLoading = true;
      return await ApiRequest.get<LuIndiKit>("lu/indi-kit")
        .then((resp) => (this.$state.indicator_types = resp))
        .catch((err) => message.error(err.message))
        .finally(() => (this.$state.isLoading = false));
    },
    async fetchIndicators() {
      this.$state.isLoading = true;
      return await ApiRequest.get<ProjectIndicator>(
        `theory-of-change/${useProjectStore().prj_id}/indicators`
      )
        .then((resp) => (this.$state.project_indicators = resp))
        .catch((err) => message.error(err.message))
        .finally(() => (this.$state.isLoading = false));
    },
    async saveIndicators(opts: {
      tocItemId: number;
      added: number[] | string[];
      removed: number[] | string[];
    }) {
      this.$state.isLoading = true;
      return ApiRequest.post<TheoryOfChange>(
        `theory-of-change/${opts.tocItemId}/indicators`,
        { added: opts.added, removed: opts.removed }
      )
        .then((resp) => {
          this.theory_of_change = resp;
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
    async download() {
      return await Promise.all([
        this.fetchIndicators(),
        this.fetchTheoryOfChange(),
        this.fetchIndiKit(),
      ]);
    },
  },
});
