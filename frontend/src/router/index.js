import { createRouter, createWebHistory } from "vue-router";
import Drivers from "../views/Drivers.vue";
import Activities from "../views/Activities.vue";
import Login from "../views/Login.vue";
import Home from "../views/Home.vue";
import Projects from "../views/Projects.vue";
import Forms from "../views/Forms.vue";
import ToC from "../views/ToC.vue";
import Interventions from "../views/Interventions.vue";
import { useUserStore } from "../stores/user";
import { Auth } from "aws-amplify";
import { Hub } from "@aws-amplify/core";
import TheoryOfChangeIndex from "@/views/theory-of-change/TheoryOfChangeIndex.vue";
import MonitoringEvaluationIndex from "@/views/monitoring-n-evaluation/MonitoringEvaluationIndex.vue";

const ONLINE = true; // just for coding without internet
let user;

async function getUser() {
  return Auth.currentAuthenticatedUser()
    .then((data) => {
      if (data && data.signInUserSession) {
        useUserStore().setUser(
          data.attributes.email,
          data.signInUserSession.accessToken.jwtToken
        );
        return data;
      }
    })
    .catch(() => {
      useUserStore().setUser();
      return null;
    });
}

if (ONLINE) {
  getUser().then((user) => {
    if (user) {
      router.push({ path: "/" });
    }
  });

  console.log("online");
  Hub.listen("auth", async (data) => {
    if (data.payload.event === "signOut") {
      user = null;
      useUserStore().setUser();
      router.push({ path: "/login" });
    } else if (data.payload.event === "signIn") {
      user = await getUser();
      router.push({ path: "/" });
    }
  });
}

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      component: Home,
    },
    {
      path: "/login",
      name: "login",
      component: Login,
    },
    {
      path: "/drivers",
      name: "drivers",
      component: Drivers,
    },
    {
      path: "/interventions",
      name: "interventions",
      component: Interventions,
    },
    {
      path: "/activities",
      name: "activities",
      component: Activities,
    },
    {
      path: "/projects",
      name: "projects",
      component: Projects,
    },
    {
      path: "/forms/:module",
      name: "forms",
      component: Forms,
    },
    {
      path: "/toc",
      name: "toc",
      component: TheoryOfChangeIndex,
    },
    {
      path: "/monitoring-and-evaluation",
      name: "monitoring-and-evaluation",
      component: MonitoringEvaluationIndex,
    },
  ],
});

export default router;
