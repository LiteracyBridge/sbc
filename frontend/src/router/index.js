import { createRouter, createWebHistory } from 'vue-router'
import Drivers from '../views/Drivers.vue'
import Activities from '../views/Activities.vue'
import Login from '../views/Login.vue'
import Home from '../views/Home.vue'
import Test from '../views/Test.vue'
import { useUserStore } from '../stores/user'
import { Auth } from 'aws-amplify'
import { Hub } from "@aws-amplify/core"

let user;

getUser().then((user) => {
    if (user) {
        router.push({path: '/'});
    }
});

function getUser() {
  return Auth.currentAuthenticatedUser().then((data) => {
      if (data && data.signInUserSession) {
        useUserStore().setUser(data.attributes.email,data.signInUserSession.accessToken.jwtToken);
          return data;
      }
  }).catch(() => {
    useUserStore().setUser();
      return null;
  });
}

Hub.listen("auth", async (data) => {
  if (data.payload.event === 'signOut'){
      user = null;
      useUserStore().setUser();
      router.push({path: '/login'});
  } else if (data.payload.event === 'signIn') {
      user = await getUser();
      router.push({path: '/'});
  }
});


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [  {
    path: '/',
    name: 'home',
    component: Home
  },
  {
    path: '/login',
    name: 'login',
    component: Login
  },
  {
    path: '/drivers',
    name: 'drivers',
    component: Drivers
  },
  {
    path: '/activities',
    name: 'activities',
    component: Activities
  },
  {
    path: '/test',
    name: 'test',
    component: Test
  }
  ]
})

export default router
