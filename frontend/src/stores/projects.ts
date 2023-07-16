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
import { Project, Stakeholder } from "@/types";
import { ApiRequest } from "@/apis/api";
import { message } from "ant-design-vue";
import { AppStore } from "./app.store";

// projectStores returns all the stores that have project-specific data
const projectStores = () => [
  // useActivityStore,
  useProjectDataStore,
  useInterventionStore,
  useDriverStore,
  useParticipantStore,
];

// Clears all project-specific data from stores
function clearAllProjectStores() {
  for (const store of projectStores()) {
    store().$reset();
  }
}

// Downloads all project-specific data from stores
async function downloadAllProjectStores() {
  for await (const store of projectStores()) {
    await store().download();
  }
}

const init_objects = {
  // below are SQL Views; so updates/inserts/deletes require the projects or project_users tables
  users_in_project: {
    // @ts-ignore
    id: null,
    // @ts-ignore
    user_id: null,
    email: "",
    name: "",
    // @ts-ignore
    access_id: null,
    address_as: "",
  },
  user_projects: {
    // @ts-ignore
    prj_id: null,
    name: "",
    // @ts-ignore
    private_prj: true,
    // @ts-ignore
    country_id: null,
    // @ts-ignore
    access_id: null,
    start_date: "",
    end_date: "",
    archived: true,
  },
};

export const useProjectStore = defineStore({
  id: "projects",
  state: () => ({
    loading: false,
    prj_id: null,
    users_in_project: [],
    user_projects: [],
    current_project: {} as Project,
  }),
  getters: {
    projects:
      (state) =>
      (archived = false) =>
        state.user_projects.filter((p) => p.archived == archived),
    userById: (state) => (userId: number) =>
      state.users_in_project.find((u) => u.user_id == userId),
    userName: (state) => (userId: number) => {
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
      const name = state.current_project?.name;
      if (name) return name;

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
    stakeholders: (state) => state.current_project?.stakeholders ?? [],
  },
  actions: {
    // Archives a project by updating its archived status
    async archive(prj_id: number) {
      this.user_projects.find((p) => p.prj_id == prj_id).archived = true;
      api.update("projects", prj_id, { archived: true });
      if (prj_id == this.prj_id) {
        this.setPrj(null); // if archiving the currently open project, must clear it
      }
    },

    // Updates a user's access in a project
    async updateAccess(event: any, uip_id: number) {
      const access_id = parseInt(event.target.value);
      this.users_in_project.find((u) => u.id == uip_id).access_id = access_id;
      api.update("project_users", uip_id, { access_id });
    },

    // Adds a user to a project
    async addUser(
      name: string,
      email: string,
      access_id: number,
      address_as: string = ""
    ) {
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
    async add(
      name: string,
      country_id: number,
      start_date: string,
      end_date: string
    ) {
      // create entry in db projects table and get id
      const private_prj = true;
      const prj_id = await api.insert("projects", {
        name,
        country_id,
        private_prj,
        start_date,
        end_date,
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
    async setPrj(id: number, newProject: boolean = false) {
      this.prj_id = id;

      await useUserStore().setLastProject(id);

      // await AppStore().downloadObjects();
      useProjectStore().download();
      if (id && !newProject) {
        clearAllProjectStores();
        downloadAllProjectStores();
      } else {
        clearAllProjectStores();
      }

      // if (!id) {
      //   router.push({ path: "/projects" });
      // }

      return;
    },

    // Update project strategy
    async updateStrategy() {
      this.$state.loading = true;
      return await ApiRequest.put<Project>(`project/${this.$state.prj_id}`, {
        evaluation_strategy: this.$state.current_project.evaluation_strategy,
        feedback_strategy: this.$state.current_project.feedback_strategy,
        sustainability_strategy:
          this.$state.current_project.sustainability_strategy,
      })
        .then((response) => {
          this.$state.current_project = response[0];
          message.success("Project strategy updated");
          return response;
        })
        .catch((error) => {
          message.error(error.message);
          throw error;
        })
        .finally(() => (this.$state.loading = false));
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
            "start_date",
            "end_date",
          ],
          "user_id=" + useUserStore().id,
          true
        );
        this.user_projects = response;
      }

      // Download current project data
      if (this.prj_id) {
        this.$state.loading = true;
        await ApiRequest.get<Project>(`project/${this.projectId}`)
          .then((response) => {
            if (response.length > 0) {
              this.$state.current_project = response[0] as Project;
            }
            return response;
          })
          .catch((error) => {
            message.error(error.message);
            throw error;
          })
          .finally(() => (this.$state.loading = false));
      }

      return;
    },

    /**
     * Delete project stakeholder
     */
    async deleteStakeholder(id: number) {
      this.$state.loading = true;

      return await ApiRequest.delete<Stakeholder>(
        `project/${this.prj_id}/stakeholders/${id}`
      )
        .then((resp) => {
          this.$state.current_project.stakeholders = resp;
          message.success("Stakeholder deleted successfully!");
          return resp;
        })
        .catch((error) => {
          message.error(error.message);
          throw error;
        })
        .finally(() => (this.$state.loading = false));
    },
    /**
     * Update or add project stakeholder
     */
    async createOrUpdateStakeholder(form: Stakeholder) {
      this.$state.loading = true;

      form.project_id = this.prj_id;
      form.editing_user_id = useUserStore().id;

      return await ApiRequest.post<Stakeholder>(
        `project/${this.prj_id}/stakeholders`,
        form
      )
        .then((resp) => {
          this.$state.current_project.stakeholders = resp;
          message.success(
            `Stakeholder ${form.id != null ? "updated" : "added"} successfully`
          );

          return resp;
        })
        .catch((error) => {
          message.error(error.message);
          throw error;
        })
        .finally(() => (this.$state.loading = false));
    },
  },
});
