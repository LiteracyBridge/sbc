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
    project_indicators: [] as ProjectIndicator[],
    indi_kit_library: [] as LuIndiKit[],

    indicator_groups: [] as IndicatorGroup[],
    indicator_types: [] as IndicatorType[],
    isLoading: false,
  }),
  getters: {
    data: (state) => state.theory_of_change,

    indicatorTypes: (state) => state.indicator_types,
    indicatorGroups: (state) => state.indicator_groups,
    // Theory of Change
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
    // IndiKit Helpers
    getIndiKitItemById: (state) => {
      return (id: number) => state.indi_kit_library.find((i) => i.id == id);
    },
    getIndiKitSectors: (state): string[] => {
      return uniqBy(state.indi_kit_library, "sector").flatMap((i) => i.sector);
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
          message.success("Indicators saved");
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
      return await Promise.all([
        this.fetchIndicators(),
        this.fetchTheoryOfChange(),
        this.fetchIndiKit(),
        this.fetchRisks(),
      ]);
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
