<template>
  <nav
    class="navbar is-success"
    aria-label="main navigation"
    role="navigation"
  >
    <div class="container is-max-desktop px-2">
      <div class="navbar-brand">
        <div class="navbar-item is-size-4 is-family-monospace">
          SBC Impact Designer   
        </div>

        <a
          @click.prevent="showMobileNav = !showMobileNav"
          class="navbar-burger"
          :class="{ 'is-active' : showMobileNav }"
          aria-expanded="false"
          aria-label="menu"
          data-target="navbarBasicExample"
          role="button"
          ref="navbarBurgerRef"
        >
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
        </a>
      </div>

      <div
        id="navbarBasicExample"
        class="navbar-menu"
        :class="{ 'is-active' : showMobileNav }"
        ref="navbarMenuRef"
      >
        <div class="navbar-end">
          <RouterLink
            @click="showMobileNav = false"
            to="/"
            class="navbar-item"
            active-class="is-active"
          >
            Home
          </RouterLink>
          <RouterLink
            @click="showMobileNav = false"
            to="/drivers"
            class="navbar-item"
            active-class="is-active"
          >
            Drivers
          </RouterLink>
          <RouterLink
            @click="showMobileNav = false"
            to="/activities"
            class="navbar-item"
            active-class="is-active"
          >
            Activities
          </RouterLink>
          <RouterLink
            @click="showMobileNav = false"
            to="/test"
            class="navbar-item"
            active-class="is-active"
          >
            Test
          </RouterLink>
          <RouterLink
            @click="showMobileNav = false"
            to="/login"
            class="navbar-item"
            active-class="is-active"
          >
          <span v-if="userStore.loggedIn">Logout </span> 
            {{userStore.firstName}}
          </RouterLink>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup>
/*
  imports
*/

  import { ref } from 'vue'
  import { onClickOutside } from '@vueuse/core'
  import { useUserStore } from '@/stores/user'
/*
  mobile nav
*/

  const showMobileNav = ref(false)
  const userStore = useUserStore();

/*
  click outside to close
*/

  const navbarMenuRef = ref(null)
  const navbarBurgerRef = ref(null)

  onClickOutside(navbarMenuRef, () => {
    showMobileNav.value = false
  }, {
    ignore: [navbarBurgerRef]
  })

</script>

<style>
@media (max-width: 1023px) {
  .navbar-menu {
    position: absolute;
    left: 0;
    width: 100%;
  }
}
</style>