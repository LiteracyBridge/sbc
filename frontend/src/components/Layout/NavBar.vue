<script setup>
import { ref } from 'vue'
import { Auth } from 'aws-amplify';
import { onClickOutside } from '@vueuse/core'
import { useUserStore } from '@/stores/user'
import { useProjectStore } from '@/stores/projects';
import { useSideNavStore } from "@/stores/sideNav";
import { useRouter } from 'vue-router';
import LogoWhite from '@/assets/logo-white.png';

const router = useRouter();
const showMobileNav = ref(false)
const userStore = useUserStore();
const projectStore = useProjectStore();
const navbarMenuRef = ref(null)
const navbarBurgerRef = ref(null)
const sideNavStore = useSideNavStore();

onClickOutside(navbarMenuRef, () => {
  showMobileNav.value = false
}, {
  ignore: [navbarBurgerRef]
})

const toggleSideNav = function (event) {
  const x = event.currentTarget;
  x.classList.toggle("change");
  sideNavStore.toggle();
};

const goHome = function () {
  router.push('/');
}


async function signOut() {
  try {
    await Auth.signOut()
      .then((resp) => {
        userStore.setUser();
        sideNavStore.hide()

        router.push('/login');
        window.location.reload()
      })
  } catch (error) {
    userStore.setUser();
    router.push('/login')

    window.location.reload()
    console.log('error signing out: ', error);
  }
}

</script>

<template>
  <nav class="navbar is-success is-fixed-top" aria-label="main navigation" role="navigation">
    <!-- <div class="container is-max-desktop px-2"> -->
    <div class="container is-fluid">
      <div class="navbar-brand">

        <div class="navbar-item" @click="goHome">
          <!-- <a class="navbar-item"> -->
          <img src="@/assets/logo.png" alt="Bulma: Free, open source, and modern CSS framework based on Flexbox"
            class="mr-1">
          SBC Impact Designer
          <!-- </a> -->
        </div>

        <!-- <div class="container" @click="toggleSideNav">
          <div class="bar1"></div>
          <div class="bar2"></div>
          <div class="bar3"></div>
        </div> -->




        <a @click.prevent="showMobileNav = !showMobileNav" class="navbar-burger" :class="{ 'is-active': showMobileNav }"
          aria-expanded="false" aria-label="menu" data-target="navbarBasic" role="button" ref="navbarBurgerRef">
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
        </a>
      </div>

      <div id="navbarBasic" class="navbar-menu" :class="[{ 'is-active': showMobileNav }]" ref="navbarMenuRef">
        <div class="navbar-end" v-if="userStore.loggedIn">
          <!-- <RouterLink @click="showMobileNav = false" to="/projects" class="navbar-item" active-class="is-active">
            Projects
          </RouterLink>

          <RouterLink v-if="projectStore.prj_id" @click="showMobileNav = false" to="/drivers" class="navbar-item"
            active-class="is-active">
            Resources
          </RouterLink> -->
          <!--
          <RouterLink v-if="projectStore.prj_id" @click="showMobileNav = false" to="/activities" class="navbar-item"
            active-class="is-active">
            Help
          </RouterLink>

          <RouterLink @click="showMobileNav = false" to="/login" class="navbar-item" active-class="is-active">
            <span v-if="userStore.loggedIn" class="mr-2">Logout</span>
            {{ userStore.address_as }}
          </RouterLink> -->

          <div class="navbar-item has-dropdown is-hoverable">
            <a class="navbar-link">
              <span class="icon mr-1">
                <i class="fas fa-user-circle"></i>
              </span>
              {{ userStore.address_as }}
            </a>

            <div class="navbar-dropdown">


              <RouterLink v-if="projectStore.prj_id" to="/drivers" class="navbar-item">
                <span class="icon mr-1">
                  <i class="fas fa-book"></i>
                </span>
                Resources
              </RouterLink>

              <RouterLink to="/projects" class="navbar-item">
                <span class="icon mr-1">
                  <i class="fas fa-briefcase"></i>
                </span>
                Projects
              </RouterLink>

              <RouterLink v-if="projectStore.prj_id" to="/activities" class="navbar-item">
                <span class="icon mr-1">
                  <i class="fas fa-question-circle"></i>
                </span>
                Help
              </RouterLink>

              <hr class="navbar-divider">
              <div v-if="userStore.loggedIn">
                <!-- FIX: fix user logout -->
                <a @click="signOut" class="navbar-item">
                  <span class="icon mr-1">
                    <i class="fas fa-sign-out"></i>
                  </span>
                  Logout
                </a>
              </div>
            </div>
          </div>

          <!-- <div class="navbar-item">
            <img :src="LogoWhite" alt="Logo" />
          </div> -->


        </div>
      </div>
    </div>
  </nav>
</template>

<style>
@media (max-width: 1023px) {
  .navbar-menu {
    position: absolute;
    left: 0;
    width: 100%;
  }
}

.navbar {
  z-index: 102;
}

.navbar-menu.is-active {
  left: 240px;
}

.container {
  display: inline-block;
  cursor: pointer;
}

.bar1 {
  width: 35px;
  height: 4px;
  background-color: #FFF;
  margin: 5px 0;
  margin-top: 15px;
  transition: 0.4s;
  transform: translate(0, 11px) rotate(-45deg);
}

.bar2 {
  width: 35px;
  height: 4px;
  background-color: #FFF;
  margin: 5px 0;
  transition: 0.4s;
  opacity: 0;
}

.bar3 {
  width: 35px;
  height: 4px;
  background-color: #FFF;
  margin: 5px 0;
  transition: 0.4s;
  transform: translate(0, -8px) rotate(45deg);
}

.change .bar1 {
  transform: translateY(0) rotate(0);
}

.change .bar2 {
  opacity: 1;
}

.change .bar3 {
  transform: translateY(0) rotate(0);
}

.custom-link {
  font-family:
    /* Your desired font-family */
  ;
  font-size:
    /* Your desired font-size */
  ;
  font-weight:
    /* Your desired font-weight */
  ;
  color: inherit;
  text-decoration: none;
}

.custom-link:hover,
.custom-link:focus {
  color: inherit;
  text-decoration: none;
}

.custom-link-text {
  color: white;
}
</style>
