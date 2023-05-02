import { defineStore } from "pinia";

export const useSideNavStore = defineStore({
  id: "sideNav",

  state: () => ({
    visible: true,
  }),

  actions: {
    show() {
      this.visible = true;
    },

    hide() {
      this.visible = false;
    },

    toggle() {
      this.visible = !this.visible;
    },
  },
});
