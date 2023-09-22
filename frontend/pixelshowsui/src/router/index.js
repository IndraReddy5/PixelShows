import { createRouter, createWebHistory } from "vue-router";
import UserLogin from "../components/UserLogin.vue";
import SignUp from "../components/SignUp.vue";
import DashboardView from "../views/DashboardView.vue";
import ShowView from "../views/ShowView.vue";
import VenueView from "../views/VenueView.vue";
import SearchView from "../views/SearchView.vue";
import BookTicketsView from "../views/BookTicketsView.vue";
import UserProfileView from "../views/UserProfileView.vue";
import EditPasswordView from "../views/EditPasswordView.vue";
import CreateShowView from "../views/CreateShowView.vue";
import EditShowView from "../views/EditShowView.vue";
import CreateVenueView from "../views/CreateVenueView.vue";
import EditVenueView from "../views/EditVenueView.vue";
import CreateTagView from "../views/CreateTagView.vue";
import EditTagView from "../views/EditTagView.vue";
import CreateVenueTypeView from "../views/CreateVenueTypeView.vue";



const routes = [
  {
    path: "/",
    redirect: "/login",
    name: "home",
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
    path: "/userprofile",
    name: "userprofile",
    component: UserProfileView,
    beforeEnter() {
      if (!localStorage.getItem("Auth-Token")) {
        return "/login";
      }
    }
  },
  {
    path: "/dashboard",
    name: "dashboard",
    component: DashboardView,
    beforeEnter() {
      if (!localStorage.getItem("Auth-Token")) {
        return "/login";
      }
    }
  },
  {
    path: "/booktickets/:sv_id",
    name: "booktickets",
    component: BookTicketsView,
    beforeEnter() {
      if (!localStorage.getItem("Auth-Token")) {
        return "/login";
      }
    }
  },
  {
    path: "/show/:id",
    name: "showpage",
    component: ShowView,
    beforeEnter() {
      if (!localStorage.getItem("Auth-Token")) {
        return "/login";
      }
    }
  },
  {
    path: "/venue/:id",
    name: "venuepage",
    component: VenueView,
    beforeEnter() {
      if (!localStorage.getItem("Auth-Token")) {
        return "/login";
      }
    }
  },
  {
    path: "/searchshow",
    name: "searchage",
    component: SearchView,
    beforeEnter() {
      if (!localStorage.getItem("Auth-Token")) {
        return "/login";
      }
    }
  },
  {
    path: "/editaccount",
    name: "changepassword",
    component: EditPasswordView,
    beforeEnter() {
      if (!localStorage.getItem("Auth-Token")) {
        return "/login";
      }
    }
  },
  {
    path: "/createshow",
    name: "createshow",
    component: CreateShowView,
    beforeEnter() {
      if (!localStorage.getItem("Auth-Token")) {
        return "/login";
      }
      else {
        if (localStorage.getItem("role") != 'admin') {
          alert("You do not have permission to access this page.");
          return "/";
        }
      }
    }
  },
  {
    path: "/editshow/:id",
    name: "editshow",
    component: EditShowView,
    beforeEnter() {
      if (!localStorage.getItem("Auth-Token")) {
        return "/login";
      }
      else {
        if (localStorage.getItem("role") != 'admin') {
          alert("You do not have permission to access this page.");
          return "/";
        }
      }
    }
  },
  {
    path: "/edittag",
    name: "edit",
    component: EditTagView,
    beforeEnter() {
      if (!localStorage.getItem("Auth-Token")) {
        return "/login";
      }
      else {
        if (localStorage.getItem("role") != 'admin') {
          alert("You do not have permission to access this page.");
          return "/";
        }
      }
    }
  },
  {
    path: "/createvenue",
    name: "createvenue",
    component: CreateVenueView,
    beforeEnter() {
      if (!localStorage.getItem("Auth-Token")) {
        return "/login";
      }
      else {
        if (localStorage.getItem("role") != 'admin') {
          alert("You do not have permission to access this page.");
          return "/";
        }
      }
    }
  },
  {
    path: "/editvenue",
    name: "editvenue",
    component: EditVenueView,
    beforeEnter() {
      if (!localStorage.getItem("Auth-Token")) {
        return "/login";
      }
      else {
        if (localStorage.getItem("role") != 'admin') {
          alert("You do not have permission to access this page.");
          return "/";
        }
      }
    }
  },
  {
    path: "/createtag",
    name: "createtag",
    component: CreateTagView,
    beforeEnter() {
      if (!localStorage.getItem("Auth-Token")) {
        return "/login";
      }
      else {
        if (localStorage.getItem("role") != 'admin') {
          alert("You do not have permission to access this page.");
          return "/";
        }
      }
    }
  },
  {
    path: "/createvenuetype",
    name: "createvenuetype",
    component: CreateVenueTypeView,
    beforeEnter() {
      if (!localStorage.getItem("Auth-Token")) {
        return "/login";
      }
      else {
        if (localStorage.getItem("role") != 'admin') {
          alert("You do not have permission to access this page.");
          return "/";
        }
      }
    }
  },
  {
    path: "/logout",
    name: "logout",
    beforeEnter(to, from, next) {
      localStorage.clear();
      next("/login");
    }
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});


export default router;
