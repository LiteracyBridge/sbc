import { defineStore } from "pinia";
import { downloadObjects } from "@/apis/lambda";
import { GenericLookup, LuIndiKit } from "@/types";
import { ApiRequest } from "@/apis/api";

type IndiKitData = Record<string, Record<string, LuIndiKit[]>>;
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
    access_types: [] as GenericLookup[],
    activity_status: [
      {
        id: 1,
        name: "proposed",
        sequence: 1,
      },
      {
        id: 2,
        name: "planned",
        sequence: 2,
      },
      {
        id: 3,
        name: "in progress",
        sequence: 3,
      },
      {
        id: 4,
        name: "completed",
        sequence: 4,
      },
    ],
    indikit: {} as IndiKitData,
    countries: [] as GenericLookup[],
    importance: [] as Array<{
      id: number;
      name: string;
      sequence: number;
      color: string;
    }>,
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
    indikitSectors: (state) => Object.keys(state.indikit),
    getSubSectors: (state) => (sector: string) => state.indikit[sector] || {},
  },
  actions: {
    // Downloads lookup data and sets it to the store state
    download() {
      return ApiRequest.get<{
        access_types: [];
        countries: [];
        indi_kit: IndiKitData;
        importance: [];
      }>("lu").then((resp) => {
        const data = resp[0];
        this.$state.countries = data.countries;
        this.$state.access_types = data.access_types;
        this.$state.importance = data.importance;
        this.$state.indikit = data.indi_kit;
      });
    },
  },
});
