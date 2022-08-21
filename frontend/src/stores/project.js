import { defineStore } from 'pinia'
import * as api from '@/apis/axios.js'
import { useUserStore } from './user';

export const useProjectStore = defineStore({
  id: 'project',
  state: () => ({
    prj_id: -1,
    // below are SQL Views; so updates/inserts/deletes require the projects or project_users tables
    users_in_project: [{id:-1,email:'a@amplio.org',name:'User X',access_id:-1}],
    user_projects: [{prj_id:-1,name:'',private:true,country_id:-1,access_id:-1}]
  }),
  getters: {
  },
  actions: {
    // addActivity ({name,parent_id=null,driver_id=null,intervention_id=null,owner_id=null,status_id=1,notes='',url=''} = {}) {
    setPrj(id) {
      this.prj_id = id;
    },
    async download() {
      let response = await api.downloadObject('users_in_project',['id','email','name','access_id'],'prj_id='+this.prj_id);
      this.users_in_project = response;
      response = await api.downloadObject(
          'user_projects',['prj_id','name','private','country_id','access_id'],'user_id='+ useUserStore().id
      );
      this.user_projects = response;
      
      // api.downloadObjects(this.$state,this);
      // console.log('useProjectStore, user_projects_id:'+this.user_projects[0].id);
    }
  }
})
