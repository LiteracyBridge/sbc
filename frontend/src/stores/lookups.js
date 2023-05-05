import { defineStore } from 'pinia';
import { downloadObjects } from '@/apis/lambda';

// Initial objects for lookup data structure
const init_objects = {
  access_types: { id: 0, name: '' },
  activity_status: { id: 0, name: '' },
  countries: { id: 0, name: '' },
  importance: { id: 0, name: '', color: '' },
  library_types: { id: 0, name: '' },
  participant_types: { id: 0, name: '' },
  sem: { id: 0, name: '', description: '' },
  toc_types: { id: 0, name: '', text_short: '', text_long: '' },
};

export const useLookupStore = defineStore({
  id: 'lookup',
  state: () => ({
    access_types: [],
    activity_status: [],
    countries: [],
    importance: [],
    library_types: [],
    participant_types: [],
    sem: [],
    toc_types: [],
  }),
  getters: {
    lookupNameById: (state) =>
      function (lookupName, id) {
        try {
          const obj = state[lookupName].find((a) => a.id == id);
          let name = '';
          if (obj != null) {
            name = obj.name;
          }
          return name;
        } catch (e) {
          console.log(e);
          return null;
        }
      },
  },
  actions: {
    // Downloads lookup data and sets it to the store state
    download() {
      downloadObjects(init_objects, this, 'lu_');
    },
  },
});
