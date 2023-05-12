// @ts-check

import { defineStore } from 'pinia';

export const AppStore = defineStore({
  id: 'app_store',
  state: () => ({
    is_loading: true,
  }),
  getters: {
    isLoading: (state) => state.is_loading,
  },
  actions: {
    /**
     * @param   {boolean}  loading
     * @return  {void}
     */
    setLoading(loading) {
      this.$state = { is_loading: loading };
    }
  },
});
