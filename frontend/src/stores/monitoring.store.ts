import { defineStore } from "pinia";
import { useProjectStore } from "./projects";
import { ApiRequest } from "@/apis/api";
import { Monitoring } from "@/types";
import { message } from "ant-design-vue";
import { useTheoryOfChangeStore } from "./theory_of_change";

export const useMonitoringStore = defineStore({
  id: "monitoring_store",
  state: () => ({
    loading: false,
    data: [] as Monitoring[],
  }),
  getters: {
    getIndicatorName: (state) => (monitoringId: number) => {
      const indicator = state.data.find((i) => i.id === monitoringId);
      return indicator ? indicator.toc_indicator?.indicator?.name : "";
    },
    getTheoryOfChange: (state) => (monitoringId: number) => {
      const indicator = state.data.find((i) => i.id === monitoringId);

      if (indicator == null) return null;

      return useTheoryOfChangeStore().getByTocId(
        indicator.toc_indicator?.theory_of_change_id
      );
    },
  },
  actions: {
    async create(tocId: number, form: any) {
      this.$state.loading = true;

      // TODO: rewrite adding monitoring item
      // useTheoryOfChangeStore().saveIndicators({
      //   tocItemId: config.value.form.toc_item_id,
      //   added: [config.value.form.indicator_id],
      //   removed: [],
      // })
      //   .then((_resp) => {
      //     message.success('Indicator added successfully!');
      //     emit('isUpdated', true);

      //     closeModal();
      //   })
      //   .catch((error) => {
      //     message.error(error.message);
      //   });
    },
    async download() {
      this.$state.loading = true;

      ApiRequest.get<Monitoring>(`monitoring/${useProjectStore().prj_id}`)
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
    async update(id: number, form: any) {
      this.$state.loading = true;
      return ApiRequest.put<Monitoring>(`monitoring/${id}`, form)
        .then((resp) => {
          message.success("Monitoring record updated successfully!");
          this.$state.data = resp;
          return resp;
        })
        .catch((error) => {
          message.error(error.message);
          throw error;
        })
        .finally(() => (this.$state.loading = false));
    },
    async recordProgress(id: number, form: any) {
      return ApiRequest.post<Monitoring>(`monitoring/${id}/evaluation`, form)
        .then((resp) => {
          message.success("Progress recorded successfully!");
          this.$state.data = resp;
          return resp;
        })
        .catch((error) => {
          message.error(error.message);
          throw error;
        })
        .finally(() => (this.$state.loading = false));
    },
    // async delete(communicationId: number) {
    //   this.$state.loading = true;
    //   return ApiRequest.delete<Communication>(
    //     `communications/${useProjectStore().prj_id}/${communicationId}`
    //   )
    //     .then((resp) => {
    //       this.$state.data = resp;
    //       message.success("Communication deleted successfully!");
    //       return resp;
    //     })
    //     .catch((err) => {
    //       message.error(err.message);
    //       throw err;
    //     })
    //     .finally(() => (this.$state.loading = false));
    // },
  },
});
