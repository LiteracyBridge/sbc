
import { defineStore } from "pinia";
import * as api from "@/apis/lambda.js";
import { useProjectStore } from "./projects.js";

export const useUserStore = defineStore({
  id: "user",
  state: () => ({
    id: null,
    email: null,
    name: null,
    address_as: null,
    last_project_id: null,
  }),
  getters: {
    firstName: (state) => (state.name ? state.name.split(" ")[0] : ""),
    loggedIn: (state) => !(state.email == null),
    user: (state) => state,
  },
  actions: {
    // Update the last_project_id for the user and call API to update the database
    async setLastProject(last_project_id) {
      this.last_project_id = last_project_id;
      const response = api.update("users", this.id, { last_project_id });
    },

    async fetchUser(email) {},

    // Set the user details based on email and token, if provided
    async setUser(email = null, token = null) {
      this.email = email;
      if (email == null) {
        this.id = null;
        this.name = null;
        this.address_as = null;
        this.last_project_id = null;
      } else {
        // Query user details from the database
        const response = await api.downloadObject(
          "users",
          ["id", "name", "address_as", "last_project_id"],
          "email=" + this.email
        );

        // Check whether there's a match for the user's email
        if (response.length > 0) {
          // At least one user with that email address (hopefully only one -- take the first one)
          this.$state = response[0];
          useProjectStore().setPrj(this.last_project_id);
        } else {
          // No user with that email -- create one so we can have a user_id
          // Name cannot be null
          const user_attributes = {
            name: null,
            email: email,
            last_project_id: null,
          };
          const user_id = await api.insert("users", user_attributes);
          user_attributes["user_id"] = user_id;
          this.$state = user_attributes;
          console.log(this.$state);
        }
      }
    },
  },
});
