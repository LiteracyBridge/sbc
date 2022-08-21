import { defineStore } from 'pinia'
import * as api from '@/apis/axios.js'
import { useProjectStore } from './project.js'
import { useDriverStore } from './drivers.js'
import { useActivityStore } from './activities.js'
import { useInterventionStore } from './interventions.js'

export const useUserStore = defineStore({
  id: 'user',
  state: () => ({
    id: null, 
    email: null,
    name: null,
    last_project_id: null
  }),
  getters: {
    firstName: (state)=> state.name ? state.name.split(' ')[0] : '',
    loggedIn: (state) => !(state.email == null)
  },
  actions: {
    // addActivity ({name,parent_id=null,driver_id=null,intervention_id=null,owner_id=null,status_id=1,notes='',url=''} = {}) {
    async setUser(email = null, token = null) {
      console.log('setUser:'+email);
      this.email = email;
      if (email == null ) {
        this.id = null;
        this.name = null;
        this.last_project_id = null;
      } else {
        const attributes = Object.keys(this.$state).join(',')
        console.log(attributes);
        const response = await api.downloadObject('users',['id','name','last_project_id'],'email='+this.email);
        this.$state = response[0];
        console.log('useUserStore last project:'+this.last_project_id);
        useProjectStore().setPrj(this.last_project_id);
        useProjectStore().download();
        useInterventionStore().download();
        useDriverStore().download();
        useActivityStore().download();
      }
    }
  }
})
