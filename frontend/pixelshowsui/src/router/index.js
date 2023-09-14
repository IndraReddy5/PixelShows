import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import UserLogin from "../components/UserLogin.vue";
import SignUp from "../components/SignUp.vue";

const routes = [
  {
    path: "/",
    redirect: "/login",
    name: "home",
  },
  {
    path: "/signup",
    name: "signup",
    component: SignUp,
    beforeEnter() {
      if (localStorage.getItem("Auth-Token")) {
        return "/dashboard";
      }
    }
  },
  {
    path: "/dashboard",
    name: "dashboard",

    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () =>
      import(/* webpackChunkName: "about" */ "../views/AboutView.vue"),

    beforeEnter() {
      if (!localStorage.getItem("Auth-Token")) {
        return "/login";
      }
    }
  },
  {
    path: "/login",
    name: "login",
    component: UserLogin,
    beforeEnter() {
      if (localStorage.getItem("Auth-Token")) {
        return "/dashboard";
      }
    }
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});


export default router;
