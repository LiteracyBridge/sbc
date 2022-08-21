import { defineStore } from 'pinia'
import axios from 'axios';
import { downloadObjects } from '@/apis/axios.js'

export const useLookupStore = defineStore({
  id: 'lookup',
  state: () => ({
    access_types: [{id:0,name:'owner'}],
    activity_status: [{id:1,name:'proposed'}],
    countries: [{id:0,name:'country name'}],
    importance: [{id:0,name:'',color:''}],
    library_types: [{id:1,name:'article'}],
    participant_types: [{id:1,name:'infant'}],
    sem: [{id:1,name:'Individual',description:'Characteristics influencing behaviours'}],
    toc_types: [{id:1,name:'input',text_short:'',text_long:''}]
  }),
  getters: {
  },
  actions: {
    download() {
      downloadObjects(this.$state,this,'lu_');
     }
  }
})
