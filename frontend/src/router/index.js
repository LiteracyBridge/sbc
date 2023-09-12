import { createRouter, createWebHistory } from "vue-router";
import Drivers from "../views/Drivers.vue";
import Login from "../views/Login.vue";
import Home from "../views/Home.vue";
// import Projects from "../views/Projects.vue";
import Forms from "../views/Forms.vue";
import Interventions from "../views/Interventions.vue";
import { useUserStore } from "../stores/user";
import { Auth } from "aws-amplify";
import { Hub } from "@aws-amplify/core";
import { ApiRequest } from "@/apis/api";
import { AppStore } from "../stores/app.store";

import TheoryOfChangeIndex from "@/views/theory-of-change/TheoryOfChangeIndex.vue";
import MonitoringEvaluationIndex from "@/views/monitoring-n-evaluation/MonitoringEvaluationIndex.vue";
import ProjectManagementIndex from "@/views/project-management/ProjectManagementIndex.vue";
import AccessRequest from "@/views/AccessRequest.vue";
import ProjectsIndex from "@/views/projects/ProjectsIndex.vue";
import ProjectObjective from "@/views/ProjectObjective.vue";
import Audience from "@/views/Audience.vue";
import CommunicationsIndex from "@/views/communications/CommunicationsIndex.vue";
import ProjectInfo from "@/views/ProjectInfo.vue";
import Partners from "@/views/Partners.vue";
import BackgroundAndContext from "@/views/BackgroundAndContext.vue";
import ProjectDocsIndex from "@/views/project-docs/ProjectDocsIndex.vue";
import { User } from "@/types";

function disabledConsole() {
  if (import.meta.env.PROD) {
    console.log = function () {};
    // console.error = function () {};
    // console.warn = function () {};
  }
}

let user;

async function getUser() {
  return Auth.currentAuthenticatedUser()
    .then(async (data) => {
      if (data && data.signInUserSession) {
        useUserStore().token = data.signInUserSession.accessToken.jwtToken;
        console.log("here");

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

      AppStore().is_loading = false;
      return { authorized: false };
    })
    .catch(() => {
      AppStore().is_loading = false;
      useUserStore().setUser();
      return { authorized: false };
    });
}

Hub.listen("auth", async (data) => {
  disabledConsole();

  console.log(data.payload.event);
  switch (data.payload.event) {
    case "signIn":
      user = await getUser();
      if (user?.authorized == true) {
        await AppStore().downloadObjects();
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
      window.location.reload();
      break;
    case "signIn_failure":
      console.log("user sign in failed");
      break;
    case "configured":
      console.log(data.payload.event);
      getUser().then(async (user) => {
        console.log("Existing user: ", user);
        console.log(user);
        if (user?.authorized == true) {
          await AppStore().downloadObjects();

          router.push({ path: "/" });
        } else {
          router.push({ path: "/login" });
        }
      });
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
      meta: { title: "Dashboard" },
    },
    {
      path: "/login",
      name: "login",
      component: Login,
      meta: { title: "Login" },
    },
    {
      path: "/background-and-context",
      name: "background-and-context",
      component: BackgroundAndContext,
      meta: { title: "Background and Context" },
    },
    {
      path: "/drivers",
      name: "drivers",
      component: Drivers,
      meta: { title: "Behaviour Drivers" },
    },
    {
      path: "/project-info",
      name: "project-info",
      component: ProjectInfo,
      meta: { title: "Project Information" },
    },
    {
      path: "/interventions",
      name: "interventions",
      component: Interventions,
      meta: { title: "Interventions" },
    },
    {
      path: "/projects",
      name: "projects",
      component: ProjectsIndex,
      meta: { title: "Projects" },
    },
    {
      path: "/project-objectives",
      name: "project-objectives",
      component: ProjectObjective,
      meta: { title: "Project Objectives" },
    },
    {
      path: "/audiences",
      name: "audiences",
      component: Audience,
      meta: { title: "Audiences" },
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
      meta: { title: "Theory of Change" },
    },
    {
      path: "/communications-and-messaging",
      name: "communications-and-messaging",
      component: CommunicationsIndex,
      meta: { title: "Communications and Messaging" },
    },
    {
      path: "/monitoring-and-evaluation",
      name: "monitoring-and-evaluation",
      component: MonitoringEvaluationIndex,
      meta: { title: "Monitoring and Evaluation" },
    },
    {
      path: "/project-management",
      name: "project-management",
      component: ProjectManagementIndex,
      meta: { title: "Project Management" },
    },
    {
      path: "/request-access",
      name: "request-access",
      component: AccessRequest,
      meta: { title: "Request Access" },
    },
    {
      path: "/partners",
      name: "partners",
      component: Partners,
      meta: { title: "Partners" },
    },
    {
      path: "/project-documents",
      name: "docs",
      component: ProjectDocsIndex,
      meta: { title: "Project Documents" },
    },
  ],
});

router.beforeEach((to, from, next) => {
  const title = to.meta.title;
  if (title) {
    document.title = `SBC Impact Designer | ${title}`;
  }
  // Continue resolving the route
  next();
});

router.afterEach((to, from) => {
  if (window.gtag) {
    gtag("event", "screen_view", {
      page_location: to.fullPath,
      page_title: to.meta?.title,
    });
  }
});
export default router;
