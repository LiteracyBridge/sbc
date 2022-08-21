<script setup>
import AddActivityModalVue from '../components/AddActivityModal.vue';
import { ref, onMounted } from "vue";
import { useUserStore } from "@/stores/user";
import { useRouter } from 'vue-router'

const userStore = useUserStore();
onMounted (()=>userStore.loggedIn ? null :  useRouter().push({ path: '/login'}));

const showModal = ref(false);

</script>

<template>
<h1>Home</h1>

</template>

<style>
.vertical-center {
  margin: 2rem;
}
</style>
<!-- 
 -->
