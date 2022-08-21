import { defineStore } from 'pinia'
import { useActivityStore } from './activities'
import { downloadObjects } from '@/apis/axios.js'

export const useInterventionStore = defineStore({
  id: 'interventions',
  state: () => ({
    interventions: [
      { id:1,
        name: 'Multi-media campaigns',
        text_short:'consist of using a combination of traditional and non-traditional methods of communication to reach a target audience, deliver messages, educate, entertain, induce specific emotions, increase visibility, amplify the voice of communities and young people, leverage local creativity, or project transitional characters and role models in edutainment.',
        text_long:'When traditional financial education was not effective in South Africa, for example, a television soap opera was aired, in which financial messages were delivered through a central character. Following the show, there was a decrease in gambling and expensive instalment purchases (World Bank, 2015, p. 4). Communication channels are very diverse and can include localized options such as community radio, community cinema via mobile audio-visual vans, street theatre, puppet shows, etc. Trans-media approaches are used to reinforce ideas and messages across multiple media platforms, and 360-degree strategies link multimedia engagement with community engagement.'
      }]
  }),
  getters: {
    interventionById:(state) => 
      (interventionId) => state.interventions.find((i)=>i.id==interventionId),
    interventionsByDriver:(state) => 
      (driver) => driver.intervention_ids ? state.interventions.filter((i)=>driver.intervention_ids.some((id)=>id===i.id)) : null,
    activityIds:(state) =>
      function (interventionId) {
        const activityStore = useActivityStore();
        return activityStore.activities.reduce((prev,current) => 
          current.intervention_id===interventionId ? prev.concat(current.id) : prev,[])
      }  
    },
  actions: {
    download() {
      downloadObjects(this.$state,this,'lu_');
     }
  }
})
