// @ts-check

import { defineStore } from "pinia";
import { useTheoryOfChangeStore } from "./theory_of_change";
import { useProjectStore } from "./projects";
import { useLookupStore } from "./lookups";

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
        .download().then(() => {

        })
        .then(() => useLookupStore().download())
        .then(() => useTheoryOfChangeStore().download())
        .finally(() => this.setLoading(false));
    },
  },
});
