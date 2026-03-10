import { createRouter, createWebHistory } from 'vue-router'
import AuthLayout from '../layouts/AuthLayout.vue'
import PublicLayout from '../layouts/PublicLayout.vue'
import LogoutPage from '../pages/auth/LogoutPage.vue'
import HomePage from '../pages/home/index.vue'
import SiginPage from '../pages/auth/SiginPage.vue'
import SigupPage from '../pages/auth/SigupPage.vue'
import store from '../store'

const routes = [
  {
    path: '/login',
    redirect: { name: 'signin' }
  },
  {
    path: '/signin',
    component: PublicLayout,
    children: [
      {
        path: '',
        name: 'signin',
        component: SiginPage
      }
    ]
  },
  {
    path: '/signup',
    component: PublicLayout,
    children: [
      {
        path: '',
        name: 'signup',
        component: SigupPage
      }
    ]
  },
  {
    path: '/logout',
    name: 'logout',
    component: LogoutPage
  },
  {
    path: '/',
    component: AuthLayout,
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
        name: 'home',
        component: HomePage
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to) => {
  const requiresAuth = to.matched.some((record) => record.meta.requiresAuth)
  const isAuthenticated = store.getters.isAuthenticated

  if (requiresAuth && !isAuthenticated) {
    return { name: 'signin' }
  }
  if ((to.name === 'signin' || to.name === 'signup') && isAuthenticated) {
    return { name: 'home' }
  }
  return true
})

export default router
