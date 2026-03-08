import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/history',
    name: 'History',
    component: () => import('../views/History.vue')
  },
  {
    path: '/documents',
    name: 'DocumentManagement',
    component: () => import('../views/DocumentManagement.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router