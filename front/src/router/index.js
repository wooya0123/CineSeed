import LogInView from '@/views/LogInView.vue'
import SignUpView from '@/views/SignUpView.vue'
import BaseHomeView from '@/views/BaseHomeView.vue'
import BaseProfileView from '@/views/BaseProfileView.vue'

import { createRouter, createWebHistory } from 'vue-router'
import { useAccountStore } from '@/stores/account'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: BaseHomeView
    },
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
    {
      path: '/profile/:id',
      name: 'profile',
      component: BaseProfileView,
      meta: { requiresAuth: true } // 인증이 필요한 라우트에 메타 필드 추가
    },
  ],
})

// 네비게이션 가드 추가
router.beforeEach((to, from, next) => {
  const accountStore = useAccountStore()
  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!accountStore.isLogIn) {
      next({ name: 'login' }) // 로그인 페이지로 리디렉션
    } else {
      next()
    }
  } else {
    next()
  }
})

export default router
