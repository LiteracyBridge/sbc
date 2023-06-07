import { defineStore } from "pinia";
import * as api from "@/apis/lambda";
import { useUserStore } from "./user";
import { useDriverStore } from "./drivers";
import { useActivityStore } from "./activities";
import { useInterventionStore } from "./interventions";
import { useParticipantStore } from "./participants";
import router from "@/router";
import { useLookupStore } from "./lookups";
import { useProjectDataStore } from "./projectData";

// projectStores returns all the stores that have project-specific data
const projectStores = () => [
  useActivityStore,
  useInterventionStore,
  useDriverStore,
  useParticipantStore,
  useProjectDataStore,
];

// Clears all project-specific data from stores
function clearAllProjectStores() {
  for (const store of projectStores()) {
    store().clear();
  }
}

// Downloads all project-specific data from stores
function downloadAllProjectStores() {
  for (const store of projectStores()) {
    store().download();
    console.log("just downloaded " + store());
  }
}

const init_objects = {
  // below are SQL Views; so updates/inserts/deletes require the projects or project_users tables
  users_in_project: {
    id: null,
    user_id: null,
    email: "",
    name: "",
    access_id: null,
    address_as: "",
  },
  user_projects: {
    prj_id: null,
    name: "",
    private_prj: true,
    country_id: null,
    access_id: null,
    archived: true,
  },
};

export const useProjectStore = defineStore({
  id: "projects",
  state: () => ({
    prj_id: null,
    users_in_project: [],
    user_projects: [],
  }),
  getters: {
    projects:
      (state) =>
      (archived = false) =>
        state.user_projects.filter((p) => p.archived == archived),
    userById: (state) => (userId) =>
      state.users_in_project.find((u) => u.user_id == userId),
    userName: (state) => (userId) => {
      let user = state.users_in_project.find((u) => u.user_id == userId);
      let name = "";
      if (user != null) {
        name = user.name;
      }
      return name;
    },
    projectId: (state) => {
      if (state.prj_id && state.user_projects.length) {
        const foundProject = state.user_projects.find(
          (p) => p.prj_id == state.prj_id
        );
        if (foundProject) {
          console.log("foundProject", foundProject);
          return foundProject.prj_id;
        }
      }
      return undefined;
    },
    projectName: (state) => {
      if (state.prj_id && state.user_projects.length) {
        const foundProject = state.user_projects.find(
          (p) => p.prj_id == state.prj_id
        );
        if (foundProject) {
          console.log("foundProject", foundProject);
          return foundProject.name;
        }
      }
      return "";
    },
    grantableAccess: (state) => {
      if (state.prj_id && state.user_projects.length) {
        const user_access = state.user_projects.find(
          (p) => p.prj_id == state.prj_id
        ).access_id;
        const grantable_access_types = useLookupStore().access_types.filter(
          (a) => a.id >= user_access
        );
        return grantable_access_types;
      }
    },
  },
  actions: {
    // Archives a project by updating its archived status
    async archive(prj_id) {
      this.user_projects.find((p) => p.prj_id == prj_id).archived = true;
      api.update("projects", prj_id, { archived: true });
      if (prj_id == this.prj_id) {
        this.setPrj(null); // if archiving the currently open project, must clear it
      }
    },

    // Updates a user's access in a project
    async updateAccess(event, uip_id) {
      const access_id = parseInt(event.target.value);
      this.users_in_project.find((u) => u.id == uip_id).access_id = access_id;
      api.update("project_users", uip_id, { access_id });
    },

    // Adds a user to a project
    async addUser(name, email, access_id, address_as = "") {
      if (this.users_in_project.map((p) => p.email).includes(email)) {
        console.log("user already exists in project");
        return;
      }
      const prj_id = this.prj_id;
      const last_project_id = prj_id;
      let user_id = await api.getId("users", "email=" + email, true); // get from db if exists
      console.log("checking user id");
      if (!user_id) {
        // user doesn't exist, so insert user into db
        user_id = await api.insert("users", {
          name,
          email,
          last_project_id,
          address_as,
        }); // otherwise insert and get it
      }
      // insert project-user role into db
      const id = await api.insert("project_users", {
        prj_id,
        user_id,
        access_id,
      });
      // add to store, rather than download what we just inserted into the db
      this.users_in_project.push({ id, user_id, email, name, access_id });
    },

    // Adds a new project
    async add(name, country_id) {
      // create entry in db projects table and get id
      const private_prj = true;
      const prj_id = await api.insert("projects", {
        name,
        country_id,
        private_prj,
        organisation_id: useUserStore().organisation_id,
      });

      // create entry in db user_projects table, no id needed
      const user_id = useUserStore().id;
      const access_id = 0; // owner
      await api.insert("project_users", { prj_id, user_id, access_id });

      // rather than re-downloading the user_projects view, just push the latest entry
      const user_project = { prj_id, name, private_prj, country_id, access_id };
      this.user_projects.push(user_project);

      // update users_in_project with the same data for this user in previously active project
      const user = this.users_in_project.find((u) => u.user_id == user_id);
      const userCopy = { ...user };
      userCopy.access_id = access_id;
      this.users_in_project = [userCopy];

      // No need to download all tables for new project, so call setPrj with download=false.
      this.setPrj(prj_id, true);
    },

    // Sets a project as active
    setPrj(id, newProject = false) {
      this.prj_id = id;
      useProjectStore().download();
      if (id && !newProject) {
        downloadAllProjectStores();
      } else {
        clearAllProjectStores();
      }
      useUserStore().setLastProject(id);
      if (!id) {
        router.push({ path: "/projects" });
      }
    },

    // Downloads project data
    async download() {
      if (this.prj_id) {
        let response = await api.downloadObject(
          "users_in_project",
          ["id", "user_id", "email", "name", "access_id", "address_as"],
          "prj_id=" + this.prj_id,
          true
        );
        this.users_in_project = response;
      }
      if (useUserStore().id) {
        let response = await api.downloadObject(
          "user_projects",
          [
            "prj_id",
            "name",
            "private_prj",
            "country_id",
            "access_id",
            "archived",
          ],
          "user_id=" + useUserStore().id,
          true
        );
        this.user_projects = response;
      }
    },
  },
});
