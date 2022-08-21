import { defineStore } from 'pinia';
import { useUserStore } from './user';
import * as api from '../apis/axios';

export const useActivityStore = defineStore({
  id: 'activities',
  state: () => ({
    activities: [{id:0, name:'Activity 1', parent_id:null, intervention_id:null, driver_ids:[],
                  user_id:1, owner_id:1, status_id:1, notes:'', url:''}],
    schedules: [{id:0, user_id:-1, activity_id:-1, planned_date_from: new Date(2022,7,27), planned_date_to: new Date(2022,8,27),
                  actual_date_from: new Date(2022,7,28), actual_date_to: new Date(2022,8,28),
                  dependency_ids:[], owner_id:1, audience_id: 2, status_id: 2, notes:'', url: ''}]
  }),
    getters: {
    activityById:(state) => 
      (activityId) => state.activities.find((a)=>a.id==activityId)
  },
  actions: {
    // addActivity ({name,parent_id=null,driver_id=null,intervention_id=null,owner_id=null,status_id=1,notes='',url=''} = {}) {
    download() {
      api.downloadObjects(this.$state,this);
    },

    async addActivity (activity) {
      delete activity.id;
      console.log('add activity(activity)=');
      console.log(activity);
      const table = 'activities';
      const userId = useUserStore().id;
      activity['user_id'] = userId;
      const newId = await api.insert(table, {...activity}, userId);   //const newId = 99; // 
      activity.id = newId;
      this.activities.push(activity);
    },

    updateActivity (activity) {
      console.log(activity);
      let idx = this.activities.findIndex((a)=>a.id==activity.id)
      this.activities.splice(idx,1,activity)    
      const userId = useUserStore().id;  
      api.update('activities',activity.id, {...activity}, userId);
    },

    async deleteActivity (activityId, deleteChildren = false) {
      // find activity to be deleted
      const activity = this.activities.find((a)=>a.id===activityId); 

      // handle children of the to-be-deleted activity
      const children = this.activities.filter((a)=>a.parent_id===activityId);
      const deleteIds = [].push(activity).push(children);
      console.log('deleteIds:');
      console.log(deleteIds);
      const table = 'activities';
      api.remove(table,deleteIds);
      if (deleteChildren)
        this.activities = this.activities.filter((a)=>!children.includes(a));
      else 
        children.forEach((c)=>c.parent_id = activity.parent_id);
      this.activities = this.activities.filter((a)=> a != activity)
    },

    async deleteIntervention(interventionId) {
      // Delete an activity from an intervention id ONLY IF:
      //    - it has no schedules 
      //    - it has no notes
      //    - it has no child activities
      // If these conditions are not met, return false.  deleteActivity() should be used instead.
      
      // find all activities linked to the intervention
      const removeActivities = this.activities.filter((a,idx,arr)=> 
          a.intervention_id===interventionId && 
          this.schedules.filter((s)=>s.activity_id==a.id).length == 0 &&
          (!a.notes || a.notes=='') &&
          !arr.filter((b)=>b.parent_id==a.id).length);
      const deleteIds = removeActivities.map((a)=>a.id);
      console.log('deleteIds:');
      console.log(deleteIds);
      const table = 'activities';
      api.remove(table,deleteIds);
    
      this.activities = this.activities.filter((a)=>!removeActivities.includes(a));
    }
  }
})
