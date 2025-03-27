import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Dashboard',
    component: () => import('../components/DashBoard.vue')
  },
  {
    path: '/news-ranking',
    name: 'NewsRanking',
    component: () => import('../components/NewsRanking.vue')
  },
  {
    path: '/news-detail',
    name: 'NewsDetail',
    component: () => import('../components/NewsDetail.vue')
  }
]
const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router