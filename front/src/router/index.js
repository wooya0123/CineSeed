import LogInView from '@/views/LogInView.vue'
import SignUpView from '@/views/SignUpView.vue'
import GameBanner from '@/components/GameBanner.vue'

import { createRouter, createWebHistory } from 'vue-router'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/signup',
      name: 'signup',
      component: SignUpView
    },
    {
      path: '/login',
      name: 'login',
      component: LogInView
    },
  ],
})

export default router
