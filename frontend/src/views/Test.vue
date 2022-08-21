<template>
  <div>
    <Multiselect
      v-model="value"
      :options="options"
      mode="tags"
      valueProp="lu_id"
      nameProp="name"
      label="name"
      placeholder=""
    />
    <div>
        {{value}}
    </div>
  </div>
</template>

<script setup>
  import Multiselect from '@vueform/multiselect'
  import { useDriverStore } from '../stores/drivers'
  import { ref } from 'vue'
  const driverStore = useDriverStore();

  const value = ref(null);
  const options = ref(driverStore.driversInProject);
    
    // [
    //       {id:1,name:'Batman'},
    //       {id:2,name:'Robin'},
    //       {id:3,name:'Joker'}
    //     ]);

</script>

<style src="@vueform/multiselect/themes/default.css"></style>