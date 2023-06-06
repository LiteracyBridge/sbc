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
import { ApiRequest } from "@/apis/api";

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
    switch (data.payload.event) {
      case "signIn":
        user = await getUser();
        router.push({ path: "/" });
        break;
      case "signUp":
        console.log(data);
        // TODO: add a/c to sbc
        const _user = data.payload.data.attributes;
        console.log(_user);

        ApiRequest.post("users/", {
          email: _user.email,
          name: _user.name,
        }).then((resp) => {
          console.log("account created");
          console.warn(resp);
        });
        console.log("user signed up");
        break;
      case "signOut":
        user = null;
        useUserStore().setUser();
        router.push({ path: "/login" });
        break;
      case "signIn_failure":
        console.log("user sign in failed");
        break;
      case "configured":
        console.log("the Auth module is configured");
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
