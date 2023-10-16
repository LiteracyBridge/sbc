import { defineStore } from "pinia";
import { useUserStore } from "./user";
import * as api from "../apis/lambda";
import { useProjectStore } from "./projects";
import { ApiRequest } from "@/apis/api";
import { ProjectData, ProjectDataModule, ProjectDataName } from "@/types";
import { message } from "ant-design-vue";
import { twilioBroadcast } from "../apis/lambda";

export class ProjectDataForm {
  id?: number | string;
  name?: string;
  q_id: number;
  data: string;
  label: string;
  showBuild: boolean = false;
  deleted: boolean = false;
  module: ProjectDataModule;
}

export const useProjectDataStore = defineStore({
  id: "project_data",
  state: () => ({
    new_project_data: [] as ProjectData[],
    loading: false,

    // objectives: [] as ProjectData[],
    questions: [
      {
        id: 0,
        topic: "basic",
        topic_id: 0,
        bulb: true,
        q2u: "What is the name of your project?",
        q2ai: "Propose a name for this SBC program.",
        f4ai: "item",
        label: "Program Name",
      },
      {
        id: 1,
        topic: "basic",
        topic_id: 1,
        bulb: false,
        q2u: "What sector is this project working in?",
        q2ai: "Propose a sector for this project.",
        f4ai: "item",
        label: "Sector",
      },
      {
        id: 2,
        topic: "basic",
        topic_id: 2,
        bulb: false,
        q2u: "Where is your project working?",
        q2ai: "",
        f4ai: "item",
        label: "Location",
      },
      {
        id: 3,
        topic: "basic",
        topic_id: 3,
        bulb: false,
        q2u: "What partner organizations are working on this project?",
        q2ai: "",
        f4ai: "list",
        label: "Partners",
      },
      {
        id: 4,
        topic: "basic",
        topic_id: 4,
        bulb: true,
        q2u: "Write a summary paragraph for this project.",
        q2ai: "Summarize this project in one paragraph.",
        f4ai: "item",
        label: "Project Summary",
      },
      {
        id: 5,
        topic: "background",
        topic_id: 0,
        bulb: false,
        q2u: "What challenge is your project working to address?",
        q2ai: "",
        f4ai: "item",
        label: "Challenges",
      },
      {
        id: 6,
        topic: "background",
        topic_id: 1,
        bulb: true,
        q2u: "What are the root causes of that challenge?",
        q2ai: "What are the root causes of the challenges? each root cause should be a separate item in the list.",
        f4ai: "list",
        label: "Root Causes",
      },
      {
        id: 7,
        topic: "background",
        topic_id: 2,
        bulb: true,
        q2u: "What other background information do you have on the context of your project? (social, economic, cultural, political, etc.)",
        q2ai: "What other background information do you have on the context of your project? DO NOT GIVE ISSUES ALREADY STATED IN THE PROJECT CHALLENGES!",
        f4ai: "short_answer",
        label: "Other background",
      },
      {
        id: 8,
        topic: "objectives",
        topic_id: 0,
        bulb: false,
        q2u: "What is your project's long term goal or vision?",
        q2ai: "",
        f4ai: "item",
        label: "Project Vision",
      },
      {
        id: 9,
        topic: "objectives",
        topic_id: 1,
        bulb: true,
        q2u: "What behavior(s) is your project seeking to influence?",
        q2ai: "Propose a list of behaviors that this project may be seeking to influence.",
        f4ai: "list",
        label: "Targeted Behaviors",
      },
      // {
      //   id: 10,
      //   topic: "objectives",
      //   topic_id: 2,
      //   bulb: true,
      //   q2u: "What specific objective(s) will your project achieve? What changes will your project make happen?",
      //   q2ai: "Propose a list of objectives that this project may be able to achieve.",
      //   f4ai: "list",
      //   label: "Objectives",
      // },
      // {
      //   id: 11,
      //   topic: "audiences",
      //   topic_id: 0,
      //   bulb: true,
      //   q2u: "Who is the primary target audience for your project? Who will be adopting the behavior you want to influence?",
      //   q2ai: "Propose a primary target audience for this project.",
      //   f4ai: "item",
      //   label: "Primary Audience",
      // },
      // {
      //   id: 12,
      //   topic: "audiences",
      //   topic_id: 1,
      //   bulb: true,
      //   q2u: "Who else influences the actions of your main target audience? What other audiences need to be involved? Who else influences the actions of your main target audience? What other audiences need to be involved?",
      //   q2ai: "Propose a list of potential other audiences who may influence the actions of the primary audience.",
      //   f4ai: "list",
      //   label: "Influencers",
      // },
      {
        id: 13,
        topic: "audiences",
        topic_id: 2,
        bulb: true,
        q2u: "What key stakeholders will need to be engaged to ensure the success of your project?",
        q2ai: "Propose a list of key stakeholders to consider for this project.",
        f4ai: "item",
        label: "Key Stakeholders",
      },
    ],

    /**
     * @deprecated
     * use 'new_project_data' instead
     */
    project_data: [],
    topics: [
      { id: 0, sequence: 0, value: "basic", label: "Project Info" },
      {
        id: 1,
        sequence: 1,
        value: "background",
        label: "Background and context",
      },
      { id: 2, sequence: 2, value: "objectives", label: "Project objectives" },
      { id: 3, sequence: 3, value: "audiences", label: "Audiences" },
      // {id:2,sequence:4,value:"drivers",label:"Behavioral drivers and barriers"},
      {
        id: 4,
        sequence: 5,
        value: "approaches",
        label: "Approaches and Activities",
      },
      // {id:1,sequence:6,value:"toc",label:"Theory of Change"},
      {
        id: 5,
        sequence: 7,
        value: "communications",
        label: "Communications and Messaging",
      },
      {
        id: 6,
        sequence: 8,
        value: "monitoring",
        label: "Monitoring and Evaluation",
      },
      { id: 7, sequence: 9, value: "prjmgmt", label: "Project Management" },
      { id: 8, sequence: 9, value: "prjdocs", label: "Project Documents" },
    ],

    // Project Info
    sector: {} as ProjectData,
  }),
  getters: {
    questionsForTopic: (state) => (topic: string) =>
      state.questions.filter((q) => q.topic == topic),
    countBulbs: (state) => (id: number, topic: string) =>
      state.questions.filter(
        (question) =>
          question.id <= id && question.bulb === true && question.topic == topic
      ).length,
    answerForQuestionId: (state) => (questionId: number) =>
      state.project_data.filter((d) => d.q_id == questionId)[0],
    getData: (state) => {
      return (questionId: number): string =>
        state.new_project_data.find((d) => d.q_id == questionId)?.data;
    },
    findByQuestionId: (state) => {
      return (questionId: number): ProjectData | null => {
        const result =
          state.new_project_data.filter((d) => d.q_id == questionId) || [];

        if (result.length == 0) {
          return null;
        }

        if (result.length == 1) {
          return result[0];
        }

        // There are situations where there are multiple records for a question, this could be
        // slow network but haven't been able to reliably reproduce it. So, we'll just merge the data
        const merged = result
          .sort((a, b) => a.id - b.id) // sort by id, so that the latest is last
          .reduce((acc, curr) => {
            return {
              ...acc,
              data: acc.data + "\n\n" + curr.data,
            };
          });

        return merged;
      };
    },
    // specificObjectives: (state) => {
    //   return state.project_data.filter((d) => d.name == "specific_objectives");
    // },

    // Project Objectives
    specificObjectives: (state) => {
      return state.new_project_data.filter(
        (d) => d.name == "specific_objective"
      );
    },

    // Audiences
    secondaryAudiences: (state) => {
      return state.new_project_data.filter(
        (d) => d.name == "secondary_audience"
      );
    },
    primaryAudience: (state) => {
      return state.new_project_data.filter((d) => d.name == "primary_audience");
    },
    audiences: (state) => {
      return state.new_project_data.filter(
        (d) => d.name == "primary_audience" || d.name == "secondary_audience"
      );
    },
  },
  actions: {
    clear() {
      for (const property of Object.keys(this.$state)) {
        // @ts-ignore
        this.$state[property] = [];
      }
    },

    async download() {
      this.$state.loading = true;

      // TODO: Remove this query
      const key_index = 1;
      const filter_clause = "prj_id=" + useProjectStore().prj_id;
      // const data = await api.downloadDictionary(
      //   "project_data",
      //   [
      //     "id",
      //     "q_id",
      //     "editing_user_id",
      //     "data",
      //     "name",
      //     "module",
      //     "theory_of_change_id",
      //   ],
      //   filter_clause,
      //   key_index
      // );
      // this.$state.project_data = data as any;
      // this.$state.objectives = Object.values(data).filter(
      //   (d) => d.name == "specific_objectives"
      // );
      // console.error(Object.values(data));

      // Download project data
      return await ApiRequest.get<ProjectData>(
        `project/${useProjectStore().prj_id}/data`
      )
        .then((resp) => {
          this.$state.new_project_data = resp;

          // Update sector
          this.$state.sector =
            resp.find((i) => i.name == ProjectDataName.sector) ??
            new ProjectData();
          this.$state.sector.name ??= ProjectDataName.sector;
          this.$state.sector.module ??= ProjectDataModule.project_info;
          this.$state.sector.data ??= "";
          this.$state.sector.q_id ??= 1;

          return resp;
        })
        .catch((err) => {
          message.error(err.message);
          throw err;
        })
        .finally(() => (this.$state.loading = false));
    },

    async setData(q_id: number, data: any) {
      const name = q_id == 1 ? "sector" : null;

      if (!(q_id in this.project_data)) {
        this.project_data[q_id] = {};
      }
      this.project_data[q_id]["data"] = data;
      const id = this.project_data[q_id].id;
      if (id) {
        return await api.update("project_data", id, { q_id, data, name });
      } else {
        this.project_data[q_id].q_id = q_id;
        this.project_data[q_id].editing_user_id = useUserStore().id;
        // this.updateProjectData(this.project_data[q_id]);
        const _id = await api.insert("project_data", {
          q_id,
          data,
          name,
        });
        this.project_data[q_id].id = _id;
      }
    },

    async deleteData(id: number | string) {
      return ApiRequest.delete<ProjectData>(
        `project/${useProjectStore().prj_id}/data/${id}`
      )
        .then((resp) => {
          this.$state.new_project_data = resp;
          return resp;
        })
        .catch((err) => {
          message.error(err.message);
          throw err;
        });
    },

    async addOrUpdate(form: ProjectDataForm[]) {
      this.loading = true;
      return ApiRequest.post<ProjectData>(
        `project/${useProjectStore().prj_id}/data`,
        form.map((i) => ({
          ...i,
          editing_user_id: useUserStore().id,
        }))
        // {
        //   name: form.name,
        //   q_id: form.q_id,
        //   id: form.id,
        //   data: form.value,
        //   module: form.module,
        //   editing_user_id: useUserStore().id,
        // }
      )
        .then((resp) => {
          // if (resp.length > 0) {
          //   const temp = this.$state.new_project_data;

          //   const index = temp.findIndex((i) => i.id == resp[0].id);

          //   if (index < 0) {
          //     temp.push(resp[0]);
          //   } else {
          //     temp[index] = resp[0];
          //   }

          //   this.$state.new_project_data = resp;
          // }

          // return resp[0];
          this.$state.new_project_data = resp;
          message.success("Changes saved successfully!");
          return resp;
        })
        .finally(() => (this.loading = false));
    },

    summarizeProject() {
      let summary =
        "\n----\nHere's a summary of the SBC project I want you to analyze:\n";
      for (var q of this.questions) {
        const a = this.getData(q.id);
        if (!(a === null || a == "")) {
          summary += q.label + ": " + a + "\n\n";
        }
      }
      return summary;
    },
    async addOrRemoveObjective(value?: string, removed_id?: number) {
      return ApiRequest.post<ProjectData>(
        `project/${useProjectStore().prj_id}/objectives`,
        {
          editing_user_id: useUserStore().id,
          description: value,
          removed_id: removed_id,
        }
      )
        .then((resp) => {
          this.$state.project_data = resp;
          this.$state.new_project_data = resp;
          message.success("Project objectives added successfully");

          return resp;
        })
        .catch((err) => message.error(err.message));
    },
    async updateData(form: {
      editing_user_id: number;
      added: string[];
      removed: number[];
      updated: Record<string, any>[];
      name: "primary_audience" | "secondary_audience" | "specific_objective";
      module: "audiences" | "objectives";
    }) {
      this.$state.loading = true;
      return ApiRequest.post<ProjectData>(
        `project/${useProjectStore().prj_id}/data`,
        form
      )
        .then((resp) => {
          this.$state.new_project_data = resp;
          message.success("Project audiences updated successfully");
          return resp;
        })
        .catch((err) => {
          message.error(err.message);
          throw err;
        })
        .finally(() => (this.$state.loading = false));
    },

    /**
     * Build broadcast message
     */
    buildBroadcastMessage(module: string): string {
      let msg = "";
      for (var q of this.questionsForTopic(module)) {
        const a = this.getData(q.id);
        if (a != "") {
          msg += `${q.label} \n${a} \n\n`;
        }
      }

      // If module is objectives, Add 'specific objectives' to the message
      if (module == "objectives") {
        msg += "Specific Objectives\n";
        for (const o of this.specificObjectives) {
          msg += `  • ${o.data}\n`;
        }
        msg += "\n";
      }

      // Add audiences to the message
      if (module == "audiences") {
        msg += "Primary Audiences\n";
        for (const o of this.primaryAudience) {
          msg += `  • ${o.data}\n`;
        }
        msg += "\n";

        msg += "Secondary Audiences\n";
        for (const o of this.secondaryAudiences) {
          msg += `  • ${o.data}\n`;
        }
      }
      return msg;
    },

    /**
     * Broadcasts a message to all users in the project
     */
    async broadcastPage(module: string) {
      message.info("Broadcasting message to all users in the project");

      this.$state.loading = true;
      const ms = this.buildBroadcastMessage(module);
      await twilioBroadcast(ms, module);
      this.$state.loading = false;
    },
  },
});
