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
    indi_kit_library: [] as LuIndiKit[],

    indicator_groups: [] as IndicatorGroup[],
    indicator_types: [] as IndicatorType[],
    isLoading: false,
  }),
  getters: {
    indicatorTypes: (state) => state.indicator_types,
    indicatorGroups: (state) => state.indicator_groups,

    // IndiKit Helpers
    getIndiKitItemById: (state) => {
      return (id: number) => state.indi_kit_library.find((i) => i.id == id);
    },
    indiKitSubSectors: (state) => {
      return (sector?: string | number): LuIndiKit[] => {
        if (sector == null) return [];

        if (isNaN(+sector)) {
          return state.indi_kit_library.filter((i) => i.sector == sector);
        }

        return state.indi_kit_library.filter((i) => i.id == +sector);
      };
    },
    indiKitSubSectorIndicators: (state) => {
      return (sector?: string | number): LuIndiKit[] => {
        if (sector == null) return [];

        if (isNaN(+sector)) {
          return state.indi_kit_library.filter((i) => i.sub_sector == sector);
        }

        return state.indi_kit_library.filter((i) => i.id == +sector);
      };
    },
  },
  actions: {
    async fetchIndiKit() {
      this.$state.isLoading = true;
      return await ApiRequest.get<LuIndiKit>("lu/indi-kit")
        .then((resp) => (this.$state.indi_kit_library = resp))
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
      tocId: number;
      data: {
        removed: number[];
        removed_custom: number[];
        added: Array<{ id?: number; name: string; indi_kit_id?: number }>;
      };
      // newCustomIndicators: Array<{ name: string; id?: number }>;

      // removed: number[] | string[];

      // added: number[] | string[];
      // removed: number[] | string[];
    }) {
      this.$state.isLoading = true;

      // if(opts.newCustomIndicators.length > 0) {
      //   // Create new custom indicators

      // }

      return ApiRequest.post<TheoryOfChange>(
        `theory-of-change/${opts.tocId}/indicators`,
        { ...opts.data }
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
