import { createRouter, createWebHistory } from 'vue-router'

import MainLayout from '../layouts/MainLayout.vue'

import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import DashboardView from '../views/DashboardView.vue'
import ProjectsView from '../views/ProjectsView.vue'
import ProjectView from '../views/ProjectView.vue'
import ProfileView from '../views/ProfileView.vue'
import SettingsView from '../views/SettingsView.vue'


const routes = [

  {
    path: '/',
    redirect: '/dashboard'
  },


  {
    path: '/login',
    name: 'login',
    component: LoginView
  },


  {
    path: '/register',
    name: 'register',
    component: RegisterView
  },


  {
    path: '/',
    component: MainLayout,

    children: [

      {
        path: 'dashboard',
        name: 'dashboard',
        component: DashboardView,
        meta: {
          requiresAuth: true
        }
      },


      {
        path: 'projects',
        name: 'projects',
        component: ProjectsView,
        meta: {
          requiresAuth: true
        }
      },


      {
        path: 'projects/:id',
        name: 'project',
        component: ProjectView,
        props: true,
        meta: {
          requiresAuth: true
        }
      },


      {
        path: 'profile',
        name: 'profile',
        component: ProfileView,
        meta: {
          requiresAuth: true
        }
      },


      {
        path: 'settings',
        name: 'settings',
        component: SettingsView,
        meta: {
          requiresAuth: true
        }
      }

    ]
  }

]


const router = createRouter({

  history: createWebHistory(),

  routes

})



router.beforeEach((to, from, next) => {


  const token = localStorage.getItem('access')


  if (to.meta.requiresAuth && !token) {

    next('/login')

  } else {

    next()

  }


})



export default router