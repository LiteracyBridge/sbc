<script setup>
import { onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useUserStore } from '../stores/user'
import Form from '../components/Form.vue';
const userStore = useUserStore();
onMounted(() => userStore.loggedIn ? null : useRouter().push({ path: '/login' }));
const route = useRoute();
const module = route.params.module;
console.log("module:" + module);
</script>

<template>
  <div>
    <Form :topic="module"></Form>
  </div>
</template>

<style>
.vertical-center {
  margin: 2rem;
}
</style>
