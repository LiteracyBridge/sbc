import { defineStore } from 'pinia'
import { useUserStore } from './user';

import * as api from '../apis/axios';

export const useDriverStore = defineStore({
  id: 'drivers',

  state: () => ({
    lu_driver_categories: [{id:0,name:'Psychology',color:'#A9D18E'}],
    drivers: [{lu_id:1,parent_id:0,category_id:0,text_short:'',text_long:'',name:'Cognitive biases',intervention_ids:[1],
              dip_id:0,user_id:0,importance_id:0,notes_context:'',notes_gap:'',notes_goal:''}],
    driver_graph: [{id:0,user_id:0,driver_id:0,driver_influenced_id:0,importance_id:0}]
  }),

  getters: {
    iconFilename: (state) => 
      (driver) => driver.name.toLowerCase().replace(' ','_')+'.svg',
    factors:(state) => 
      state.drivers.filter((d)=>d.parent_id===0),
    dimensionsByFactor:(state) => 
      (factor) => state.drivers.filter(d=>d.parent_id===factor.lu_id),
    driversByCategory:(state) => 
      (category_id) => state.drivers.filter(d=>d.category_id===category_id),
    factorsByCategory:(state) => 
      (category_id) => state.drivers.filter(d=>d.category_id===category_id && d.parent_id===0),
    driverByLUid:(state) => 
      (driverLUId) => state.drivers.find((d)=>d.lu_id===driverLUId),
    driverByDIPid:(state) =>
      (driverDIPid) => state.drivers.find((d)=>d.dip_id===driverDIPid),
    driversInProject:(state) => state.drivers.filter(d=>d.dip_id != null)
  },


  actions: {
    async setImportance (lu_driver_id, importance_id = null) {
      const table = 'drivers_in_prj';
      const driver = this.driverByLUid(lu_driver_id);
      const userId = useUserStore().id;
      driver.user_id = userId;
      if (importance_id == null) {
        importance_id = driver.importance_id;
      }
      // check if dip_id already exists to determine if axios shuold call an update or an insert on the drivers_in_prj table
      if (driver.dip_id == null) {
        // insert a new row in drivers_in_prj table
        driver.dip_id = await api.insert(table,{lu_driver_id,importance_id},userId)
      } else {
        // update row in drivers_in_prj table
        api.update(table,driver.dip_id,{lu_driver_id,importance_id},userId)
      }
    },
    download() {
      api.downloadObjects(this.$state,this);
    }
 }
})
