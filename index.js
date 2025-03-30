import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Dashboard',
    component: () => import('../components/LoginPage.vue'),
    meta: { requiresAuth: true } // 需要认证的页面
  },
  {  
    path: '/login',
    name: 'Login',
    component: () => import('../components/LoginPage.vue')
  },
  {
    path: '/home',
    name: 'Home',
    component: () => import('../components/DashBoard.vue'),
    meta: { requiresAuth: true } // 需要认证的页面
  },
  {
    path: '/database',
    name: 'Database',
    component: () => import('../components/DatabaseManager.vue'),
    meta: { requiresAuth: true } // 需要认证的页面
  },
  {
    path: '/news-ranking',
    name: 'NewsRanking',
    component: () => import('../components/NewsRanking.vue'),
    meta: { requiresAuth: true } // 需要认证的页面
  },
  {
    path: '/news-detail',
    name: 'NewsDetail',
    component: () => import('../components/NewsDetail.vue'),
    meta: { requiresAuth: true } // 需要认证的页面
  }
]
const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const userInfo = localStorage.getItem('userInfo')
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth)
  console.log(userInfo)
  console.log(requiresAuth)
  if (requiresAuth && !userInfo) {
    // 需要认证且未登录，重定向到登录页
    next('/login')
  } else if (!requiresAuth && userInfo) {
    // 已登录用户访问公开页面，重定向到首页
    next('/home')
  } else {
    // 正常放行
    next()
  }
})

export default router