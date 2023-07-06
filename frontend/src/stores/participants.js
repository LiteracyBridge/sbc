import { defineStore } from "pinia";
import { downloadObjects } from "@/apis/lambda.js";

// Initial objects for participant data structure
const init_objects = {
  participants: {
    id: 0,
    prj_id: 0,
    editing_user_id: 0,
    parent_id: 0,
    name: "",
    type_id: 0,
    language_id: 0,
    location_id: 0,
  },
};

export const useParticipantStore = defineStore({
  id: "participants",
  state: () => ({
    participants: [],
  }),
  getters: {
    participantById: (state) => (participantId) =>
      state.participants.find((p) => p.id == participantId),
    participantNameById: (state) => (participantId) => {
      let name = "";
      let p = state.participants.find((p) => p.id == participantId);
      if (p != null) {
        name = p.name;
      }
      return name;
    },
  },
  actions: {
    // Clears participant data in the store state
    clear() {
      for (const property of Object.keys(this.$state)) {
        this.$state[property] = [];
      }
    },
    // Downloads participant data and sets it to the store state
    async download() {
      return await downloadObjects(init_objects, this);
    },
  },
});
