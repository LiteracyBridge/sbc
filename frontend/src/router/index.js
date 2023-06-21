import { createRouter, createWebHistory } from "vue-router";
import Drivers from "../views/Drivers.vue";
import Login from "../views/Login.vue";
import Home from "../views/Home.vue";
import Projects from "../views/Projects.vue";
import Forms from "../views/Forms.vue";
import Interventions from "../views/Interventions.vue";
import { useUserStore } from "../stores/user";
import { Auth } from "aws-amplify";
import { Hub } from "@aws-amplify/core";
import { ApiRequest } from "@/apis/api";

import TheoryOfChangeIndex from "@/views/theory-of-change/TheoryOfChangeIndex.vue";
import MonitoringEvaluationIndex from "@/views/monitoring-n-evaluation/MonitoringEvaluationIndex.vue";
import ProjectManagementIndex from "@/views/project-management/ProjectManagementIndex.vue";
import AccessRequest from "@/views/AccessRequest.vue";
import ProjectsIndex from "@/views/projects/ProjectsIndex.vue";
import ProjectObjective from "@/views/ProjectObjective.vue";
import Audience from "@/views/Audience.vue";
import CommunicationsIndex from "@/views/communications/CommunicationsIndex.vue";
import ProjectInfo from "@/views/ProjectInfo.vue";


let user;

async function getUser() {
  return Auth.currentAuthenticatedUser()
    .then(async (data) => {
      if (data && data.signInUserSession) {
        // Verify user from server
        return await ApiRequest.get(`users/${data.attributes.email}`).then(
          async (resp) => {
            if (resp.length == 0) {
              await Auth.signOut();
              return { authorized: false };
            }
            useUserStore().setUser({
              ...resp[0],
              token: data.signInUserSession.accessToken.jwtToken,
            });
            return { ...data, authorized: true };
          }
        );
      }

      return null;
    })
    .catch(() => {
      useUserStore().setUser();
      return null;
    });
}

getUser().then((user) => {
  console.log(user);
  if (user?.authorized == true) {
    router.push({ path: "/" });
  }
});

Hub.listen("auth", async (data) => {
  switch (data.payload.event) {
    case "signIn":
      user = await getUser();
      if (user?.authorized) {
        router.push({ path: "/" });
      } else {
        router.push({ path: "/request-access" });
      }
      // router.push({ path: "/" });
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
      path: "/project-info",
      name: "project-info",
      component: ProjectInfo,
    },
    {
      path: "/interventions",
      name: "interventions",
      component: Interventions,
    },
    {
      path: "/projects",
      name: "projects",
      component: ProjectsIndex,
    },
    {
      path: "/project-objectives",
      name: "project-objectives",
      component: ProjectObjective,
    },
    {
      path: "/audiences",
      name: "audiences",
      component: Audience,
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
      path: "/communications-and-messaging",
      name: "communications-and-messaging",
      component: CommunicationsIndex,
    },
    {
      path: "/monitoring-and-evaluation",
      name: "monitoring-and-evaluation",
      component: MonitoringEvaluationIndex,
    },
    {
      path: "/project-management",
      name: "project-management",
      component: ProjectManagementIndex,
    },
    {
      path: "/request-access",
      name: "request-access",
      component: AccessRequest,
    },
  ],
});

export default router;
