<script setup>
// Importing required Vue libraries and modules
import { ref, onMounted } from "vue";
import { useUserStore } from "@/stores/user";
import { useRouter } from "vue-router";

// Initialize the user store and the router
const userStore = useUserStore();
const router = useRouter();

// On component mount, redirect to the login page if the user is not logged in
onMounted(() => {
  if (!userStore.loggedIn) {
    router.push({ path: "/login" });
  }
});
</script>

<template>
  <section class="hero is-fullheight">
    <div class="hero-body">
      <div class="container has-text-centered raised-title">
        <!-- Display the welcome message, addressing the user with their preferred name -->
        <h1 class="title is-1">Welcome, {{ userStore.address_as }}!</h1>
      </div>
    </div>
  </section>
</template>

<style scoped>
/* Styling for vertical center alignment */
.vertical-center {
  margin: 2rem;
}

/* Styling to raise the welcome message to slightly above center */
.raised-title {
  margin-top: -20rem; /* Adjust this value to change the vertical position */
}
</style>
