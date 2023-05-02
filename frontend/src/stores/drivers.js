import { defineStore } from 'pinia'
import { useUserStore } from './user';
import { useProjectDataStore } from './projectData';
import * as api from '../apis/lambda';

// Initialize objects with default values
const init_objects = {
  lu_driver_categories: {id:0,name:'',color:'#000000'},
  lu_drivers: {id:null,name:'',dgroup:'',parent_id:0,sem_id:0,text_short:'',text_long:'',url:'',category_id:0,intervention_ids:[]},
  drivers_in_prj: {id:null,editing_user_id:0,lu_driver_id:0,importance_id:0,notes_context:'',notes_gap:'',notes_goal:''},
  drivers: {lu_id:0,parent_id:0,category_id:0,text_short:'',text_long:'',name:'',intervention_ids:[],
            dip_id:0,user_id:0,importance_id:0,notes_context:'',notes_gap:'',notes_goal:''},
  driver_graph: {id:null,editing_user_id:0,driver_id:0,driver_influenced_id:0,importance_id:0}
};

export const useDriverStore = defineStore({
  id: 'drivers',

  // Define the state
  state: () => ({
    lu_driver_categories: [], //{id:0,name:'',color:'#000000'},
    lu_drivers: [],  // {id:null,name:'',dgroup:'',parent_id:0,sem_id:0,text_short:'',text_long:'',url:'',category_id:0,intervention_ids:[]},
    drivers_in_prj: [], // {id:null,editing_user_id:0,lu_driver_id:0,importance_id:0,notes_context:'',notes_gap:'',notes_goal:''},
    drivers_suggested: []
  }),

  getters: {
    // Retrieve driver name by id
    nameById: (state) => (dip_id) => {
      const lu_driver_id = state.drivers_in_prj.find(dip => dip.id == dip_id).lu_driver_id;
      const name = state.lu_drivers.find(d => d.id == lu_driver_id).name;
      return name;
    },

    // Generate icon filename based on driver name
    iconFilename: (state) => (driver) => {
      return driver.name.toLowerCase().replace(' ', '_') + '.svg';
    },

    // Get factors (level 1 drivers)
    factors: (state) => {
      return state.lu_drivers.filter((d) => d.parent_id === 0);
    },

    /**
     * Get top-level drivers (factors) filtered by behavior driver category and potentially limited to suggested or project drivers.
     * @param {number} category_id - Category ID to filter all drivers.
     * @param {string} filter - either 'all', 'project', or 'suggested'
     * @returns {Object[]} a list of top-level drivers (factors) satifying the provided parameter filters
     */
    factorsByCategory: (state) => 
      (category_id, filter) => {
            if (filter=='project') {
                return state.lu_drivers.filter(d=>d.category_id===category_id && d.parent_id===0 
                  && state.drivers_in_prj.map(dp=>dp.lu_driver_id).includes(d.id))
            } else if (filter == 'all') {
                return state.lu_drivers.filter(d=>d.category_id===category_id && d.parent_id===0)
            } else { // filter == 'suggested' 
                return state.lu_drivers.filter(d=>d.category_id===category_id && d.parent_id===0 
                  && state.drivers_suggested.map(dp=>dp.id).includes(d.id))
              }
          },

    /**
     * Get second-level drivers (dimensions) filtered by their parent driver (factor) and potentially limited to suggested or project drivers.
     * @param {Object} factor - reference to a specific top-level lu_driver
     * @param {Object} factor.id - id to filter dimensions to those that are chidlren of a particular top-level driver (factor) 
     * @param {string} filter - either 'all', 'project', or 'suggested'
     * @returns {Object[]} a list of second-level drivers (dimensions) satifying the provided parameter filters
     */
    dimensionsByFactor: (state) => 
      (factor, filter) => {
            if (filter == 'project') {
                return state.lu_drivers.filter(d=>d.parent_id===factor.id
                  && state.drivers_in_prj.map(dp=>dp.lu_driver_id).includes(d.id)) 
            } else if (filter == 'all') {
                return state.lu_drivers.filter(d=>d.parent_id===factor.id) 
            } else { // filter == 'suggested'
                return state.lu_drivers.filter(d=>d.parent_id===factor.id
                && state.drivers_suggested.map(dp=>dp.id).includes(d.id)) 
            }
        },

    // Get drivers by category
    driversByCategory: (state) => (category_id) => {
      return state.lu_drivers.filter(d => d.category_id === category_id);
    },

    // Find luDriver by id
    luDriverById: (state) => (id) => {
      return state.lu_drivers.find((d) => d.id === id);
    },

    // Find project driver by luDriver id
    prjDriverByLUid: (state) => (LUid) => {
      return state.drivers_in_prj.find(d => d.lu_driver_id == LUid);
    },

    // Get drivers in the project
    driversInProject: (state) => {
      const drivers = [];
      for (const driver of state.drivers_in_prj) {
        const luDriver = state.lu_drivers.find(d => d.id == driver.lu_driver_id);
        const id = driver.id;
        const name = luDriver.name;
        const newDriver = { id, name };
        drivers.push(newDriver);
      }
      return drivers;
    },

    // Get explanation for the suggested driver by id
    suggestionExplanation: (state) => 
      (id) => {
        const foundDriver = state.drivers_suggested.find(d=>d.id==id);
        let explain;
        if (foundDriver) {
          explain = foundDriver.explanation;
        } else {
          explain = '';
        }
        return explain;
      },

    // Get example for the suggested driver by id      
    suggestionExample: (state) => (id) => {
      const foundDriver = state.drivers_suggested.find(d=>d.id==id);
      let example;
      if (foundDriver) {
        example = foundDriver.example;
      } else {
        example = '';
      }
      return example;
    }
  },

  actions: {

    // Clear state
    clear() {
      for (const property of Object.keys(this.$state)) {
        if (!property.startsWith('lu_')) {
          this.$state[property] = [];
        }
      }
    },
    
    // Download data
    async download() {
      await api.downloadObjects(init_objects,this);
      this.suggestDrivers();
    },
    
    // Add driver to project    
    async add(lu_driver_id) {
      const table = 'drivers_in_prj';
      const driver = {...init_objects.drivers_in_prj};
      const importance_id = 1  // initially set to medium importance
      driver.lu_driver_id = lu_driver_id;
      driver.importance_id = importance_id; 
      this.drivers_in_prj.push(driver); 
      await api.insert(table,{lu_driver_id,importance_id})
        .then(id=>driver.id = id);
      driver.editing_user_id = useUserStore().id;
      return driver;
    }, 

    // Remove driver from project
    async remove(id) {
      const table = 'drivers_in_prj';
      const deleteIDs = [id];
      const index = this.drivers_in_prj.findIndex(d=>d.id==id);
      this.drivers_in_prj.splice(index,1);
      api.remove(table,deleteIDs);
    },

    // Set importance of a driver
    async setImportance (driver, importance_id) {
      const table = 'drivers_in_prj';
      const userId = useUserStore().id;
      const lu_driver_id = driver.lu_driver_id;
      driver.editing_user_id = userId;
      driver.importance_id = importance_id;
      // update row in drivers_in_prj table
      api.update(table,driver.id,{lu_driver_id,importance_id})
    },

    // Suggest drivers based on project data
    async suggestDrivers() {
      // use lambda.gptCompletion() to suggest drivers based on useProjectDataStore.project_data
      // first give ChatGPT a description of the factors (level 1 drivers)

      let context_drivers = "Background:\nAs a refresher, here are the descriptions of Level 1 Drivers from the UNICEF Behavioral Drivers Model." +
          "The category for the driver is listed in parentheses, after the name:\n\n";

      const category_list = [];
      // const factors = this.lu_drivers.filter(d=>d.parent_id==0);
      for (const category of this.lu_driver_categories) {
        const factors = this.factorsByCategory(category.id,"all");
        const num_suggestions = category.id < 3 ? 1: 0; //Math.floor(factors.length / 3);
        const name = category.name;
        category_list.push({name,num_suggestions});
        if (num_suggestions > 0) {
          for (const factor of factors) {
            if (factor.text_long != '') {
              context_drivers += "\n\n" + factor.id + ". " + factor.name + " (" + category.name + ")\n" + factor.text_long;
            }
          }
        }  
      }
      
      // now give it a summary of the project
      const context_project = useProjectDataStore().summarizeProject();

      let question = "\n----\nOf the UNICEF Behavioural Drivers summarized above, list the NAME of "
      for (let i=0; i < category_list.length; i++) {
        if (i>0) {
          question += ", ";
          if (i == category_list.length - 1) {
            question += "and ";
          }
        } else {
          question += " ";
        }
        question += category_list[i].num_suggestions + " driver(s) from the " + category_list[i].name + " category"
      }
      question += " that would be most influential to achieving the SBC objectives of this project."
      question += 'In addition, include an EXPLANATION (2-4 sentences) with specific reasons why elements of this project align to your selected dimension.';
      question += 'Finally, include an EXAMPLE (3-5 sentences) describing how this driver was found to influence SBC in an actual project. Focus on the influences of this driver before the project interventions began.';
      question += "Give your answer as an array of json objects according to this format:\n";
      question += '[{"id":0,"name":"","explanation":"","example":""}]\n\n(In place of the 0 for id, use the number preceding each dimension name)\n\n';
      let context = context_drivers + context_project;
      let ai_answer = await api.gptCompletion(question, context);
      let json_answer = JSON.parse(ai_answer);
      this.drivers_suggested = json_answer;    



      context_drivers = "Background:\nAs a refresher, here are the descriptions of Dimensions (Level 2 Drivers) from the UNICEF Behavioral Drivers Model." +
          "The factor for each dimension is listed in parentheses, after its name:\n\n";

      const factor_list = [];
      for (const factor of this.drivers_suggested) {
        const dimensions = this.dimensionsByFactor(factor,"all");
        const num_suggestions = Math.floor(dimensions.length / 4) + 1;
        const name = factor.name;
        factor_list.push({name,num_suggestions});
        for (const dimension of dimensions) {
          if (dimension.text_long != '') {
            context_drivers += "\n\n" + dimension.id + ". " + dimension.name + " (" + factor.name + ")\n" + dimension.text_long;
          }
        }
      }
      question = "\n----\nOf the Dimensions summarized above, select exactly 2 dimensions for each factor "
      for (let i=0; i < factor_list.length; i++) {
        if (i>0) {
          question += ", ";
          if (i == factor_list.length - 1) {
            question += "and ";
          }
        } else {
          question += " ";
        }
        question += factor_list[i].name + " factor"
      }
      question += "that would be most influential to achieving the SBC objectives of this project."
      question += 'List the NAME of each selected dimension. ';
      question += 'Provide an EXPLANATION (2-4 sentences) with specific reasons why elements of this project align to your selected dimension.';
      question += 'Finally, include an EXAMPLE (3-5 sentences) describing how this dimension was found to influence SBC in an actual project. Focus on the influences of this dimension before the project interventions began.';
      question += "Give your answer as an array of json objects according to this format:\n";
      question += '[{"id":0,"name":"","explanation":"","example":""}]\n\n(In place of the 0 for id, use the number preceding each dimension name)\n\n';
      context = context_drivers + context_project;
      ai_answer = await api.gptCompletion(question, context); //, null,'[{"id":'
      if (ai_answer) {
        json_answer = JSON.parse(ai_answer);
        this.drivers_suggested = this.drivers_suggested.concat(json_answer);
      }
    }
 }
})
