import { defineStore } from "pinia";
import { downloadObjects } from "@/apis/lambda";
import { Country, LuIndiKit } from "@/types";
import { ApiRequest } from "@/apis/api";

// Initial objects for lookup data structure
// const init_objects = {
//   access_types: { id: 0, name: "" },
//   activity_status: { id: 0, name: "" },
//   countries: { id: 0, name: "" },
//   importance: { id: 0, name: "", color: "" },
//   library_types: { id: 0, name: "" },
//   participant_types: { id: 0, name: "" },
//   sem: { id: 0, name: "", description: "" },
//   toc_types: { id: 0, name: "", text_short: "", text_long: "" },
// };

export const useLookupStore = defineStore({
  id: "lookup",
  state: () => ({
    // access_types: [],
    // activity_status: [],
    indi_kits: [] as LuIndiKit[],
    countries: [] as Country[],
    // importance: [],
    // library_types: [],
    // participant_types: [],
    // sem: [],
    // toc_types: [],
  }),
  getters: {
    lookupNameById: (state) =>
      function (lookupName: string, id: number) {
        try {
          const obj = (state as any)[lookupName].find((a: any) => a.id == id);
          let name = "";
          if (obj != null) {
            name = obj.name;
          }
          return name;
        } catch (e) {
          console.log(e);
          return null;
        }
      },
  },
  actions: {
    // Downloads lookup data and sets it to the store state
    download() {
      return ApiRequest.get<{ access_types: []; countries: []; indi_kit: [] }>(
        "lu"
      ).then((resp) => {
        const data = resp[0];
        this.$state.countries = data.countries;
        this.$state.indi_kits = data.indi_kit;
      });
      // return downloadObjects(init_objects, this, "lu_");
    },
  },
});
